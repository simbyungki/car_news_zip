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
		if idx > 2 : 
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
	# print(q_list)
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
	# print(morpheme[1].split('/'))

def get_question_type(q_type) : 
	if q_type == 1 : 
		q_type = '일반, 차량 구매 관련 문의'
	elif q_type == 2 :
		q_type = '출고 옵션 관련 문의'
	elif q_type == 3 :
		q_type = '차량 직접 볼 수 있는지? 시승 가능 여부 문의'
	elif q_type == 4 :
		q_type = '오프라인 구입 후 온라인 구매 이력 등록 요청'
	elif q_type == 5 :
		q_type = '탁송비, 배송비 문의'
	elif q_type == 6 :
		q_type = '서비스 문의 (찾케서, 포인트 등)'
	elif q_type == 7 :
		q_type = '네고 가능 여부 문의'
	elif q_type == 8 :
		q_type = '차량 추천 문의'
	elif q_type == 9 :
		q_type = '차량업체 제휴 문의'
	elif q_type == 10 :
		q_type = '기존 이력 문의'
	elif q_type == 11 :
		q_type = '지점 위치 문의'
	elif q_type == 12 :
		q_type = '현금영수증 관련 문의'
	elif q_type == 13 :
		q_type = '리스 문의'
	elif q_type == 14 :
		q_type = '환불 문의'
	elif q_type == 15 :
		q_type = '렌트 문의'
	elif q_type == 16 :
		q_type = '홈페이지 기능 문의 (회원정보 등)'
	elif q_type == 17 :
		q_type = '계약중인 차량 문의'
	elif q_type == 18 :
		q_type = '복합 문의'
	elif q_type == 19 :
		q_type = '회원 탈퇴 문의'
	elif q_type == 20 :
		q_type = '사고 이력 관련 문의'
	elif q_type == 21 :
		q_type = '차량 매입, 대차 문의'
	elif q_type == 23 :
		q_type = '준비중인 차량 문의'
	elif q_type == 25 :
		q_type = '할부 문의'
	elif q_type == 27 :
		q_type = '결제관련 문의'

	return q_type

