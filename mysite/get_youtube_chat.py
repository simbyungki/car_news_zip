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
	excel_path = '../data/youtube_live_chats/check_20201215_live_chat.xlsx'
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
				# print(data2)		
				result = pd.DataFrame(data2)
				result.to_csv(f'C:/Users/PC/Documents/simbyungki/git/car_news_zip/data/youtube_live_chats/after_check_20201215_live_chat.csv', mode='a', header=False, encoding='utf-8-sig')
	print(f'형태소 분석 후, 파일 저장 완료!')

def isNaN(num):
    return num != num

def sentence_test(sentence) : 
	excel_path = '../data/youtube_live_chats/live_chat_keyword_list.xlsx'
	# sheetname='live_chat_keyword_list'
	df = pd.read_excel(excel_path, usecols='A:C', header=1)

	chat_list = []

	for idx, row in enumerate(df.values) : 
		if idx != 0 :
			# if not (isNaN(row[0])) : 
			# if row[2] == 5 : 
			temp_dict = {}
			temp_dict['word_morpheme'] = row[0]
			tag = ''
			if row[1] == '명사, 대명사' : 
				tag = 'NN'
			elif row[1] == '동사' : 
				tag = 'VV'
			elif row[1] == '형용사' : 
				tag = 'VA'
			temp_dict['word_class'] = tag
			temp_dict['word_category'] = row[2]
			chat_list.append(temp_dict)

	# print(chat_list)

	match_list = []
	replace_sentence = re.sub('\,', '&#44;', re.sub('[\"\'‘“”″′]', '&#8220;', str(sentence)))
	result = regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}|\d+]+', f'{replace_sentence}')

	print(result)

	fin_result_data = {
		'len_nn' : 0,
		'len_vv' : 0,
		'len_va' : 0,
		'category01' : [],
		'category02' : [],
		'category03' : [],
		'category04' : [],
		'category05' : [],
		'category06' : [],
		'category07' : []
	}

	for idx, chat in enumerate(chat_list) : 
		for word in result : 
			if chat.get('word_morpheme') in word : 
				if chat.get('word_class') == 'NN' : 
					fin_result_data['len_nn'] += 1
					print(chat.get('word_morpheme'))
				elif chat.get('word_class') == 'VV' : 
					fin_result_data['len_vv'] += 1
				elif chat.get('word_class') == 'VA' : 
					fin_result_data['len_va'] += 1
			if (chat.get('word_morpheme') in word) and (chat.get('word_category') != 1) : 
				# print(f'[{type(chat.get("word_morpheme"))}]{chat.get("word_morpheme")} ///// [{type(chat.get("word_category"))}]{chat.get("word_category")}')
				match_list.append(chat)

	# if class_type == 3 :
	# 	category = '긍정'
	# elif class_type == 5 : 
	# 	category = '부정'
	# elif class_type == 6 : 
	# 	category = '지역, 지명'
	# elif class_type == 7 or class_type == 9 or class_type == 11 or class_type == 13 or class_type == 15 or class_type == 17 or class_type == 19 or class_type == 20 or class_type == 21 or class_type == 23 or class_type == 25 or class_type == 27 : 
	# 	category = '차량 관련'
	# elif class_type == 29 : 
	# 	category = '오플 관련'
	# elif class_type == 31 : 
	# 	category = '상담, 문의'

	for match_item in match_list :
		word_morpheme = match_item.get('word_morpheme')
		category = ''
		# if match_item.get('word_category') == 3 :
		# 	category = '긍정'
		# elif match_item.get('word_category') == 5 : 
		# 	category = '부정'
		# elif match_item.get('word_category') == 6 : 
		# 	category = '지명, 지역'
		# elif match_item.get('word_category') == 7 : 
		# 	category = '차량타입'
		# elif match_item.get('word_category') == 9 : 
		# 	category = '브랜드'
		# elif match_item.get('word_category') == 11 : 
		# 	category = '모델'
		# elif match_item.get('word_category') == 13 : 
		# 	category = '가격'
		# elif match_item.get('word_category') == 15 : 
		# 	category = '결제'
		# elif match_item.get('word_category') == 17 : 
		# 	category = '계약'
		# elif match_item.get('word_category') == 19 : 
		# 	category = '등급,옵션,연료
		# elif match_item.get('word_category') == 20 : 
		# 	category = '디자인'
		# elif match_item.get('word_category') == 21 : 
		# 	category = '외장'
		# elif match_item.get('word_category') == 23 : 
		# 	category = '내장
		# elif match_item.get('word_category') == 25 : 
		# 	category = '부품 / 차량 전문지식'
		# elif match_item.get('word_category') == 27 : 
		# 	category = '차량 기타'
		# elif match_item.get('word_category') == 29 : 
		# 	category = '오플 관련'
		# elif match_item.get('word_category') == 31 : 
		# 	category = '상담, 문의'		
		if match_item.get('word_category') == 3 :
			category = '긍정'
			fin_result_data['category01'].append(word_morpheme)
		elif match_item.get('word_category') == 5 : 
			category = '부정'
			fin_result_data['category02'].append(word_morpheme)
		elif match_item.get('word_category') == 6 : 
			category = '지역, 지명'
			fin_result_data['category03'].append(word_morpheme)
		elif match_item.get('word_category') == 7 or match_item.get('word_category') == 9 or match_item.get('word_category') == 11 or match_item.get('word_category') == 13 or match_item.get('word_category') == 19 or match_item.get('word_category') == 20 or match_item.get('word_category') == 21 or match_item.get('word_category') == 23 or match_item.get('word_category') == 25 or match_item.get('word_category') == 27 : 
			category = '차량 관련'
			fin_result_data['category04'].append(word_morpheme)
		elif match_item.get('word_category') == 15 or match_item.get('word_category') == 17 : 
			category = '결제, 계약'
			fin_result_data['category05'].append(word_morpheme)
		elif match_item.get('word_category') == 29 : 
			category = '오토플러스'
			fin_result_data['category06'].append(word_morpheme)
		elif match_item.get('word_category') == 31 : 
			category = '상담, 문의'
			fin_result_data['category07'].append(word_morpheme)

	print(f'위 문장은 명사 {fin_result_data["len_nn"]}개, 동사 {fin_result_data["len_vv"]}개, 형용사 {fin_result_data["len_va"]}개로 구성 되어있습니다.')
	print(f"""속해있는 단어별 구분은,
-> 긍정 {len(fin_result_data['category01'])}개 {fin_result_data['category01']}, 
-> 부정 {len(fin_result_data['category02'])}개 {fin_result_data['category02']}, 
-> 지역, 지명 관련 {len(fin_result_data['category03'])}개 {fin_result_data['category03']}, 
-> 차량 관련 {len(fin_result_data['category04'])}개 {fin_result_data['category04']}, 
-> 결제, 계약 관련 {len(fin_result_data['category05'])}개 {fin_result_data['category05']}, 
-> 오토플러스 관련 {len(fin_result_data['category06'])}개 {fin_result_data['category06']}, 
-> 상담, 문의 관련 {len(fin_result_data['category07'])}개 {fin_result_data['category07']} 입니다.""")
	
	# return chat_list
	



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
	export_xlsx(get_keywords(get_chat_message_list()))

	# sentence_test('기아의 스테디셀러 자동차, 더 뉴 모하비 지난해 준준형 스포티지 보다 더 팔렸다고 하지요~ 캠핑, 레저족의 드림카 더 뉴 모하비도 집중해주세요~')

	# kkma = Kkma()
	# print(kkma.pos('아버지가방에들어가시다'))