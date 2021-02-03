#-*- coding: utf-8 -*-
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


def classification(dbconn, cursor) :
	# 긍정, 부정 단어 사전 load
	positive_keywords = []
	negative_keywords = []
	va_keywords = []
	p_keywords_list = TblNewsKeywordList.objects.all().filter(positive_yn='y')
	n_keywords_list = TblNewsKeywordList.objects.all().filter(negative_yn='y')
	for idx in range(len(p_keywords_list)) :
		positive_keywords.append(p_keywords_list[idx].word_morpheme)
	for idx in range(len(n_keywords_list)) :
		negative_keywords.append(n_keywords_list[idx].word_morpheme)

	in_query = ""
	for idx, p_keywords in enumerate(positive_keywords[:5]) :
		if idx == 0 :
			in_query = f"REPLACE(NEWS_SUMMARY, '{p_keywords}', '<span style=\"color:#2944cc\">{p_keywords}</span>')"
		else :
			in_query = f"REPLACE({in_query}, '{p_keywords}', '<span style=\"color:#2944cc\">{p_keywords}</span>')"



	
		cursor.execute(f"""
			SELECT R1.* FROM (
				SELECT 
					NEWS_SUMMARY, {in_query}
				FROM 
					TBL_TOTAL_CAR_NEWS_LIST
				WHERE 
					NEWS_SUMMARY LIKE '%{p_keywords}%'
				) R1
			LIMIT 0, 5
		""")

		rows = cursor.fetchall()
		print(rows)



def run_classification() :
	now = time.localtime()
	start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	classification(dbconn, cursor)

	dbconn.commit()
	cursor.close()
	dbconn.close()

	now = time.localtime()
	end_time = now
	print('ㅡ'*50)
	print('뉴스 요약 내용 분류 DB Commit/Close 완료!')
	print('뉴스 요약 내용 분류 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('뉴스 요약 내용 분류 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))


if __name__ == '__main__' : 
	run_classification()