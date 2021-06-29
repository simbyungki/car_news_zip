#-*- coding:utf-8 -*-
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import os, json
import requests
import mysql.connector
import pymssql
import re
import regex

## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
## 장고 프로젝트를 사용할 수 있도록 환경을 구축
import django
django.setup()

from website.models import TblTotalCarNewsList, TblMemberList, TblNewsKeywordList, TblNewsKeywordMap
from xlrd import open_workbook
import time
import xlrd
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

def remove_html(sentence) :
	sentence = re.sub('(<([^>]+)>)', '', sentence)
	return sentence

def text_mining(qna_list, dbconn, cursor, dbconn2, cursor2) :
	kkma = Kkma()
	# 제외할 단어 목록
	except_word_list = []
	out_result = []

	for idx, qna in enumerate(qna_list) : 
		sentence = re.sub('[-=.#/?:$}\"\']', '', str(qna[1])).replace('[','').replace(']','')
		# 중복제거 set > list
		origin_word_list = list(dict.fromkeys(regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}|\d+]+', f'{sentence}')))
		# print(origin_word_list)
		# print('ㅡ'*50)
		
		word_no_list = []
		results = []
		for origin_word in origin_word_list :
			if (origin_word not in except_word_list) : 
				for morpheme in kkma.pos(origin_word) :
					in_result = []	
					in_result.append(origin_word)
					in_result.append(morpheme)
					results.append(in_result)

		out_result.append(results)
		# print(qna[0])
		# print(out_result[idx])

		try : 
			cursor2.execute(f"""
				UPDATE 
					TBL_QNA_LIST 
				SET 
					MINING_STATUS = 3,
					MINING_DATE = getdate()
				WHERE
					QNA_NO = {qna[0]}
			""")		
			dbconn2.commit()
		except Exception as e :
			print(f'****** + error! >> {e} >>>>> [{qna[0]} >> TBL_QNA_LIST > MINING_STATUS UPDATE 오류!]')
			continue
		finally : 
			pass
		
		print('*' * 80)
		print(f'Depth_idx1 >> [{qna[0]}] >> {sentence}')

		for depth_idx1, result in enumerate(out_result[idx]) :
			print('ㅡ' * 50)
			#[QNA_NO][바깥쪽 idx][어절 idx][형태소 idx]
			print(f'Depth_for1 >> [{qna[0]}][{idx}][{depth_idx1}] >> {result}')	
			if depth_idx1 == 0 :
				try :
					word_no_item = []
					# 대상
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
						INSERT INTO TBL_CCQ_KEYWORD_LIST 
						(
							QNA_NO, WORD_ORIGIN, WORD_MORPHEME, WORD_CLASS_CODE, WORD_CLASS, UPDATE_DATE
						) 
						VALUES (
							"{qna[0]}", "{result[0]}", "{result[1][0]}", "{result_word_class_code}", "{result[1][1]}", NOW()
						);
					""")
					cursor.execute(f"""
						SELECT AUTO_INCREMENT
						FROM information_schema.tables 
						WHERE TABLE_NAME = 'TBL_CCQ_KEYWORD_LIST' AND TABLE_SCHEMA = DATABASE();
					""")
					result_word_no = cursor.fetchone()[0]
					word_no_item.append(result[1][0])
					word_no_item.append(result_word_no)
					word_no_list.append(word_no_item)

					print(f'###### 대상 [{result[1][0]}][{result_word_class_code}][{result_word_no}]')
				except Exception as e :
					print(f'****** + error! >> {e} >>>>> [{qna[0]} >> TBL_CCQ_KEYWORD_LIST > KEYWORD INSERT 오류!]')
					continue
				finally : 
					pass	

			for depth_idx2, result2 in enumerate(out_result[idx]) :
				if depth_idx1 != depth_idx2 :
# 1. TBL_CCQ_KEYWORD_LIST 테이블에 형태소 분석 단어 인서트 (단어사전)
	# 1-1. TBL_ANAL_WORD_CLASS에서 품사 코드 SELECT			
					if depth_idx1 == 0 :	
						word_no_item = []
						try :
							# 타겟
							cursor.execute(f"""
								SELECT 
									WORD_CLASS_CODE
								FROM 
									TBL_ANAL_WORD_CLASS 
								WHERE 
									CLASS_NAME = "{result2[1][1]}"
							""")
							result_word_class_code2 = cursor.fetchall()[0][0]
							cursor.execute(f"""
								INSERT INTO TBL_CCQ_KEYWORD_LIST 
								(
									QNA_NO, WORD_ORIGIN, WORD_MORPHEME, WORD_CLASS_CODE, WORD_CLASS, UPDATE_DATE
								) 
								VALUES (
									"{qna[0]}", "{result2[0]}", "{result2[1][0]}", "{result_word_class_code}", "{result2[1][1]}", NOW()
								);
							""")
							cursor.execute(f"""
								SELECT AUTO_INCREMENT
								FROM information_schema.tables 
								WHERE TABLE_NAME = 'TBL_CCQ_KEYWORD_LIST' AND TABLE_SCHEMA = DATABASE();
							""")
							result_word_no2 = cursor.fetchone()[0]
							# print(f'###### 타겟 [{result2[1][0]}][{result_word_class_code2}][{result_word_no2}]')

							word_no_item.append(result2[1][0])
							word_no_item.append(result_word_no2)
							word_no_list.append(word_no_item)
							
						except Exception as e :
							print(f'****** + error! >> {e} >>>>> [{qna[0]} >> TBL_CCQ_KEYWORD_LIST > KEYWORD INSERT 오류!]')
							continue
						finally : 
							pass		
							
# 2. TBL_CCQ_KEYWORD_MAP 테이블에서 4가지 조건 동일한 데이터 SELECT
# 2-1. 명사 조건 1,2,3,4,6  8(형용사 추가 시) = or result[1][1] == 'VA'
					if (result[1][1] == 'NNG' or result[1][1] == 'NNP' or result[1][1] == 'NNB' or result[1][1] == 'NNM') and (result2[1][1] == 'NNG' or result2[1][1] == 'NNP' or result2[1][1] == 'NNB' or result2[1][1] == 'NNM') and (len(result[1][0]) > 1 and len(result2[1][0]) > 1): 
						#[QNA_NO][바깥쪽 idx][어절 idx][형태소 idx]
						print(f'Depth_for2 >> [{qna[0]}][{idx}][{depth_idx1}][{depth_idx2}] >> [{result[0]}/{result[1][0]}][{result2[0]}/{result2[1][0]}]')
						# print(f'2번 조건 통과 >> [{result[1][1]}][{result2[1][1]}]')
						# print(f'Depth_for2 >> [{result[1][1]}][{result2[1][1]}]')
						try : 
							rows = []
							if result[0] != result2[0] and result[1][0] != result2[1][0] :
								cursor.execute(f"""
									SELECT 
										MAP_NO, WORD_DISTANCE
									FROM 
										TBL_CCQ_KEYWORD_MAP
									WHERE 
										(
											SOURCE_WORD = "{result[0]}" AND 
											SOURCE_MORPHEME_WORD = "{result[1][0]}" AND 
											TARGET_WORD = "{result2[0]}" AND 
											TARGET_MORPHEME_WORD = "{result2[1][0]}"
										)
										OR
										(
											SOURCE_WORD = "{result2[0]}" AND 
											SOURCE_MORPHEME_WORD = "{result2[1][0]}" AND 
											TARGET_WORD = "{result[0]}" AND 
											TARGET_MORPHEME_WORD = "{result[1][0]}"
										)
								""")
								rows = cursor.fetchall()
						except Exception as e :
							print(f'****** + error! >> {e} >>>>> [{qna[0]} >> TBL_CCQ_KEYWORD_MAP > SELECT 오류!]')
							continue
						finally : 
							pass 

# 3. TBL_CCQ_KEYWORD_MAP 테이블에서 4가지 조건 동일한 데이터가 있으면 WORD_DISTANCE 1더해서 업데이트 
							if len(rows) > 0 : 
								# print('@@ 3번 프로세스 @@ TBL_CCQ_KEYWORD_MAP 중복되는 것 있다 > 업데이트')
								return_datas = {}
								for row_idx, row in enumerate(rows) :
									return_datas['map_no'] = int(row[0])
									return_datas['distance'] = int(row[1])
								# print(f'@@ 3번 프로세스 @@ 업데이트 전 데이터 확인! {return_datas}')
								try : 
									cursor.execute(f"""
										UPDATE
											TBL_CCQ_KEYWORD_MAP 
										SET
											WORD_DISTANCE = {return_datas.get('distance') + 1}
										WHERE 
											MAP_NO = {return_datas.get('map_no')}
									""")
								except Exception as e :
									print(f'****** + error! >> {e} >>>>> [{qna[0]} >> TBL_CCQ_KEYWORD_MAP > UPDATE 오류!]')
									continue
								finally : 
									pass
# 4. TBL_CCQ_KEYWORD_MAP 테이블에서 4가지 조건 동일한 데이터가 없으면 4가지 조건값 그대로 인서트						
							else : 
								# print('@@ 4번 프로세스 @@ TBL_CCQ_KEYWORD_MAP 중복되는 것 없다 > 인서트')
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
											CLASS_NAME = "{result2[1][1]}"
									""")
									result_word_class_code2 = cursor.fetchall()[0][0]
									result_word_class_code2 = str(result_word_class_code2) + f'-{result2[1][1]}'
									# print('조합된 class code2 = ', result_word_class_code2)
									# print('조합된 class code2 type = ', type(result_word_class_code2))
									
									result_word_no1 = 0
									result_word_no2 = 0
									for word_no_item in word_no_list :
										if word_no_item[0] == result[1][0] : 
											result_word_no1 = word_no_item[1]
										if word_no_item[0] == result2[1][0] : 
											result_word_no2 = word_no_item[1]

									##########################################################################################
									cursor.execute(f"""
										INSERT INTO 
											TBL_CCQ_KEYWORD_MAP 
											(QNA_NO, SOURCE_WORD_NO, SOURCE_WORD, SOURCE_CLASS_CODE, SOURCE_MORPHEME_WORD, TARGET_WORD_NO, TARGET_WORD, TARGET_CLASS_CODE, TARGET_MORPHEME_WORD, WORD_DISTANCE, UPDATE_DATE)
										VALUES
											("{qna[0]}", "{result_word_no1}", "{result[0]}", "{result_word_class_code1}", "{result[1][0]}", "{result_word_no2}", "{result2[0]}", "{result_word_class_code2}", "{result2[1][0]}", 1, NOW())
									""")
								except Exception as e :
									print(f'****** + error! >> {e} >>>>> [{qna[0]} >> TBL_CCQ_KEYWORD_MAP > INSERT 오류!]')
									continue
								finally : 
									pass	

