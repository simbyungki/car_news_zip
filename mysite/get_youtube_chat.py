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

# https://developers.google.com/youtube/v3/docs
# AUTOPLUS# >> AP ADMIN KEY
# DEVELOPER_KEY = 'AIzaSyCHnGrLBzQJk3IvA-lhVRgfia5QUAIPb9k'
# REBORN#
# DEVELOPER_KEY = 'AIzaSyBdTgUi0BB1A6OYqQBP4jGrUfDkVTk00Dc'
# BK#
# DEVELOPER_KEY = 'AIzaSyA2AZ0G5sRKq3uDTa_KzDT2X0oJ9rdcZWk'
# KING BK#
DEVELOPER_KEY = 'AIzaSyB08WDZOdnWGqfcDKl4FB30LIRJzQS7JCQ'
# MIN
# DEVELOPER_KEY = 'AIzaSyBH8G4-tsgT4ooV3uKUQqOUTbSu3HckrEU'
# YOON IRENE#
# DEVELOPER_KEY = 'AIzaSyDGotx2KiS3f-nmLgoq2h_ok_xYaZN-BHs'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath('./mysite'))
# SECURITY WARNING: keep the secret key used in production secret!
db_info_file = os.path.join(BASE_DIR, 'db_conn.json')
with open(db_info_file) as f :
	db_infos = json.loads(f.read())


def get_chat_message_list() : 
	excel_path = '../data/youtube_live_chats/check_20210202_live_chat.xlsx'
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
			data2 = {'형태소 단어' : [word[0]], '품사 태그': [word[1]]}
			result = pd.DataFrame(data2)
			result.to_csv(f'C:/Users/PC/Documents/simbyungki/git/car_news_zip/data/youtube_live_chats/after_check_20210202_live_chat.csv', mode='a', header=False, encoding='utf-8-sig')
	print(f'형태소 분석 후, 파일 저장 완료!')


# 문장 테스트
def sentence_test(sentence) :
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
	# export_xlsx(get_keywords(get_chat_message_list()))

	sentence_test('정답 올려주세요! 추첨결과는 방송 끝나고 말씀 드립니다! 끝까지 함께 해주세요~!')

	# kkma = Kkma()
	# print(kkma.pos('아버지가방에들어가시다'))