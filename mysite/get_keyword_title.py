import requests
import time
import schedule
import re
import regex
import mysql.connector
import pymssql
import os, json
import traceback
from wordcloud import WordCloud
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
## 장고 프로젝트를 사용할 수 있도록 환경을 구축
import django
django.setup()

from website.models import TblTotalCarNewsList, TblMemberList, TblNewsKeywordList, TblNewsKeywordMap, TblNewsAllKeywordList
from datetime import datetime
from konlpy.tag import Kkma
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

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

# 뉴스 분석
mining_result_data = []

def test_mining(sentence) : 
	# # kkma = Kkma()
	# # print(kkma.pos(keyword))
	# keyword_list = []
	# # keyword_list = []
	# keyword_table = TblNewsAllKeywordList.objects.all().filter(mining_obj = '3')
	# for idx, keyword_row in enumerate(keyword_table) : 
	# 	keyword_list.append([keyword_row.word_morpheme, keyword_row.news_no])
	
	# # print(len(keyword_list))

	# # car_list = getCarModelList()
	# car_list = [[1, '에스컬레이드']]
	# keyword_list = [['레이', 100]]
	# for car in car_list : 
	# 	for keyword in keyword_list :
	# 		if car[1] == keyword[0] : 
	# 			print(f'일치 : {car} >> [{keyword[0]}][{keyword[1]}]')

	print(regex.findall(u'[\p{Hangul}|\p{Latin}|\p{Han}|\d+]+', f'{sentence}'))


# APDB에서 차량 모델 조회
def getCarModelList() :
	dbconn2 = pymssql.connect(host=db_infos2.get('host'), user=db_infos2.get('user'), password=db_infos2.get('password'), database=db_infos2.get('database'), port=db_infos2.get('port'), charset='EUC-KR')
	cursor2 = dbconn2.cursor()

	carModelList = []

	cursor2.execute(f"""
		SELECT 
			BONO, 
			REPLACE(BONAME,' ','') 
		FROM 
			ATB_NCAR_MODEL 
		GROUP BY 
			BONO, BONAME
	""")
	rows = cursor2.fetchall()
	
	for idx, row in enumerate(rows) :
		model = []
		model.append(row[0])
		model.append(row[1])
		carModelList.append(model)


	cursor2.close()
	dbconn2.close()

	# print(carModelList)
	return carModelList

def test_code() :
	sample_list = [1,2,4,5,6,7,8]
	for sample in sample_list : 
		# print(sample, type(sample))
		if not (sample == 2 or sample == 5) : 
		# if ((sample != 2) or (sample != 5)) : 
			print('11@@', sample)
		else :
			print('22@@', sample)

	pass