def get_question_list(cursor) : 
	qna_list = []

	cursor.execute(f"""
		SELECT 
			QNA_NO, QUEST_TITLE, QUEST_CONTENTS, ANSWER_CONTENTS
		FROM 
			TBL_QNA_LIST
		WHERE 
			MINING_STATUS = 1 AND STATUS = 1 AND IS_ANSWER = 3
		ORDER BY 
			ADD_DATE DESC
	""")
	# cursor.execute(f"""
	# 	SELECT 
	# 		QNA_NO, QUEST_TITLE, QUEST_CONTENTS
	# 	FROM 
	# 		TBL_QNA_LIST
	# 	WHERE 
	# 		QNA_NO = 4110
	# """)
	rows = cursor.fetchall()

	for idx, row in enumerate(rows) :
		group = []
		if idx > 20 :
			break
		else :
			row01 = ''
			row02 = ''
			row03 = ''
			if row[1] is not None :
				row01 = row[1].encode('ISO-8859-1').decode('euc-kr', 'ignore').strip()
			if row[2] is not None :
				row02 = row[2].encode('ISO-8859-1').decode('euc-kr', 'ignore').strip()
			if row[3] is not None :
				row02 = row[3].encode('ISO-8859-1').decode('euc-kr', 'ignore').strip()

			group.append(row[0])
			group.append(remove_html(row01 + ' ' + row02 + ' ' + row03))

		qna_list.append(group)

	return qna_list





def run() : 
	now = time.localtime()
	start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	dbconn2 = pymssql.connect(host=db_infos2.get('host'), user=db_infos2.get('user'), password=db_infos2.get('password'), database=db_infos2.get('database'), port=db_infos2.get('port'))
	cursor2 = dbconn2.cursor()

	# function
	# print(get_question_list(cursor2))
	text_mining(get_question_list(cursor2), dbconn, cursor, dbconn2, cursor2)

	dbconn.commit()
	dbconn.close()

	dbconn2.commit()
	cursor2.close()

	now = time.localtime()
	end_time = now
	print('ㅡ'*50)
	print('상담 내용 DB Commit/Close 완료!')
	print('상담 내용 분석 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('상담 내용 분석 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))


if __name__ == "__main__" : 
	run()