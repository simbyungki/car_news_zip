import requests
import re
import regex
import time
import os, json
import pandas as pd
import mysql.connector
from datetime import datetime
from bs4 import BeautifulSoup
from konlpy.tag import Kkma

## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
## 장고 프로젝트를 사용할 수 있도록 환경을 구축
import django
django.setup()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath('./mysite'))
# SECURITY WARNING: keep the secret key used in production secret!
db_info_file = os.path.join(BASE_DIR, 'db_conn.json')
db_info_file2 = os.path.join(BASE_DIR, 'db_conn_apdb.json')
# db_info_file = os.path.join(BASE_DIR, 'db_conn.json')
with open(db_info_file) as f :
	db_infos = json.loads(f.read())
with open(db_info_file2) as f :
	db_infos2 = json.loads(f.read())

def remove_html(sentence) :
	sentence = re.sub('(<([^>]+)>)', '', sentence)
	return sentence

def get_soup(url) :
	try : 
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
		res = requests.get(url, headers = headers, verify=False)
		# res = requests.get(url, headers = headers)
		res.raise_for_status()
		res.encoding = None
		soup = BeautifulSoup(res.text, 'lxml')
		return soup
	except Exception as e :
		print(f'requests error! >> {e}')
		pass	

###
# 글 목록 가져오기
###
def get_post_list(board_type, dbconn, cursor) :
	page_number = 1
	page_scale = 50
	total_post = []
	# 1. 목록에서 글 가져와 DB INSERT
	for idx in range(1) : 
		print(f'>> [{board_type}]{page_number}번 페이지 작업 시작합니다.')
		# 보배드림 국산차/수입차 게시판
		url = f'https://www.bobaedream.co.kr/list?code={board_type}&s_cate=&maker_no=&model_no=&or_gu=10&or_se=desc&s_selday=&pagescale={page_scale}&info3=&noticeShow=&s_select=Subject&s_key=&level_no=&vdate=&type=list&page={page_number}'
		print(f'수집 : {url}')
		try : 
			soup = get_soup(url)
		except : 
			print("Connection refused by the server..")
			print("Let me sleep for 5 seconds")
			time.sleep(5)
			continue
		finally : 
			tr_list = soup.select('#boardlist tbody tr["itemtype"]')
			# print(len(board_list))
			for idx, tr in enumerate(tr_list) :
				tr_no= post_code= title= writer= recommend_cnt= view_cnt= date = ''
				if tr.select_one('.num01') is not None :
					tr_no = tr.select_one('.num01').get_text().strip()
					# link_url = tr.select_one('.bsubject')['href']
				if tr.select_one('.bsubject') is not None :
					if board_type == 'national' :
						post_code = tr.select_one('.bsubject')['href'][-12:-5]
					elif board_type == 'import' : 
						post_code = tr.select_one('.bsubject')['href'][-11:-5]
					title = tr.select_one('.bsubject').get_text().strip()
				if tr.select_one('.author') is not None :
					writer = tr.select_one('.author').get_text().strip()
				if tr.select_one('.recomm') is not None :
					recommend_cnt = tr.select_one('.recomm').get_text().strip()
				if tr.select_one('.count') is not None :
					view_cnt = tr.select_one('.count').get_text().strip()
				if tr.select_one('.date') is not None :
					date = tr.select_one('.date').get_text().strip()
				full_url = f'https://www.bobaedream.co.kr/view?code={board_type}&No={post_code}&bm=1'
				# print(tr_no, link_url, title, writer, date)
				in_obj = {}
				in_obj['tr_no'] = tr_no
				in_obj['post_code'] = post_code
				in_obj['title'] = title
				in_obj['writer'] = writer
				in_obj['view_cnt'] = view_cnt
				in_obj['recommend_cnt'] = recommend_cnt
				in_obj['full_url'] = full_url
				in_obj['date'] = date
				total_post.append(in_obj)    

				# 가져온 글 DB INSERT (중복 제외)
				try :
					cursor.execute(f"""
					INSERT IGNORE INTO TBL_BOBAE_POST_CODE_LIST 
						(
							POST_CODE, URL, VIEW_CNT, RECOMMEND_CNT, UPDATE_DATE
						) 
						VALUES (
							"{post_code}", "{full_url}", {view_cnt}, {recommend_cnt}, NOW()
						) 
					""")
				except Exception as e :
					print(f'***** POST LIST DB INSERT ERROR! >> {e}')	
					pass
				finally : 
					print(f'[{post_code}][DB Insert 완료!] {title}')
					dbconn.commit()
		
	print(f'>>>> 총 {len(total_post)}개의 글 수집 완료!')

