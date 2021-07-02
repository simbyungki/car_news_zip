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

def get_chat_message_list() : 
	excel_path = '../data/youtube_live_chats/check_20210126_live_chat.xlsx'
	df = pd.read_excel(excel_path, usecols='A:C')

	chat_list = []
	
	for row in df.values :
		temp_dict = {}
		temp_dict['registed_date'] = row[0]
		temp_dict['register'] = row[1]
		temp_dict['message'] = row[2]
		chat_list.append(temp_dict)

	return chat_list

def get_keywords(chat_list) :
	kkma = Kkma()
	# print(len(chat_list))
	except_word_list = []
	except_keyword_list = []
	in_result_data = []

	print('형태소 분석 시작!')
	for idx in range(len(chat_list)) :
		# if idx < 10 :
		# print(chat_list[idx].get('message'))
		replace_chat_message = re.sub('\,', '&#44;', re.sub('[\"\'‘“”″′]', '&#8220;', str(chat_list[idx].get('message'))))
		result_message = regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}|\d+]+', f'{replace_chat_message}')

		for word in result_message :
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
		# print(f'[{idx} // {len(chat_list)}] 데이터 가공 완료')


	return in_result_data

def export_xlsx(result_data) : 
	print(f'형태소 분석 후, 저장 중 {len(result_data)}건')
	for result in result_data : 
		for word in result[1] : 
			if (word[1] == 'NNG' or word[1] == 'NNP' or word[1] == 'NP' or word[1] == 'VV' or word[1] == 'VA') and (len(word[0]) > 1) :
				tag = ''
				if word[1] == 'NNG' or word[1] == 'NNP' or word[1] == 'NP' :
					tag = '명사, 대명사'
				elif word[1] == 'VV' : 
					tag = '동사'
				elif word[1] == 'VA' : 
					tag = '형용사'
				data2 = {'형태소 단어' : [word[0]], '품사 태그': tag}
				result = pd.DataFrame(data2)
				result.to_csv(f'C:/Users/PC/Documents/simbyungki/git/car_news_zip/data/contact/total_list.csv', mode='a', header=False, encoding='utf-8-sig')
	print(f'형태소 분석 후, 파일 저장 완료!')

def db_to_csv() : 
	dbconn2 = pymssql.connect(host=db_infos2.get('host'), user=db_infos2.get('user'), password=db_infos2.get('password'), database=db_infos2.get('database'), port=db_infos2.get('port'), charset='utf8')
	cursor2 = dbconn2.cursor()

	qna_list = []

	cursor2.execute(f"""
		SELECT 
			QNA_NO, QUEST_TITLE, QUEST_CONTENTS, ANSWER_CONTENTS, ADD_DATE, ANSWER_ID, ANSWER_DATE
		FROM 
			TBL_QNA_LIST
		WHERE 
			STATUS = 1 AND IS_ANSWER = 3
		ORDER BY 
			ADD_DATE DESC
	""")
	rows = cursor2.fetchall()


	for idx, row in enumerate(rows) :
		group = []
		row01 = ''
		row02 = ''
		row03 = ''
		row05 = ''
		if row[1] is not None :
			row01 = row[1].encode('ISO-8859-1').decode('euc-kr', 'ignore').strip()
		if row[2] is not None :
			row02 = row[2].encode('ISO-8859-1').decode('euc-kr', 'ignore').strip()
		if row[3] is not None :
			row03 = row[3].encode('ISO-8859-1').decode('euc-kr', 'ignore').strip()
		if row[5] is not None :
			row05 = row[5].encode('ISO-8859-1').decode('euc-kr', 'ignore')

		group.append(row[0])
		group.append(row01)
		group.append(row02)
		group.append(row03)
		group.append(row[4])
		group.append(row05)
		group.append(row[6])

		qna_list.append(group)

	cursor2.close()
	dbconn2.close()

	print(len(qna_list))

	for qna in qna_list :
		# QNA_NO, QUEST_TITLE, QUEST_CONTENTS, ANSWER_CONTENTS, ADD_DATE, ANSWER_ID, ANSWER_DATE
		data2 = {'QNA_NO' : qna[0], 'q_title': qna[1], 'q_content': qna[2], 'a_content': qna[3], 'q_date': qna[4], 'manager': qna[5], 'a_date': qna[6]}
		result = pd.DataFrame(data2, index = [0])
		result.to_csv(f'C:/Users/PC/Documents/simbyungki/git/car_news_zip/data/contact/qna_total_list_210702.csv', mode='a', header=False, encoding='utf-8-sig')
	print(f'파일 저장 완료!')

	return qna_list

def isNaN(num):
    return num != num




# 문장 테스트
def sentence_test_old(sentence) :
	positive_keywords = TblNewsKeywordList.objects.all().filter(positive_yn='Y')
	negative_keywords = TblNewsKeywordList.objects.all().filter(negative_yn='Y')
	in_negative_keywords = []
	in_positive_keywords = []

	for keywords in positive_keywords :
		if keywords.word_morpheme in sentence :
			# print(f'긍정적인 단어 : {keywords.word_morpheme}')
			in_positive_keywords.append(keywords.word_morpheme)
	
	for keywords in negative_keywords : 
		if keywords.word_morpheme in sentence : 
			# print(f'부정적인 단어 : {keywords.word_morpheme}')
			in_negative_keywords.append(keywords.word_morpheme)
	
	print('ㅡ'* 80)
	print(f'[{sentence}]')
	print(f' ㄴ >> 긍정적인 단어 목록 : {in_positive_keywords}')
	print(f' ㄴ >> 부정적인 단어 목록 : {in_negative_keywords}')
	print(f' ㄴ 긍정적 단어가 {len(in_positive_keywords)}개 포함되어있고, 부정적 단어가 {len(in_negative_keywords)}개 포함되어있습니다.')

	if len(in_negative_keywords) == len(in_positive_keywords) :
		print(' ★  위 문장은 50% 확률로 중립적인 문장입니다.') 
	elif len(in_negative_keywords) > len(in_positive_keywords) :
		per = len(in_positive_keywords) / len(in_negative_keywords) * 100 
		result_per = round((100 - per), 2)
		print(f' ★  위 문장은 {result_per}% 확률로 부정적인 문장입니다.') 
	elif len(in_negative_keywords) < len(in_positive_keywords) :
		per = len(in_negative_keywords) / len(in_positive_keywords) * 100 
		result_per = round((100 - per), 2)
		print('/'* 50)
		print(f' ★  위 문장은 {result_per}% 확률로 긍정적인 문장입니다.') 

if __name__ == '__main__' : 
	db_to_csv()
	# export_xlsx(get_keywords(get_chat_message_list()))

	# sentence_test('오늘은 수원 SKV1모터스에서 진행되는 "세계 명차 특집" 으로 진행되는 리본쇼 입니다~')

	# kkma = Kkma()
	# print(kkma.pos('아버지가방에들어가시다'))