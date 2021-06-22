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

import time
from datetime import datetime
from konlpy.tag import Kkma

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







# 1. QNA LIST 질문 내용 load ( 문장 띄어쓰기 제거 후 붙이기)
# 2. bi그램 (2gram)
# 3. DB저장 (QNA LIST > 2그램 테이블)


def remove_html(sentence) :
	sentence = re.sub('(<([^>]+)>)', '', sentence)
	return sentence

def get_question_list(cursor) : 
	q_list = []

	cursor.execute(f"""
		SELECT 
			QNA_NO, QUEST_TITLE, QUEST_CONTENTS
		FROM 
			TBL_QNA_LIST
		WHERE 
			MINING_STATUS = 3 AND STATUS = 1 AND IS_ANSWER = 3
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
		if idx > 1 : 
			break
		else : 
			group = []
			row01 = ''
			row02 = ''
			if row[1] is not None :
				row01 = row[1].encode('ISO-8859-1').decode('euc-kr', 'ignore').strip()
			if row[2] is not None :
				row02 = row[2].encode('ISO-8859-1').decode('euc-kr', 'ignore').strip()

			group.append(row[0])
			# group.append(remove_html(row01 + ' ' + row02))
			if row02 != '' :
				group.append(row02)

			q_list.append(group)

	return q_list


def insert_db_2gram(result) : 
	# DB MAP INSERT
	for idx, item in enumerate(result) : 
		try : 
			# INSERT
			cursor.execute(f"""
				INSERT IGNORE INTO TBL_CCQ_BIGRAM_MAP 
				(
					QNA_NO, Q_CATEGORY, BIGRAMS, UPDATE_DATE
				) 
				VALUES (
					"{item[0]}", 0, "{item[1]}",NOW()
				)
			""")
			print(f'**** : [{idx}/{len(result) -1}] QNA <-> bigram MAP 완료!')
		except Exception as e :
			print(f'****** + error! >> {e} >>>>> [{item[0]}] >> INSERT 오류!')
			continue
		finally : 
			print('-'*50)
	
	print(f'***** : QNA LIST > BIGRAM > DB INSERT 완료')

def sentence_to_2gram(q_list) : 
	result = []
	for idx, question in enumerate(q_list) :
		result_item = []
		result_str = ''
		result_item.append(question[0])
		result_sentence = remove_html(question[1].replace(' ', '').replace('\r', '').replace('\n', '').replace(' ', '').replace('.', ''))
		for depth1_idx, q in enumerate(result_sentence) : 
			if depth1_idx < (len(result_sentence) - 1) :	
				result_str += f'{q}{result_sentence[depth1_idx+1]}/'
		result_item.append(result_str[:-1])
		result.append(result_item)

	return result

	# bigram된 데이터 불러온 후 list로 변경
	# print(result[1][1].split('/'))

def compare_sentence(q_list, cursor) : 
	cursor.execute(f"""
		SELECT 
			Q_CATEGORY, BIGRAMS 
		FROM 
			TBL_CCQ_BIGRAM_MAP
	""")
	rows = cursor.fetchall()
	source_bigram_list = []
	for idx, row in enumerate(rows) :
		in_group = []
		in_group.append(row[0])
		in_group.append(list(dict.fromkeys(row[1].split('/'))))
		source_bigram_list.append(in_group)
	# print(source_bigram_list)
	
	q_list = sentence_to_2gram(q_list)
	len_q_list_gram = len(q_list[0][1].split('/'))
	fin_result = []
	for target_question in q_list : 
		target_bigrams = target_question[1].split('/')
		# print(target_bigrams)
		for source_bigrams in source_bigram_list : 
			same_count = 0
			# print(source_bigrams)
			# print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ'*5)
			grams = []
			for target_bigram in target_bigrams : 
				for source_bigram in source_bigrams[1] : 
					group = []
					if target_bigram == source_bigram :
						grams.append(target_bigram)
						# q category = source_bigrams[0]
						group.append(source_bigrams[0])
						same_count += 1
						group.append(same_count)
						group.append(grams)
						# print(group)
						fin_result.append(group)
						# print(f'[일치] {source_bigrams[0]} // {source_bigram}')

	max = 0
	score_list = []
	for result in fin_result :
		group = []
		if max < result[1] :
			max = result[1]
			group.append(result[0])
			group.append(max)
			group.append(result[2])
			score_list.append(group)


	for score in score_list : 
		print('ㅡ'* 70)
		q_type = ''
		if score[0] == 1 : 
			q_type = '일반, 차량 구매 관련 문의'
		elif score[0] == 2 :
			q_type = '출고 옵션 관련 문의'
		elif score[0] == 3 :
			q_type = '차량 직접 볼 수 있는지? 시승 가능 여부 문의'
		elif score[0] == 4 :
			q_type = '오프라인 구입 후 온라인 구매 이력 등록 요청'
		elif score[0] == 5 :
			q_type = '탁송비, 배송비 문의'
		elif score[0] == 6 :
			q_type = '서비스 문의 (찾케서, 포인트 등)'
		elif score[0] == 7 :
			q_type = '네고 가능 여부 문의'
		elif score[0] == 8 :
			q_type = '차량 추천 문의'
		elif score[0] == 9 :
			q_type = '차량업체 제휴 문의'
		elif score[0] == 10 :
			q_type = '기존 이력 문의'
		elif score[0] == 11 :
			q_type = '지점 위치 문의'
		elif score[0] == 12 :
			q_type = '현금영수증 관련 문의'
		elif score[0] == 13 :
			q_type = '리스 문의'
		elif score[0] == 14 :
			q_type = '환불 문의'
		elif score[0] == 15 :
			q_type = '렌트 문의'
		elif score[0] == 16 :
			q_type = '홈페이지 기능 문의 (회원정보 등)'
		elif score[0] == 17 :
			q_type = '계약중인 차량 문의'
		elif score[0] == 18 :
			q_type = '복합 문의'
		elif score[0] == 19 :
			q_type = '회원 탈퇴 문의'
		elif score[0] == 20 :
			q_type = '사고 이력 관련 문의'
		elif score[0] == 21 :
			q_type = '차량 매입, 대차 문의'
		elif score[0] == 23 :
			q_type = '준비중인 차량 문의'
		elif score[0] == 25 :
			q_type = '할부 문의'
		elif score[0] == 27 :
			q_type = '결제관련 문의'

		# print(f'\n[{q_type} ({round((score[1]/len_q_list_gram)* 100, 2)}% 확률), ({score[1]}/{len_q_list_gram})] \n')
		print(f'\n\n[{q_type} ({round((score[1]/len_q_list_gram)* 100, 2)}% 확률), ({score[1]}/{len_q_list_gram})] \n\n일치하는 gram 목록 : {score[2]}')
	
	print('ㅡ'* 70)


def mining_sentence(q_list, cursor) :
	kkma = Kkma()
	# 제외할 단어 목록
	except_word_list = []
	fin_result = []
	
	for idx, q in enumerate(q_list) : 
		question = [q[0], remove_html(q[1])]
		sentence = re.sub('[-=.#/?:$}\"\']', '', str(question[1])).replace('[','').replace(']','')
		origin_word_list = list(dict.fromkeys(regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}|\d+]+', f'{sentence}')))
		out_result = []
		out_result.append(question[0])
		result = []
		for origin_word in origin_word_list :
			if (origin_word not in except_word_list) : 
				for morpheme in kkma.pos(origin_word) :	
					in_result = []	
					in_result.append(origin_word)
					in_result.append(morpheme[0])
					result.append(in_result)
		out_result.append(result)
		fin_result.append(out_result)

	print(fin_result)



if __name__ == '__main__' : 

	
	# now = time.localtime()
	# start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	dbconn2 = pymssql.connect(host=db_infos2.get('host'), user=db_infos2.get('user'), password=db_infos2.get('password'), database=db_infos2.get('database'), port=db_infos2.get('port'))
	cursor2 = dbconn2.cursor()

	# compare_sentence([[0, 'K5차량 상담 신청합니다. 연락주세요~']], cursor)
	mining_sentence(get_question_list(cursor2), cursor)
	# print(sentence_to_2gram(get_question_list(cursor2)))
	# insert_db_2gram(sentence_to_2gram(get_question_list(cursor2)))

	# dbconn.commit()
	# dbconn.close()

	# dbconn2.commit()
	# cursor2.close()

	# now = time.localtime()
	# end_time = now
	# print('ㅡ'*50)
	# print('상담 내용 DB Commit/Close 완료!')
	# print('상담 내용 분석 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	# print('상담 내용 분석 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))