def sentence_mining(dbconn, cursor) : 
	# 2. 글 상세 콘텐츠 가져오기
	try :
		kkma = Kkma()
		# 형태소 분석
		except_word_list = []
		cursor.execute(f"""
			SELECT 
				POST_CODE, URL
			FROM 
				TBL_BOBAE_POST_CODE_LIST 
			WHERE 
				MINING_STATUS = 1
		""")
		rows = cursor.fetchall()
	except Exception as e :
		print(f'***** TBL_BOBAE_POST_CODE_LIST SELECT ERROR! >> {e}')	
		pass
	finally : 
		if len(rows) == 0 : 
			print('모든 글 분석이 완료된 상태입니다.')
		else : 
			print(len(rows), '개의 목록 작업 시작')
			for row in rows : 
				word_no_list = []
				results = []
				post_code = row[0]
				# 형태소 분석 > KEYWORD LIST DB INSERT
				if (get_post_detail(row[1], post_code) is not None) and (get_post_detail(row[1], post_code) != '') : 
					# 특수문자 제거
					detail = re.sub('[-=.#/?:$}\"\']', '', str(get_post_detail(row[1], post_code))).replace('[','').replace(']','')
					# 어절 분리 > list
					origin_word_list = list(dict.fromkeys(regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}|\d+]+', f'{detail}')))

					for origin_word in origin_word_list :
						if (origin_word not in except_word_list) : 
							for morpheme in kkma.pos(origin_word) :
								in_result = []	
								in_result.append(origin_word)
								in_result.append(morpheme)
								results.append(in_result)

					print('*' * 80)
					print(f'Depth_idx1 >> [{post_code}] >> {detail}')
					# DB KEYWORD LIST TABLE INSERT
					for idx, result in enumerate(results) :
						print('ㅡ' * 50)
						#[QNA_NO][바깥쪽 idx][어절 idx][형태소 idx]
						print(f'Depth_for1 >> [{post_code}][{idx}] >> {result}')	
						if idx == 0 :
							try : 
								word_no_item = []
								cursor.execute(f"""
									SELECT 
										WORD_CLASS_CODE
									FROM 
										TBL_ANAL_WORD_CLASS 
									WHERE 
										CLASS_NAME = "{result[1][1]}"
								""")
								result_word_class_code = cursor.fetchall()[0][0]
								cursor.execute(f"""
									INSERT INTO TBL_BOBAE_KEYWORD_LIST 
									(
										POST_CODE, WORD_ORIGIN, WORD_MORPHEME, WORD_CLASS_CODE, WORD_CLASS, UPDATE_DATE
									) 
									VALUES (
										"{post_code}", "{result[0]}", "{result[1][0]}", "{result_word_class_code}", "{result[1][1]}", NOW()
									)
								""")
								cursor.execute(f"""
									SELECT AUTO_INCREMENT
									FROM information_schema.tables 
									WHERE TABLE_NAME = 'TBL_BOBAE_KEYWORD_LIST' AND TABLE_SCHEMA = DATABASE();
								""")
								result_word_no = cursor.fetchone()[0]
								word_no_item.append(result[1][0])
								word_no_item.append(result_word_no)
								word_no_list.append(word_no_item)
							except Exception as e :
								print(f'****** {post_code} >> TBL_BOBAE_KEYWORD_LIST > KEYWORD INSERT error! >> {e}')
								continue
							finally : 
								pass	
						# 단어 거리 계산
						for depth_idx, depth_result in enumerate(results) :
							if idx != depth_idx :
								if idx == 0 :	
									word_no_item = []
									try :
										# 타겟
										cursor.execute(f"""
											SELECT 
												WORD_CLASS_CODE
											FROM 
												TBL_ANAL_WORD_CLASS 
											WHERE 
												CLASS_NAME = "{depth_result[1][1]}"
										""")
										result_word_class_code2 = cursor.fetchall()[0][0]
										cursor.execute(f"""
											INSERT INTO TBL_BOBAE_KEYWORD_LIST 
											(
												POST_CODE, WORD_ORIGIN, WORD_MORPHEME, WORD_CLASS_CODE, WORD_CLASS, UPDATE_DATE
											) 
											VALUES (
												"{post_code}", "{depth_result[0]}", "{depth_result[1][0]}", "{result_word_class_code}", "{depth_result[1][1]}", NOW()
											)
										""")
										cursor.execute(f"""
											SELECT AUTO_INCREMENT
											FROM information_schema.tables 
											WHERE TABLE_NAME = 'TBL_BOBAE_KEYWORD_LIST' AND TABLE_SCHEMA = DATABASE();
										""")
										result_word_no2 = cursor.fetchone()[0]
										# print(f'###### 타겟 [{depth_result[1][0]}][{result_word_class_code2}][{result_word_no2}]')

										word_no_item.append(depth_result[1][0])
										word_no_item.append(result_word_no2)
										word_no_list.append(word_no_item)
										
									except Exception as e :
										print(f'****** + error! >> {e} >>>>> [{post_code} >> TBL_BOBAE_KEYWORD_LIST > KEYWORD INSERT 오류!]')
										continue
									finally : 
										pass

									if (result[1][1] == 'NNG' or result[1][1] == 'NNP' or result[1][1] == 'NNB' or result[1][1] == 'NNM') and (depth_result[1][1] == 'NNG' or depth_result[1][1] == 'NNP' or depth_result[1][1] == 'NNB' or depth_result[1][1] == 'NNM') and (len(result[1][0]) > 1 and len(depth_result[1][0]) > 1) : 
										#[post_code][바깥쪽 idx][어절 idx][형태소 idx]
										print(f'Depth_for2 >> [{post_code}][{idx}][{depth_idx}] >> [{result[0]}/{result[1][0]}][{depth_result[0]}/{depth_result[1][0]}]')
										# print(f'2번 조건 통과 >> [{result[1][1]}][{depth_result[1][1]}]')
										# print(f'Depth_for2 >> [{result[1][1]}][{depth_result[1][1]}]')
										try : 
											rows = []
											if result[0] != depth_result[0] and result[1][0] != depth_result[1][0] :
												cursor.execute(f"""
													SELECT 
														MAP_NO, WORD_DISTANCE
													FROM 
														TBL_BOBAE_KEYWORD_MAP
													WHERE 
														(
															SOURCE_WORD = "{result[0]}" AND 
															SOURCE_MORPHEME_WORD = "{result[1][0]}" AND 
															TARGET_WORD = "{depth_result[0]}" AND 
															TARGET_MORPHEME_WORD = "{depth_result[1][0]}"
														)
														OR
														(
															SOURCE_WORD = "{depth_result[0]}" AND 
															SOURCE_MORPHEME_WORD = "{depth_result[1][0]}" AND 
															TARGET_WORD = "{result[0]}" AND 
															TARGET_MORPHEME_WORD = "{result[1][0]}"
														)
												""")
												rows = cursor.fetchall()
										except Exception as e :
											print(f'****** + error! >> {e} >>>>> [{post_code} >> TBL_BOBAE_KEYWORD_MAP > SELECT 오류!]')
											continue
										finally : 
											pass

											# 3. TBL_BOBAE_KEYWORD_MAP 테이블에서 4가지 조건 동일한 데이터가 있으면 WORD_DISTANCE 1더해서 업데이트 
											if len(rows) > 0 : 
												# print('@@ 3번 프로세스 @@ TBL_BOBAE_KEYWORD_MAP 중복되는 것 있다 > 업데이트')
												return_datas = {}
												for row_idx, row in enumerate(rows) :
													return_datas['map_no'] = int(row[0])
													return_datas['distance'] = int(row[1])
												# print(f'@@ 3번 프로세스 @@ 업데이트 전 데이터 확인! {return_datas}')
												try : 
													cursor.execute(f"""
														UPDATE
															TBL_BOBAE_KEYWORD_MAP 
														SET
															WORD_DISTANCE = {return_datas.get('distance') + 1}
														WHERE 
															MAP_NO = {return_datas.get('map_no')}
													""")
												except Exception as e :
													print(f'****** + error! >> {e} >>>>> [{post_code} >> TBL_BOBAE_KEYWORD_MAP > UPDATE 오류!]')
													continue
												finally : 
													pass
											# 4. TBL_BOBAE_KEYWORD_MAP 테이블에서 4가지 조건 동일한 데이터가 없으면 4가지 조건값 그대로 인서트						
											else : 
												# print('@@ 4번 프로세스 @@ TBL_BOBAE_KEYWORD_MAP 중복되는 것 없다 > 인서트')
												try : 
													cursor.execute(f"""
														SELECT 
															WORD_CLASS_CODE 
														FROM 
															TBL_ANAL_WORD_CLASS 
														WHERE 
															CLASS_NAME = "{result[1][1]}"
													""")
													result_word_class_code1 = cursor.fetchall()[0][0]
													result_word_class_code1 = str(result_word_class_code1) + f'-{result[1][1]}'
													# print('조합된 class code1 = ', result_word_class_code1)
													# print('조합된 class code1 type = ', type(result_word_class_code1))
													
													cursor.execute(f"""
														SELECT 
															WORD_CLASS_CODE 
														FROM 
															TBL_ANAL_WORD_CLASS 
														WHERE 
															CLASS_NAME = "{depth_result[1][1]}"
													""")
													result_word_class_code2 = cursor.fetchall()[0][0]
													result_word_class_code2 = str(result_word_class_code2) + f'-{depth_result[1][1]}'
													# print('조합된 class code2 = ', result_word_class_code2)
													# print('조합된 class code2 type = ', type(result_word_class_code2))
													
													result_word_no1 = 0
													result_word_no2 = 0
													for word_no_item in word_no_list :
														if word_no_item[0] == result[1][0] : 
															result_word_no1 = word_no_item[1]
														if word_no_item[0] == depth_result[1][0] : 
															result_word_no2 = word_no_item[1]

													##########################################################################################
													cursor.execute(f"""
														INSERT INTO 
															TBL_BOBAE_KEYWORD_MAP 
															(SOURCE_WORD_NO, SOURCE_WORD, SOURCE_CLASS_CODE, SOURCE_MORPHEME_WORD, TARGET_WORD_NO, TARGET_WORD, TARGET_CLASS_CODE, TARGET_MORPHEME_WORD, WORD_DISTANCE, UPDATE_DATE)
														VALUES
															("{result_word_no1}", "{result[0]}", "{result_word_class_code1}", "{result[1][0]}", "{result_word_no2}", "{depth_result[0]}", "{result_word_class_code2}", "{depth_result[1][0]}", 1, NOW())
													""")
												except Exception as e :
													print(f'****** + error! >> {e} >>>>> [{post_code} >> TBL_BOBAE_KEYWORD_MAP > INSERT 오류!]')
													continue
												finally : 
													dbconn.commit()
													pass				
				else : 
					continue

				# for idx, origin_word in enumerate(origin_word_list) : 
				# 	if idx == 0 : 
				# 		print(f'{origin_word} : {origin_word_list[1]}, {origin_word_list[2]}')
				# 	elif idx == len(origin_word_list) - 1 : 
				# 		print(f'{origin_word} : {origin_word_list[len(origin_word_list) - 3]}, {origin_word_list[len(origin_word_list) -2 ]}')
				# 	elif idx == 1 : 
				# 		print(f'{origin_word} : {origin_word_list[idx-1]}, {origin_word_list[idx+1]}, {origin_word_list[idx+2]}')
				# 	elif idx == len(origin_word_list) - 2 : 
				# 		print(f'{origin_word} : {origin_word_list[idx-2]}, {origin_word_list[idx-1]}, {origin_word_list[idx+1]}')
				# 	else : 
				# 		try : 
				# 			print(f'{origin_word} : {origin_word_list[idx-2]}, {origin_word_list[idx-1]}, {origin_word_list[idx+1]}, {origin_word_list[idx+2]}')
				# 		except : 
				# 			continue



				# 상태값 업데이트 (분석완료상태)
				try : 
					cursor.execute(f"""
						UPDATE 
							TBL_BOBAE_POST_CODE_LIST 
						SET 
							MINING_STATUS = 3,
							MINING_DATE = NOW()
						WHERE
							POST_CODE = "{post_code}"
					""")	
				except Exception as e :
					print(f'***** TBL_BOBAE_POST_CODE_LIST UPDATE (MINING STATUS) ERROR! >> {e}')	
					pass
				finally : 
					time.sleep(1)	
	# return total_post