def text_mining(cont_type, dbconn, cursor) :
	kkma = Kkma()
	car_model_list = getCarModelList()
	car_news_list = TblTotalCarNewsList.objects.all().filter(title_mining_status = 1)
	except_word_list = []
	except_keyword_list = []
	origin_sentence_list = []
	news_no = 0

	# print(car_news_list)
	
	print(f'형태소 분석 시작 ({len(car_news_list)}건)')

	# 뉴스 제목 분석
	if cont_type == 'news' : 
		# step01. 형태소 분석 (데이터 가공)
		for idx in range(len(car_news_list)) :
		# for idx in range(3) :
			print(f'[{idx} // {len(car_news_list)}] 데이터 가공 완료')
			replace_news_title = re.sub('\,', '&#44;', re.sub('[\"\'‘“”″′]', '&#8220;', car_news_list[idx].news_title))
			re_title = regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}|\d+]+', f'{car_news_list[idx].news_title}')

			# print(f'[{idx}] >> {len(re_title)}')
			# print('-'*50)
			in_result_data = []
		# in_result_data[0] 각종 카운트 사전
			etc_info_dic = {}
			# 형태소 단어 총 개수
			etc_info_dic['morpheme_count'] = len(re_title)
			# 형용사 개수
			va_count = 0
			etc_info_dic['va_count'] = va_count
			# 긍정단어 개수
			p_count = 0
			etc_info_dic['positive_count'] = p_count
			# 부정단어 개수
			n_count = 0
			etc_info_dic['negative_count'] = n_count
			# 미디어 코드
			etc_info_dic['media_code'] = car_news_list[idx].media_code
			
			in_result_data.append(etc_info_dic)
		# in_result_data[1] 뉴스 번호
			in_result_data.append(car_news_list[idx].news_no)
			# 뉴스 타이틀
			for word in re_title :
				in_result_word = []	
				group = []
				if (word not in except_word_list) :
					word_g = []
					word_g.append(word)
					group.append(word_g)
					for keyword in kkma.pos(word) :
						if (keyword not in except_keyword_list) :
							in_result_word.append(keyword)
					group.append(in_result_word)
				
				in_result_data.append(group)
			
			in_result_data[0]['re_title'] = replace_news_title
			mining_result_data.append(in_result_data)
		print(mining_result_data)

		# step02. DB Insert
		print('DB Insert')
		try : 
			for out_idx, data_list in enumerate(mining_result_data) :
				media_code = data_list[0].get('media_code')
				print('미디어코드 = ', media_code)
				for idx, data in enumerate(data_list) :
					try : 
						if idx > 1 : 
							news_no = data_list[1]
							origin_word = re.sub('[-=.#/?:$}\"\']', '', str(data[0])).replace('[','').replace(']','')
							print(f'*** : [{out_idx}/{len(mining_result_data) -1}][{news_no}][{idx}/{len(data_list)}][{origin_word}]')
							# data[1] 형태소 분석 (세트) >> ex) [('신', 'NNG'), ('차', 'NNG')]
							for in_idx, word in enumerate(data[1]) :
								# INSERT
								cursor.execute(f"""
									INSERT IGNORE INTO TBL_NEWS_KEYWORD_LIST 
									(
										WORD_MORPHEME, WORD_CLASS, UPDATE_DATE
									) 
									VALUES (
										"{word[0]}", "{word[1]}", NOW()
									)
								""")

								cursor.execute(f"""
									INSERT INTO TBL_NEWS_ALL_KEYWORD_LIST 
									(
										WORD_MORPHEME, WORD_CLASS, MEDIA_CODE, MINING_OBJ, NEWS_NO, UPDATE_DATE
									) 
									VALUES (
										"{word[0]}", "{word[1]}", "{media_code}", "3", "{news_no}", NOW()
									)
								""")

								cursor.execute(f"""
									SELECT 
										WORD_NO
									FROM 
										TBL_NEWS_KEYWORD_LIST
									WHERE
										WORD_MORPHEME = "{word[0]}"
								""")
								word_no = cursor.fetchall()
								word_no = word_no[0][0]

								cursor.execute(f"""
									INSERT IGNORE INTO TBL_NEWS_KEYWORD_MAP 
									(
										WORD_ORIGIN, WORD_MORPHEME,
										NEWS_NO, WORD_COUNT, WORD_NO
									) 
									VALUES (
										"{origin_word}", "{word[0]}",
										"{news_no}", 1, "{word_no}"
									)
								""")
								# time.sleep(0.1)
								print(f'**** : [{out_idx}/{len(mining_result_data) -1}][{news_no}][{idx}/{len(data_list) - 1}][{origin_word}][{in_idx}/{len(data[1]) -1}] >> {word[0]} / {word[1]} / KEYWORD 추가 및 뉴스 매핑 완료!')
					except Exception as e :
						print(f'****** + error! >> {e} >>>>> [{idx} // {len(data_list) - 1}] >> 안쪽 오류!')
						continue
					finally : 
						print('-'*50)
						print(f'***** : [{out_idx}/{len(mining_result_data) -1}][{idx}/{len(data_list) - 1}][{news_no}] >> 분석 / INSERT 완료')
				# 형태소 단어 사용 수 및 치환된 뉴스 요약, 뉴스 본문 UPDATE
				try : 
					cursor.execute(f"""
						UPDATE 
							TBL_TOTAL_CAR_NEWS_LIST
						SET 
							TITLE_MINING_STATUS = 3, 
							TITLE_MINING_DATE = NOW()
						WHERE 
							NEWS_NO = {news_no}
					""")
				except Exception as e :
					print(f'****** + error! >> {e} >>>>> [{data_list[1]}][상태 업데이트 오류]')
				finally : 
					print(f'**** [{data_list[1]}] 상태 업데이트 완료!')
		except Exception as e :
			print(f'****** + error! >> {e} >>>>> [{idx} // {len(data_list) - 1}] >> 바깥쪽 오류!')
			pass
		finally : 
			pass
			print('바깥쪽 종료')