def compare_sentence(q_list, cursor) : 

	print(q_list)
	cursor.execute(f"""
		SELECT 
			Q_CATEGORY, BIGRAMS 
		FROM 
			TBL_CCQ_BIGRAM_MAP
	""")
	rows = cursor.fetchall()
	source_bigram_list = []
	for idx, row in enumerate(rows) :
		weight_keywords = ''
		if idx < 1000 : 
			in_group = []
			in_group.append(row[0])
			# in_group.append(row[1].split('/'))
			in_group.append(list(dict.fromkeys(row[1].split('/'))))
			source_bigram_list.append(in_group)
	# print(len(source_bigram_list))
	
	q_list = sentence_to_2gram(q_list)
	len_q_list_gram = len(q_list[0][1].split('/'))

	fin_result = []
	for target_question in q_list : 
		target_bigrams = target_question[1].split('/')

		weight_keywords = ''
		if target_question[0] == 2 : 
			weight_keywords = '/옵션/션문/문의/옵션/션추/추가/출고/고옵/옵션/션유/유무'
		elif target_question[0] == 3 : 
			weight_keywords = '/차를/를직/직접/보고/볼수/예약/약가/가능/지점/점방/방문'
		elif target_question[0] == 4 : 
			weight_keywords = '/오프/프라/라인/구매/매이/이력/력등/등록/업뎃/업데/데이/이트'
		elif target_question[0] == 5 : 
			weight_keywords = '/배송/송비/탁송/송비/비얼/얼마'
		elif target_question[0] == 6 : 
			weight_keywords = '/포인/인트/트내/내역/찾아/아가/가는/는케/케어/어서/서비/비스/방문/문점/점검/냄새/새케/케어/신청/무상/상보/보증'
		elif target_question[0] == 7 : 
			weight_keywords = '/현금/금완/완납/네고/고가/가능/일시/시불/할인/디씨/추가/가할/할인/가격/격인/인하'
		elif target_question[0] == 8 : 
			weight_keywords = '/좋은/은차/차량/추천/천해/추천'
		elif target_question[0] == 9 : 
			weight_keywords = '/광고/고제/제휴/마케/케팅/휴업/협업/제안/채널/귀사/당사'
		elif target_question[0] == 10 : 
			weight_keywords = '/용도/도이/이력/업체/과거/거렌/렌트/트이/이력/렌터/터카/카이/이력'
		elif target_question[0] == 11 : 
			weight_keywords = '/지점/점위/위치/지점/점주/주소/구경/찾아'
		elif target_question[0] == 12 : 
			weight_keywords = '/현금/금영/영수/수증/증요/요청/증가'
		elif target_question[0] == 13 : 
			weight_keywords = '/리스/스상/상담/신용/용등/등급/리스/스가/리스/스신/신청/리스/스자/자격/리스/리스/리스'
		elif target_question[0] == 14 : 
			weight_keywords = '/환불/불절/절차/취소/환급'
		elif target_question[0] == 15 : 
			weight_keywords = '/장기/기렌/렌트/트계/계약/렌터/터카/렌트/렌터/트카/터카'
		elif target_question[0] == 16 : 
			weight_keywords = '/활용/용동/동의/비밀/밀번/번호/수신/신동/동의/이메/메일/회원/원정/정보/보수/수정'
		elif target_question[0] == 17 : 
			weight_keywords = '/계약/약중/중인/불발/발시/안팔/팔리/리면/계약/약취/취소/소되/되면'
		elif target_question[0] == 19 : 
			weight_keywords = '회원/원탈/탈퇴/퇴어/어떻/탈퇴'
		elif target_question[0] == 20 : 
			weight_keywords = '/사고/고이/이력/자세/세한/사고/고내/내역'
		elif target_question[0] == 21 : 
			weight_keywords = '/대차/차가/교체/체차/매입/입도/매입/대차/차도/교체/체도'
		elif target_question[0] == 23 : 
			weight_keywords = '/준비/비중/중인/판매/매시/시작/알람/알림/준비/비중'
		elif target_question[0] == 25 : 
			weight_keywords = '/할부/부기/기간/무이/이자/이율/금리/할부/부문/할부/부상/신용/용등/등급/금융'
		elif target_question[0] == 27 : 
			weight_keywords = '/결제/구입/카드/드한/한도/전액/결제/제관'

		target_question[1] += weight_keywords

		
		# # 최근
		# same_list = []
		# for source_bigrams in source_bigram_list : 
		# 	# source_bigrams [1, ['안녕', '차량', '량구', '구매', '매관', '관련', '련상', '상담', '담희', '희망', '망합', '합니', '니다']], 

		# 	# same_list = list(set(source_bigrams[1]) & set(target_bigrams))
		# 	same_list = list(set(source_bigrams[1]) & set(target_bigrams))
		# 	if same_list : 
		# 		fin_result.append([source_bigrams[0], len(same_list), same_list])

		# 			# if target_bigram == source_bigram :
		# 			# 	# print(target_bigram)
		# 			# 	same_grams.append(target_bigram)
		# 			# 	group.append(source_bigrams[0])
		# 			# 	# source_bigrams[0] : 5 (Q CATEGORY)
		# 			# 	same_count += 1
		# 			# 	group.append(same_count)
		# 			# 	group.append(same_grams)
		# 			# 	# print(group)
		# 			# 	# print(f'[일치] {source_bigrams[0]} // {source_bigram}')
		# 			# 	# print(fin_result)
		# 			# 	in_fin_result.append(group)
		# # print(fin_result)
		# # 최근 끝

		# 옛날
		
		for source_bigrams in source_bigram_list : 
			# source_bigrams [1, ['안녕', '차량', '량구', '구매', '매관', '관련', '련상', '상담', '담희', '희망', '망합', '합니', '니다']], 
			same_count = 0
			same_grams = []
			for in_idx, source_bigram in enumerate(source_bigrams[1]) : 
				# source_bigrams ['안녕', '차량', '량구', '구매', '매관', '관련', '련상', '상담', '담희', '희망', '망합', '합니', '니다']
				for target_bigram in target_bigrams : 
					# target_bigrams : ['안녕', '녕하', '하세', '세요']
					# 숫자 두자리는 제거
					if not isinstance(target_bigram, int ) :
						if target_bigram == source_bigram : 
							same_count += 1
							same_grams.append(target_bigram)
			
			if len(same_grams) :
				fin_result.append([source_bigrams[0], same_count, same_grams]) 

	# print(fin_result)
	# score_list = []
	# for result in fin_result :
	# 	# result [27, 3, ['능한', '리스', '가능']]
	# 	max = 0
	# 	group = []
	# 	if max < result[1] :
	# 		max = result[1]
	# 		# print('max보다 result[1]이 커서 ', max)
	# 		group.append(result[0])
	# 		group.append(max)
	# 		group.append(result[2])
	# 		score_list.append(group)

	score_list = sorted(fin_result, key=lambda x: x[1], reverse=True)

	# rank_box = []
	# for idx, score in enumerate(score_list) : 
	# 	# print('ㅡ'* 70)
	# 	# print(score[0])
	# 	# score : [6, 2, ['가능', '능한']], 
	# 	q_type = ''
	# 	q_type = get_question_type(score[0])
	# 	rank_box.append(score[0])
	# 	# print(f'\n[{q_type} ({round((score[1]/len_q_list_gram)* 100, 2)}% 확률), ({score[1]}/{len_q_list_gram})] \n')
	# 	# print(f'\n\n[{q_type}, ({score[1]}/{len_q_list_gram})] \n\n일치하는 gram 목록 : {score[2]}\n')
	
	# print(rank_box)
	
	# count = {}
	# for rank in rank_box : 
	# 	# print(rank)
	# 	try :
	# 		count[rank] += 1
	# 	except : 
	# 		count[rank] = 1
	
	# rank_list = sorted(count.items(), key=(lambda x: x[1]), reverse=True)
	# # print(rank_list)

	for idx, rank in enumerate(score_list) : 
		if idx > 2 : 
			break
		else :
			q_type = get_question_type(rank[0])
			print(f'이 문의 타입은 {q_type} 확률이 {idx + 1}번째로 높다. \n {rank[2]}')