###
# 글 상세 콘텐츠 가져오기
###
def get_post_detail(url, post_code) : 
	# print(f'>> 글 상세 내용 수집 시작합니다.')
	# url = f'https://www.bobaedream.co.kr/view?code={board_type}&No={post_code}&bm=1'
	print('ㅡ'* 30)
	print(url)
	soup = get_soup(url)
	title = ''
	content = ''
	try : 
		detail = soup.select_one('#print_area')
		title = detail.select_one('.writerProfile dl dt').attrs['title'].strip()
		content = detail.select_one('.bodyCont').get_text().strip().replace('\n', '').replace('\xa0', '').replace('\r', '')
		return title + ' ' + content
	except Exception as e : 
		print(f'get post detail error! >> {e}')
		pass
	finally : 
		time.sleep(3)


def input_to_morphemes(sentence) :
	kkma = Kkma()
	# 불용어
	except_word_list = []
	# 허용 형태소 타입 >> VA 형용사 /  VV 동사 / OL 외국어 / OH 한자 / 명사 추정 범주
	types = ['NNG', 'NNP', 'NNB', 'NNM', 'NP', 'VA', 'UN']
	# 특수문자 제거
	sentence = re.sub('[-=.#/?:$}\"\']', '', str(sentence)).replace('[','').replace(']','')
	# 어절 분리 > list
	origin_word_list = list(dict.fromkeys(regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}|\d+]+', f'{sentence}')))
	print(origin_word_list)
	results = []
	morphemes = []
	# 형태소 분석 단어 추출
	for origin_word in origin_word_list :
		if (origin_word not in except_word_list) : 
			for morpheme in kkma.pos(origin_word) :
				in_result = []	
				in_result.append(origin_word)
				in_result.append(morpheme)
				results.append(in_result)
				# 허용된 타입 & 2글자 이상의 단어만 추출
				if (morpheme[1] in types) and (len(morpheme[0]) > 1): 
					morphemes.append(morpheme)
	print(morphemes)
	return morphemes

