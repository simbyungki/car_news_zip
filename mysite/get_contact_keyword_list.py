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


def get_question_list(dbconn, cursor) : 
	qna_list = []
	cursor.execute(f"""
		SELECT 
			QNA_NO, QUEST_TITLE, QUEST_CONTENTS
		FROM 
			TBL_QNA_LIST
		WHERE 
			STATUS = 1 AND IS_ANSWER = 3
		ORDER BY 
			ADD_DATE DESC
	""")
	rows = cursor.fetchall()

	for idx, row in enumerate(rows) :
		group = []
		if idx > 3 :
			break
		else :
			row01 = ''
			row02 = ''
			if row[1] is not None :
				row01 = row[1].encode('ISO-8859-1').decode('euc-kr', 'ignore').strip()
			if row[2] is not None :
				row02 = row[2].encode('ISO-8859-1').decode('euc-kr', 'ignore').strip()

			group.append(row[0])
			group.append(remove_html(row01 + ' ' + row02))

		qna_list.append(group)

	return qna_list

def text_mining(qna_list, dbconn, cursor) :
	kkma = Kkma()
	# 제외할 단어 목록
	except_word_list = []
	out_result = []
	
	for idx, qna in enumerate(qna_list) : 
		sentence = re.sub('[-=.#/?:$}\"\']', '', str(qna[1])).replace('[','').replace(']','')
		origin_word_list = regex.findall(r'[\p{Hangul}|\p{Han}]+', f'{sentence}')

		# print(origin_word_list)

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

		for result in out_result[idx] :
			print(result)
			try : 
				pass
				# print(result)
				# cursor.execute(f"""
				# 	INSERT INTO TBL_CCQ_KEYWORD_LIST 
				# 	(
				# 		QNA_NO, WORD_ORIGIN, WORD_MORPHEME, WORD_CLASS, UPDATE_DATE
				# 	) 
				# 	VALUES (
				# 		"{qna[0]}", "{result[0]}", "{result[1][0]}", "{result[1][1]}", NOW()
				# 	)
				# """)
			
			except Exception as e :
				print(f'****** + error! >> {e} >>>>> [{qna[0]} >> 오류!]')
				continue
			finally : 
				print('-'*50)
				print(f'***** : [{qna[0]} >> 분석 / INSERT 완료')

			

	
def run_text_mining() :
	now = time.localtime()
	start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	dbconn2 = pymssql.connect(host=db_infos2.get('host'), user=db_infos2.get('user'), password=db_infos2.get('password'), database=db_infos2.get('database'), port=db_infos2.get('port'))
	cursor2 = dbconn2.cursor()

	text_mining(get_question_list(dbconn2, cursor2), dbconn, cursor)

	dbconn.commit()
	dbconn.close()

	now = time.localtime()
	end_time = now
	print('ㅡ'*50)
	print('상담 내용 DB Commit/Close 완료!')
	print('상담 내용 분석 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('상담 내용 분석 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))





if __name__ == '__main__' : 
	run_text_mining()