def mining_sentence(q_list, cursor) :
	kkma = Kkma()
	# 제외할 단어 목록
	except_word_list = []
	fin_result = []
	
	for idx, q in enumerate(q_list) : 
		question = [q[0], remove_html(q[1])]
		sentence = re.sub('[-=.#/?:$}\"\']', '', str(question[1])).replace('[','').replace(']','')
		origin_word_list = list(dict.fromkeys(regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}|\d+]+', f'{sentence}')))
		# 형태소 분석
		out_result = []
		out_result.append(question[0])
		result = []
		for origin_word in origin_word_list :
			if (origin_word not in except_word_list) : 
				for morpheme in kkma.pos(origin_word) :	
					if (len(morpheme[0]) > 1) and (morpheme[1] == 'NNG' or morpheme[1] == 'NNP' or morpheme[1] == 'NNB' or morpheme[1] == 'NNM'):
						in_result = []	
						in_result.append(origin_word)
						in_result.append(morpheme[0])
					
						result.append(in_result)
		out_result.append(result)
		fin_result.append(out_result)

	# print(fin_result)
	target_morpheme_list = []
	for idx, result in enumerate(fin_result) :
		# result : [[4311, [['제네시스', '제네시스'], ['매물', '매물'], ['차량번호', '차량'], ['차량번호', '번호'], ['대한', '대한'], ['상담', '상담'], ['문의', '문의']]], [4299, ...]
		for words in result[1] : 
			source_word = words[1]
			in_target_morpheme_words = []
			in_target_morpheme_words.append(source_word)
			in_target_morpheme_words.append(result[0])
			try : 
				cursor.execute(f"""
					SELECT 
						TARGET_MORPHEME_WORD 
					FROM 
						TBL_CCQ_KEYWORD_MAP
					WHERE
						SOURCE_MORPHEME_WORD = "{source_word}" 
					ORDER BY
						DISTANCE_WEIGHT DESC,
						WORD_DISTANCE DESC
					LIMIT 5 	
				""")
				rows = cursor.fetchall()
				for in_idx, row in enumerate(rows) :
					in_group = []
					in_group.append(row[0])
					in_target_morpheme_words.append(in_group)
				target_morpheme_list.append(in_target_morpheme_words)
			except Exception as e :
				print(f'****** + error! >> {e} >>>>> SELECT 오류!')
				continue
			finally : 
				pass
	
	print(target_morpheme_list)
	# [
	# 	['제네시스', 4311, ['차량'], ['관심'], ['구매'], ['부탁'], ['가능']], 
	# 	['매물', 4311, ['가요'], ['번호'], ['상담'], ['문의'], ['확인']], 
	# 	['차량', 4311, ['문의'], ['구매'], ['부탁'], ['부탁'], ['상담']], 
	# 	['번호', 4311, ['완료'], ['상품'], ['며칠'], ['회신'], ['부 탁']], 
	# 	['대한', 4311], ['상담', 4311, ['부탁'], ['신청'], ['문의'], ['한번'], ['희망']], 
	# 	['문의', 4311, ['구매'], ['확인'], ['확인'], ['문자'], ['문자']], 
	# 	['장기', 4299, ['문의'], ['이용'], ['개월'], ['정도'], ['타이어']], 
	# 	['렌트', 4299, ['이용'], ['개월'], ['정 도'], ['타이어'], ['앞쪽']], 
	# 	['이용', 4299, ['문의'], ['방법'], ['타이어'], ['앞쪽'], ['마모']], 
	# 	['한지', 4299, ['포기']], 
	# 	['정도', 4299, ['이전비'], ['앞쪽'], ['마모'], ['교체'], ['렌트']], 
	# 	['타이어', 4299, ['앞쪽'], ['마모'], ['교체'], ['할부'], ['문의']], 
	# 	['앞쪽', 4299, ['마모'], ['교체']], 
	# 	['마모', 4299, ['교체']], 
	# 	['교체', 4299, ['잔여'], ['횟수'], ['부탁'], ['내역'], ['문의']], 
	# 	['주시', 4299, ['진영'], ['논의'], ['감사'], ['감사'], ['안내']]
	# ]