def compare_morphemes(new_morphemes, dbconn, cursor) :
	# 기존 문장의 형태소 단어 SELECT
	cursor.execute(f"""
		SELECT 
			POST_CODE, WORD_MORPHEME
		FROM 
			TBL_BOBAE_KEYWORD_LIST
		WHERE
			CHAR_LENGTH(WORD_MORPHEME) > 1 AND
			(WORD_CLASS = 'NNG' OR WORD_CLASS = 'NNP' OR WORD_CLASS = 'NNB' OR WORD_CLASS = 'NNM' OR WORD_CLASS = 'NP' OR WORD_CLASS = 'VA' OR WORD_CLASS = 'UN')
		GROUP BY POST_CODE, WORD_MORPHEME
	""")
	old_morphemes = cursor.fetchall()
	print('new_morphemes', new_morphemes)
	print('old_morphemes', old_morphemes[0:5])

	# # 신규 문장과 형태소 단어 비교
	# results = []
	# for idx, old_morpheme in enumerate(old_morphemes) : 
	# 	for new_morpheme in new_morphemes : 	
	# 		if old_morpheme[1] == new_morpheme[0] : 
	# 			results.append([old_morpheme[0], old_morpheme[1]])

	# count = {}
	# # 중복 취합
	# for idx, result in enumerate(results) : 
	# 	try : 
	# 		count[result[0]] += 1
	# 	except : 
	# 		count[result[0]] = 1
	# # sorting
	# fin_result = sorted(count.items(), key=(lambda v: v[1]), reverse = True)
	# print('*'* 60)
	# print(fin_result)
	# # get detail URL
	# print('*'* 60)
	# for idx, result in enumerate(fin_result) : 
	# 	if idx < 3 : 
	# 		post_code = result[0]
	# 		url = f'https://www.bobaedream.co.kr/view?code=national&No={post_code}&bm=1'
	# 		print(f'{idx + 1}번째 추천(유사) 글 : {url}')
	# 		print('*'* 60)


if __name__ == '__main__' : 
	now = time.localtime()
	start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	# print(input_to_morphemes('제네시스 G80 전동화모델 이름 깨네 ㅋㅋㅋ Q30 G70'))
	# compare_morphemes(input_to_morphemes('솔직히 국산 SUV 중 투싼이 갑 아니냐'), dbconn, cursor)

	# dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	# cursor = dbconn.cursor()

	# # 글 목록 가져오기 (DB Insert)
	get_post_list('national', dbconn, cursor)
	get_post_list('import', dbconn, cursor)
	# # 문장 분석
	sentence_mining(dbconn, cursor)

	dbconn.close()

	now = time.localtime()
	end_time = now
	print('ㅡ'*50)
	print('보배드림 국산차 게시판 게시물 분석 DB Commit/Close 완료!')
	print('보배드림 국산차 게시판 게시물 분석 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('보배드림 국산차 게시판 게시물 분석 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))