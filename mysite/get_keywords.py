import requests
import time
import schedule
import re
import regex
import mysql.connector
import os, json
import traceback
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
## 장고 프로젝트를 사용할 수 있도록 환경을 구축
import django
django.setup()

from website.models import TblTotalCarNewsList, TblMemberList, TblNewsKeywordList, TblNewsKeywordMap
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
with open(db_info_file) as f :
	db_infos = json.loads(f.read())

# 뉴스 분석
mining_result_data = []
def text_mining(cont_type, dbconn, cursor) :
	kkma = Kkma()
	car_news_list = TblTotalCarNewsList.objects.all().filter(mining_status=1).exclude(news_content = '')
	except_word_list = []
	except_keyword_list = []
	origin_sentence_list = []
	news_no = 0
	# user_id = request.session.get('user')
	# if user_id :
	# 	memb_name = TblMemberList.objects.filter(memb_id=user_id).values()[0].get('memb_name')
	# 	context['user'] = memb_name
	# else : 
	# 	context['user'] = None

	# print(car_news_list[0].news_summary)

	print('형태소 분석')

	# step00. 긍정, 부정 단어 사전 load
	positive_keywords = []
	negative_keywords = []
	va_keywords = []
	p_keywords_list = TblNewsKeywordList.objects.all().filter(positive_yn='y')
	n_keywords_list = TblNewsKeywordList.objects.all().filter(negative_yn='y')
	va_keywords_list = TblNewsKeywordList.objects.all().filter(word_class='VA')
	for idx in range(len(p_keywords_list)) :
		positive_keywords.append(p_keywords_list[idx].word_morpheme)
	for idx in range(len(n_keywords_list)) :
		negative_keywords.append(n_keywords_list[idx].word_morpheme)
	for idx in range(len(va_keywords_list)) :
		va_keywords.append(va_keywords_list[idx].word_morpheme)

	# 뉴스 본문 분석
	if cont_type == 'news' : 
		# step01. 형태소 분석 (데이터 가공)
		for idx in range(len(car_news_list)) :
		# for idx in range(10) :
			re_content = regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}]+', f'{car_news_list[idx].news_content}')
			# print(f'[{idx}] >> {len(re_content)}')
			origin_sentence_list.append(car_news_list[idx].news_summary)
			# print(re_summary)
			# print('-'*50)
			in_result_data = []
		# in_result_data[0] 각종 카운트 사전
			count_dic = {}
			# 형태소 단어 총 개수
			count_dic['morpheme_count'] = len(re_content)
			# 형용사 개수
			va_count = 0
			count_dic['va_count'] = va_count
			# 긍정단어 개수
			p_count = 0
			count_dic['positive_count'] = p_count
			# 부정단어 개수
			n_count = 0
			count_dic['negative_count'] = n_count
			
			in_result_data.append(count_dic)
		# in_result_data[1] 뉴스 번호
			in_result_data.append(car_news_list[idx].news_no)
			for word in re_content :
				in_result_word = []	
				group = []
				if (word not in except_word_list) :
					word_g = []
					word_g.append(word)
					group.append(word_g)
					# print(word)
					# print('-'*50)
					for keyword in kkma.pos(word) :
						if (keyword not in except_keyword_list) :
							# print(keyword)
							# print('-'*50)
							in_result_word.append(keyword)
					group.append(in_result_word)
				
				if (word in positive_keywords) :
					p_count += 1
				if (word in negative_keywords) :
					n_count += 1
				if (word in va_keywords) :
					va_count += 1

				in_result_data.append(group)
			in_result_data[0]['positive_count'] = p_count
			in_result_data[0]['negative_count'] = n_count
			in_result_data[0]['va_count'] = va_count
			mining_result_data.append(in_result_data)

		# step02. DB Insert
		print('DB Insert')
		try : 
			for out_idx, data_list in enumerate(mining_result_data) :
				print('DB Insert 2')
				for idx, data in enumerate(data_list) :
					try : 
						if idx == 0 :
							news_info = data_list[0]
						elif idx == 1 :	
							news_no = data_list[1]
						else : 
							pass
							origin_word = re.sub('[-=.#/?:$}\"\']', '', str(data[0])).replace('[','').replace(']','')
							print(f'*** : [{out_idx}/{len(mining_result_data) -1}][{news_no}][{idx}/{len(data_list)}][{origin_word}]')
							# data[1] 형태소 분석 (세트) >> ex) [('신', 'NNG'), ('차', 'NNG')]
							for in_idx, word in enumerate(data[1]):
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
									INSERT IGNORE INTO TBL_NEWS_KEYWORD_MAP 
									(
										WORD_ORIGIN, WORD_MORPHEME,
										NEWS_NO, WORD_COUNT
									) 
									VALUES (
										"{origin_word}", "{word[0]}",
										"{news_no}", 1
									)
								""")
								print(f'**** : [{out_idx}/{len(mining_result_data) -1}][{news_no}][{idx}/{len(data_list) - 1}][{origin_word}][{in_idx}/{len(data[1]) -1}] >> {word[0]} / {word[1]} / KEYWORD 추가 및 뉴스 매핑 완료!')
								cursor.execute(f"""
									UPDATE TBL_TOTAL_CAR_NEWS_LIST
									SET MINING_STATUS = 3, MINING_DATE = NOW(), 
										POSITIVE_COUNT = {news_info["positive_count"]}, NEGATIVE_COUNT = {news_info["negative_count"]},
										VA_COUNT = {news_info["va_count"]}, MORPHEME_COUNT = {news_info["morpheme_count"]}
									WHERE NEWS_NO = {news_no}
								""")
								# time.sleep(0.1)
					except Exception as e :
						print(f'****** + error! >> {e} >>>>> [{idx} // {len(data_list) - 1}] >> 안쪽 오류!')
						pass
					finally : 
						print('-'*50)
						print(f'***** : [{out_idx}/{len(mining_result_data) -1}][{idx}/{len(data_list) - 1}][{news_no}] >> 분석 / INSERT 완료')
		except Exception as e :
			print(f'****** + error! >> {e} >>>>> [{idx} // {len(data_list) - 1}] >> 바깥쪽 오류!')
			pass
		finally : 
			pass
			print('바깥쪽 종료')

	# # 유튜브 댓글 분석
	elif cont_type == 'youtube_comments' : 
		reviews = pd.read_excel('../data/youtube_comments/쉐보레트레일블레이저_review_comments_youtube.xlsx')
		df_list = reviews.values.tolist()
		in_result_data = []

		# # step01. 형태소 분석 (데이터 가공)
		for idx in range(len(df_list)) :
			re_content = regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}]+', f'{df_list[idx][2]}')
			origin_sentence_list.append(df_list[idx][2])
			# print(re_summary)
			# print('-'*50)
			in_result_data = []
			in_result_data.append('idx')
			for word in re_content :
				in_result_word = []	
				group = []
				if (word not in except_word_list) :
					word_g = []
					word_g.append(word)
					group.append(word_g)
					# print(word)
					# print('-'*50)
					for keyword in kkma.pos(word) :
						if (keyword not in except_keyword_list) :
							# print(keyword)
							# print('-'*50)
							in_result_word.append(keyword)
					group.append(in_result_word)
				in_result_data.append(group)
			mining_result_data.append(in_result_data)
	
		# step02. DB Insert
		print(f'{len(mining_result_data)} > DB Insert')
		try : 
			for out_idx, data_list in enumerate(mining_result_data) :
				for idx, data in enumerate(data_list) :
					try : 
						origin_word = re.sub('[-=.#/?:$}\"\']', '', str(data[0])).replace('[','').replace(']','')
						print(f'*** : [{out_idx}/{len(mining_result_data) -1}][{idx}/{len(data_list) - 1}][{origin_word}]')
						for in_idx, word in enumerate(data[1]) :
							# print(f'[{word[0]}], [{word[1]}]')
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
							print(f'**** : [{out_idx}/{len(mining_result_data) -1}][{idx}/{len(data_list) - 1}][{origin_word}][{in_idx}/{len(data[1]) -1}] >> {word[0]} / {word[1]} / KEYWORD 추가 완료!')
						time.sleep(0.1)
					except Exception as e :
						print(f'****** + error! >> {e} >>>>> [{idx} // {len(data_list) - 1}] >> 안쪽 오류!')
						pass
					finally : 
						print('-'*50)
						print(f'***** : [{out_idx}/{len(mining_result_data) -1}][{idx}/{len(data_list) - 1}] >> 분석 / INSERT 완료')

		except Exception as e :
			print(f'****** + error! >> {e} >>>>> [{idx} // {len(data_list) - 1}] >> 바깥쪽 오류!')
			pass
		finally : 
			print('바깥쪽 종료')
					
					
def run_text_mining() :
	now = time.localtime()
	start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	text_mining('news', dbconn, cursor)
	# text_mining('youtube_comments', dbconn, cursor)

	dbconn.commit()
	cursor.close()
	dbconn.close()

	now = time.localtime()
	end_time = now
	print('ㅡ'*50)
	print('뉴스 상세 내용 분석 DB Commit/Close 완료!')
	print('뉴스 상세 내용 분석 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('뉴스 상세 내용 분석 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))


if __name__ == '__main__' : 
	run_text_mining()