def get_near_keyword(q_list, cursor) : 
	kkma = Kkma()
	# 제외할 단어 목록
	except_word_list = []
	fin_result = []

	for idx, q in enumerate(q_list) : 
		question = [q[0], remove_html(q[1])]
		sentence = re.sub('[-=.#/?:$}\"\']', '', str(question[1])).replace('[','').replace(']','')
		origin_word_list = list(dict.fromkeys(regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}|\d+]+', f'{sentence}')))
		# 형태소 분석
		out_result = []
		out_result.append(question[0])
		result = []
		for origin_word in origin_word_list :
			if (origin_word not in except_word_list) : 
				for morpheme in kkma.pos(origin_word) :	
					if (len(morpheme[0]) > 1) and (morpheme[1] == 'NNG' or morpheme[1] == 'NNP' or morpheme[1] == 'NNB' or morpheme[1] == 'NNM'):
						in_result = []	
						in_result.append(morpheme[0])
					
						result.append(in_result)
		out_result.append(result)
		fin_result.append(out_result)


	for result in fin_result : 
		qna_no = result[0]
		print(result)
		for morpheme in result[1] : 
			morpheme_keyword = morpheme[0]
			# print(type(morpheme_keyword), morpheme_keyword)
			
			try : 
				cursor.execute(f"""
					SELECT 
						TARGET_MORPHEME_WORD 
					FROM 
						TBL_CCQ_KEYWORD_MAP 
					WHERE 
						SOURCE_WORD = "{morpheme_keyword}"
					ORDER BY 
						WORD_DISTANCE DESC 
					LIMIT 1
				""")
				keyword = cursor.fetchall()
				if len(keyword) > 0 :
					print(f'"{morpheme_keyword}"과(와) 연관단어 > "{keyword[0][0]}"')
			except Exception as e :
				print(f'****** + error! >> {e} >>>>> SELECT 오류!')
				continue
			finally : 
				pass



if __name__ == '__main__' : 

	
	# now = time.localtime()
	# start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	dbconn2 = pymssql.connect(host=db_infos2.get('host'), user=db_infos2.get('user'), password=db_infos2.get('password'), database=db_infos2.get('database'), port=db_infos2.get('port'))
	cursor2 = dbconn2.cursor()

	compare_sentence([[0, '리스 관련 문의 드립니다.']], cursor)
	# mining_sentence(get_question_list(cursor2), cursor)

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