def text_mining_old(cont_type, dbconn, cursor) :
	kkma = Kkma()
	car_news_list = TblTotalCarNewsList.objects.all().filter(title_mining_status = 1)
	except_word_list = []
	except_keyword_list = []
	origin_sentence_list = []
	news_no = 0

	# print(car_news_list)
	
	# step00. 긍정, 부정 단어 사전 load >> php 배치로 대체
	# positive_keywords = []
	# negative_keywords = []
	# va_keywords = []
	# p_keywords_list = TblNewsKeywordList.objects.all().filter(positive_yn='y')
	# n_keywords_list = TblNewsKeywordList.objects.all().filter(negative_yn='y')
	# va_keywords_list = TblNewsKeywordList.objects.all().filter(word_class='VA')
	# for idx in range(len(p_keywords_list)) :
	# 	positive_keywords.append(p_keywords_list[idx].word_morpheme)
	# for idx in range(len(n_keywords_list)) :
	# 	negative_keywords.append(n_keywords_list[idx].word_morpheme)
	# for idx in range(len(va_keywords_list)) :
	# 	va_keywords.append(va_keywords_list[idx].word_morpheme)

	print(f'형태소 분석 시작 ({len(car_news_list)}건)')

	# 뉴스 제목 분석
	if cont_type == 'news' : 
		# step01. 형태소 분석 (데이터 가공)
		for idx in range(len(car_news_list)) :
		# for idx in range(3) :
			print(f'[{idx} // {len(car_news_list)}] 데이터 가공 완료')
			replace_news_title = re.sub('\,', '&#44;', re.sub('[\"\'‘“”″′]', '&#8220;', car_news_list[idx].news_title))
			re_title = regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}]+', f'{car_news_list[idx].news_title}')

			# print(f'[{idx}] >> {len(re_title)}')
			# 원 문장
			# origin_sentence_list.append(car_news_list[idx].news_summary)
			# print(re_summary)
			# print('-'*50)
			in_result_data = []
		# in_result_data[0] 각종 카운트 사전
			etc_info_dic = {}
			# 형태소 단어 총 개수
			etc_info_dic['morpheme_count'] = len(re_title)
			# 형용사 개수
			va_count = 0
			etc_info_dic['va_count'] = va_count
			# 긍정단어 개수
			p_count = 0
			etc_info_dic['positive_count'] = p_count
			# 부정단어 개수
			n_count = 0
			etc_info_dic['negative_count'] = n_count
			# 미디어 코드
			etc_info_dic['media_code'] = car_news_list[idx].media_code
			
			in_result_data.append(etc_info_dic)
		# in_result_data[1] 뉴스 번호
			in_result_data.append(car_news_list[idx].news_no)
			# 뉴스 타이틀
			for word in re_title :
				in_result_word = []	
				group = []
				if (word not in except_word_list) :
					word_g = []
					word_g.append(word)
					group.append(word_g)
					for keyword in kkma.pos(word) :
						if (keyword not in except_keyword_list) :
							in_result_word.append(keyword)
					group.append(in_result_word)
				
				in_result_data.append(group)
			
			in_result_data[0]['re_title'] = replace_news_title
			mining_result_data.append(in_result_data)
		# print(mining_result_data)

		# step02. DB Insert
		print('DB Insert')
		try : 
			for out_idx, data_list in enumerate(mining_result_data) :
				media_code = data_list[0].get('media_code')
				print('미디어코드 = ', media_code)
				for idx, data in enumerate(data_list) :
					try : 
						if idx > 1 : 
							news_no = data_list[1]
							origin_word = re.sub('[-=.#/?:$}\"\']', '', str(data[0])).replace('[','').replace(']','')
							print(f'*** : [{out_idx}/{len(mining_result_data) -1}][{news_no}][{idx}/{len(data_list)}][{origin_word}]')
							# data[1] 형태소 분석 (세트) >> ex) [('신', 'NNG'), ('차', 'NNG')]
							for in_idx, word in enumerate(data[1]) :
								# INSERT
								cursor.execute(f"""
									INSERT IGNORE INTO TBL_NEWS_KEYWORD_LIST 
									(
										WORD_MORPHEME, WORD_CLASS, UPDATE_DATE
									) 
									VALUES (
										"{word[0]}", "{word[1]}", NOW()
									)
								""")

								cursor.execute(f"""
									INSERT INTO TBL_NEWS_ALL_KEYWORD_LIST 
									(
										WORD_MORPHEME, WORD_CLASS, MEDIA_CODE, MINING_OBJ, NEWS_NO, UPDATE_DATE
									) 
									VALUES (
										"{word[0]}", "{word[1]}", "{media_code}", "3", "{news_no}", NOW()
									)
								""")

								cursor.execute(f"""
									SELECT 
										WORD_NO
									FROM 
										TBL_NEWS_KEYWORD_LIST
									WHERE
										WORD_MORPHEME = "{word[0]}"
								""")
								word_no = cursor.fetchall()
								word_no = word_no[0][0]

								cursor.execute(f"""
									INSERT IGNORE INTO TBL_NEWS_KEYWORD_MAP 
									(
										WORD_ORIGIN, WORD_MORPHEME,
										NEWS_NO, WORD_COUNT, WORD_NO
									) 
									VALUES (
										"{origin_word}", "{word[0]}",
										"{news_no}", 1, "{word_no}"
									)
								""")
								# time.sleep(0.1)
								print(f'**** : [{out_idx}/{len(mining_result_data) -1}][{news_no}][{idx}/{len(data_list) - 1}][{origin_word}][{in_idx}/{len(data[1]) -1}] >> {word[0]} / {word[1]} / KEYWORD 추가 및 뉴스 매핑 완료!')
					except Exception as e :
						print(f'****** + error! >> {e} >>>>> [{idx} // {len(data_list) - 1}] >> 안쪽 오류!')
						continue
					finally : 
						print('-'*50)
						print(f'***** : [{out_idx}/{len(mining_result_data) -1}][{idx}/{len(data_list) - 1}][{news_no}] >> 분석 / INSERT 완료')
				# 형태소 단어 사용 수 및 치환된 뉴스 요약, 뉴스 본문 UPDATE
				try : 
					cursor.execute(f"""
						UPDATE 
							TBL_TOTAL_CAR_NEWS_LIST
						SET 
							TITLE_MINING_STATUS = 3, 
							TITLE_MINING_DATE = NOW()
						WHERE 
							NEWS_NO = {news_no}
					""")
				except Exception as e :
					print(f'****** + error! >> {e} >>>>> [{data_list[1]}][상태 업데이트 오류]')
				finally : 
					print(f'**** [{data_list[1]}] 상태 업데이트 완료!')
		except Exception as e :
			print(f'****** + error! >> {e} >>>>> [{idx} // {len(data_list) - 1}] >> 바깥쪽 오류!')
			pass
		finally : 
			pass
			print('바깥쪽 종료')

	
def run_text_mining() :
	now = time.localtime()
	start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	text_mining('news', dbconn, cursor)
	# text_mining('youtube_comments', dbconn, cursor)

	dbconn.commit()
	dbconn.close()

	now = time.localtime()
	end_time = now
	print('ㅡ'*50)
	print('뉴스 제목 분석 DB Commit/Close 완료!')
	print('뉴스 제목 분석 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('뉴스 제목 분석 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))


if __name__ == '__main__' : 
	run_text_mining()
	# test_mining('K5 이제부터 업그레이드 된다-~K7 3세대(NQ)  111대')

	# test_code()

	# news = '안녕하세요.'
	# wc.generate(news)
	# wc.to_file(f'{DATA_DIR}\\wordclouds\\filename.png')
