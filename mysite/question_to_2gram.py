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
		if idx > 0 : 
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

def get_answer_list(cursor) : 
	a_list = []

	cursor.execute(f"""
		SELECT 
			QNA_NO, ANSWER_CONTENTS
		FROM 
			TBL_QNA_LIST
		WHERE 
			MINING_STATUS = 1 AND STATUS = 1 AND IS_ANSWER = 3
		ORDER BY 
			ADD_DATE DESC
	""")
	rows = cursor.fetchall()

	for idx, row in enumerate(rows) :
		if idx > 0 : 
			break
		else : 
			group = []
			row01 = ''
			if row[1] is not None :
				row01 = row[1].encode('ISO-8859-1').decode('euc-kr', 'ignore').strip()
			group.append(row[0])
			if row01 != '' :
				group.append(row01)
			a_list.append(group)

	return a_list


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

def get_answer(q_type, q_type_text) : 
	# print(f'[질문타입 > {q_type_text}({q_type})]')
	template_head = '\n안녕하세요 [고객명] 고객님, \n\n'
	template_footer = '\n\n오늘도 즐거우하루 보내세요, \n감사합니다 :) '
	answer = ''
	if q_type == 1 : 
		answer = '문의 주신 내용은 차량 담당 매니저에게 전달하여 상담 드리도록 하겠습니다.'
	elif q_type == 2 :
		answer = '문의 주신 내용은 차량 담당 매니저에게 전달하여 상담 드리도록 하겠습니다.'
		# answer = '출고옵션 관련하여 담당매니저 명함과 상담관련 문자드리오니, \n문자받으신 후 상담시간 조율 후 궁금한점 문의주시면 되십니다.'
	elif q_type == 3 :
		answer = '방문하여 차량상담 가능하나, 차량 담당매니저와 조율없이 바로 내방은 어려운점 안내드립니다. \n금일 차량 담당매니저를 통한 방문일정 조율 및 차량상담으로 연락드리오니, 연락받으신 후 추가 궁금하신점 문의주시면 되십니다.'
	elif q_type == 4 :
		answer = '요청주신 차량정보 확인하였으며, 금일 중 고객님 아이디로 구매이력 등록도와드리겠습니다'
	elif q_type == 5 :
		answer = '문의 주신 탁송비, 배송비 내용 유선으로 안내 예정입니다.'
	elif q_type == 6 :
		answer = '문의 주신 서비스 관련 내용 담당 매니저에게 전달하여 상담 드리도록 하겠습니다.'
	elif q_type == 7 :
		answer = '리본카의 경우 차량정찰제를 운영하고 현금결제도 마찬가지로 홈페이지 표기금액과 동일한점 안내드립니다. \n우선 세일즈매니저를 통한 상담연락드리오니, 차량상세 및 구매 계약관련 궁금하신점 문의주시면 빠른안내도와드리겠습니다.'
	elif q_type == 8 :
		answer = '문의 주신 차량 추천 내용 차량 담당 매니저에게 전달하여 상담 드리도록 하겠습니다.'
	elif q_type == 9 :
		answer = '문의주신 제안 관련하여 담당부서 전달드렸습니다. 내용 확인하여 담당부서 연락드리겠습니다.'
	elif q_type == 10 :
		answer = '문의 주신 내용은 차량 담당 매니저에게 전달하여 상담 드리도록 하겠습니다.'
	elif q_type == 11 :
		answer = '홈페이지 링크 첨부드리오니 확인부탁드리며, \n홈페이지에 기재된 차량매니저님 연락주시면 자세한 상담도 가능하십니다. \n[지점 위치 URL]'
	elif q_type == 12 :
		answer = '구매하신 [차량번호] 차량에 대한 현금영수증 정상 발급 확인되어 유선으로 안내드렸습니다. \n[현금영수증 승인번호] 사진 문자로 보내드렸으니 참고 부탁드립니다.'
	elif q_type == 13 :
		answer = '문의주신 내용은 금융 담당 부서로 전달 하였으며, 신속히 안내 드리도록 하겠습니다.'
	elif q_type == 14 :
		answer = '문의 주신 내용은 차량 담당 매니저에게 전달하여 상담 드리도록 하겠습니다.'
	elif q_type == 15 :
		answer = '문의주신 내용은 렌터카 담당 부서로 전달 하였으며, 신속히 안내 드리도록 하겠습니다.'
	elif q_type == 16 :
		answer = '문의 주신 홈페이지 기능 내용 유선으로 안내 예정입니다.'
	elif q_type == 17 :
		answer = '문의 주신 내용은 차량 담당 매니저에게 전달하여 상담 드리도록 하겠습니다.'
	elif q_type == 18 :
		answer = '문의 주신 내용은 차량 담당 매니저에게 전달하여 상담 드리도록 하겠습니다.'
	elif q_type == 19 :
		answer = '홈페이지를 통해 문의주신 탈퇴 경로 안내드리겠습니다. \n*모바일 경로:  로그인 → 마이페이지 → 회원정보 → 비밀번호 추가 입력 → 회원정보수정 페이지 맨 하단 "회원탈퇴" 클릭하여 진행 가능합니다.'
	elif q_type == 20 :
		answer = '문의 주신 내용은 차량 담당 매니저에게 전달하여 상담 드리도록 하겠습니다.'
	elif q_type == 21 :
		answer = '문의 주신 내용은 차량 담당 매니저에게 전달하여 상담 드리도록 하겠습니다.'
	elif q_type == 23 :
		answer = '문의 주신 내용은 차량 담당 매니저에게 전달하여 상담 드리도록 하겠습니다.'
	elif q_type == 25 :
		answer = '문의주신 내용은 금융 담당 부서로 전달 하였으며, 신속히 안내 드리도록 하겠습니다.'
	elif q_type == 27 :
		answer = '문의 주신 결제 관련 내용 담당 부서로 전달 하였으며, 신속히 안내 드리도록 하겠습니다.'

	answer_template = template_head + answer + template_footer
	return answer_template

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
		q_type = '서비스 문의 (찾케서, 포인트, 보증기간 등)'
	elif q_type == 7 :
		q_type = '네고 가능 여부 문의'
	elif q_type == 8 :
		q_type = '차량 추천 문의'
	elif q_type == 9 :
		q_type = '업체 제휴 문의'
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

# 제외할 단어 목록
except_word_list = ['않은','지않','용이','데장','은데','가능','능할','까요','답장', '대한', '일로', '통화', '문의', '혹시', '입니', '해서', '의드', '것같', '할수', '가있', '수있', '해서', '량을', '아서','안녕','녕하','하세','세요','드립','립니','니다','제가','인데','주세','하세','주세','합니','부탁', '요?', '요.', '나요', '있나', '해야', '하겠', '겠습', '있으', '이메', '메일', '드리', '습니', '에대', '록하', '에서', '리도']
def compare_sentence(q_list, cursor) : 
	global except_word_list
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

		# print(type(target_bigrams), target_bigrams)

		weight_keywords = []
		type1_keywords = ['에이','A카','리본','본카']
		type2_keywords = ['옵션','션문','가옵','출고','고옵','션유','유무']
		type3_keywords = ['차를','를직','직접','보고','볼수','예약','약가','점방','방문']
		type4_keywords = ['프라','라인','매이','력등','등록','업뎃','업데','데이','이트']
		type5_keywords = ['배송','탁송','송비','비얼']
		type6_keywords = ['포인','인트','트내','찾아','아가','가는','는케','케어','어서','서비','비스','문점','점검','냄새','새케','케어','신청','무상','상보','보증']
		type7_keywords = ['금완','완납','네고','고가','일시','시불','디씨','추가','가할','할인','격인']
		type8_keywords = ['은차','천해','추천']
		type9_keywords = ['광고','제휴','마케','케팅','휴업','협업','제안','채널','귀사','당사']
		type10_keywords = ['용도','도이','이력','과거','거렌','트이','카이','이력','도변']
		type11_keywords = ['지점','점위','위치','점주','주소','구경','찾아']
		type12_keywords = ['현금','금영','영수','수증','증요']
		type13_keywords = ['리스','스상','스가','스신','신청','스자','자격']
		type14_keywords = ['환불','불절','절차','취소','환급']
		type15_keywords = ['장기','기렌','렌트','트계','렌터','터카','렌터','트카','터카']
		type16_keywords = ['활용','용동','동의','비밀','밀번','번호','수신','신동','동의','이메','메일','원정','정보','보수','수정']
		type17_keywords = ['약중','중인','불발','발시','안팔','팔리','리면','약취','취소','소되','되면']
		type19_keywords = ['회원','원탈','탈퇴','퇴어','어떻','탈퇴']
		type20_keywords = ['사고','고이','내역','파손','정비']
		type21_keywords = ['대차','차가','체차','매입','입도','매입','차도','교체','체도','차판']
		type23_keywords = ['준비','비중','중인','판매','매시','시작','알람','알림','비중']
		type25_keywords = ['할부','부기','기간','무이','이자','이율','금리','부문','부상','신용','용등','등급','금융']
		type27_keywords = ['결제','구입','카드','드한','한도','전액','제관']

		if list(set(target_bigrams) & set(type1_keywords)) :  
			# weight_keywords = ['문의']
			weight_keywords = []
		elif list(set(target_bigrams) & set(type2_keywords)) :  
			weight_keywords = ['옵션','옵션','션문','가옵','옵션','출고','고옵','션유','유무']
		elif list(set(target_bigrams) & set(type3_keywords)) : 
			weight_keywords = ['차를','를직','직접','보고','볼수','예약','약가','지점','점방','방문']
		elif list(set(target_bigrams) & set(type4_keywords)) : 
			weight_keywords = ['오프','프라','라인','구매','매이','이력','력등','등록','업뎃','업데','데이','이트']
		elif list(set(target_bigrams) & set(type5_keywords)) : 
			weight_keywords = ['배송','송비','탁송','송비','비얼','얼마']
		elif list(set(target_bigrams) & set(type6_keywords)) : 
			weight_keywords = ['포인','인트','트내','내역','찾아','아가','가는','는케','케어','어서','서비','비스','방문','문점','점검','냄새','새케','케어','신청','무상','상보','보증']
		elif list(set(target_bigrams) & set(type7_keywords)) : 
			weight_keywords = ['금완','네고','고가','불할','할인','디씨','가할','할인','격인','인하']
		elif list(set(target_bigrams) & set(type8_keywords)) : 
			weight_keywords = ['은차','추천','천해','추천','추천','추천']
		elif list(set(target_bigrams) & set(type9_keywords)) : 
			weight_keywords = ['광고','고제','제휴','마케','케팅','휴업','협업','제안','채널','귀사','당사']
		elif list(set(target_bigrams) & set(type10_keywords)) : 
			weight_keywords = ['용도','도이','이력','업체','과거','거렌','렌트','트이','이력','렌터','터카','카이','이력']
		elif list(set(target_bigrams) & set(type11_keywords)) : 
			weight_keywords = ['지점','점위','위치','지점','점주','주소','구경','찾아']
		elif list(set(target_bigrams) & set(type12_keywords)) : 
			weight_keywords = ['현금','금영','영수','수증','증요','요청','증가']
		elif list(set(target_bigrams) & set(type13_keywords)) : 
			weight_keywords = ['리스','스상','상담','신용','용등','등급','리스','스가','리스','스신','리스','스자','리스','리스']
		elif list(set(target_bigrams) & set(type14_keywords)) : 
			weight_keywords = ['환불','불절','절차','취소','환급']
		elif list(set(target_bigrams) & set(type15_keywords)) : 
			if list(set(target_bigrams) & set(type10_keywords)) : 
				weight_keywords = ['용도','도이','이력','업체','과거','거렌']
			else : 
				weight_keywords = ['렌터','렌터','렌트','렌트','장기','기렌','트계','터카','트카','터카']
		elif list(set(target_bigrams) & set(type16_keywords)) : 
			weight_keywords = ['활용','용동','동의','비밀','밀번','번호','수신','신동','동의','이메','메일','회원','원정','정보','보수','수정']
		elif list(set(target_bigrams) & set(type17_keywords)) : 
			weight_keywords = ['계약','계약','약중','중인','불발','발시','안팔','팔리','리면','약취','취소','소되','되면']
		elif list(set(target_bigrams) & set(type19_keywords)) : 
			weight_keywords = ['탈퇴','탈퇴','회원','원탈','퇴어','어떻']
		elif list(set(target_bigrams) & set(type20_keywords)) : 
			weight_keywords = ['사고','사고','고이','이력','자세','세한','고내','내역']
		elif list(set(target_bigrams) & set(type21_keywords)) : 
			weight_keywords = ['대차','대차','교체','교체','차가','체차','매입','입도','매입','차도','체도']
		elif list(set(target_bigrams) & set(type23_keywords)) : 
			weight_keywords = ['준비','준비','비중','비중','중인','판매','매시','시작','알람','알림']
		elif list(set(target_bigrams) & set(type25_keywords)) : 
			weight_keywords = ['할부','할부','할부','할부','부기','기간','무이','이자','이율','금리','부문','부상','신용','용등','등급','금융','부할','월얼']
		elif list(set(target_bigrams) & set(type27_keywords)) : 
			weight_keywords = ['결제','구입','카드','드한','한도','전액','결제','제관']

		target_bigrams.extend(weight_keywords)
		# print(f'weight_keywords >> {target_bigrams}')
		
		for source_bigrams in source_bigram_list : 
			# source_bigrams [1, ['안녕', '차량', '량구', '구매', '매관', '관련', '련상', '상담', '담희', '희망', '망합', '합니', '니다']], 
			same_count = 0
			same_grams = []
			for in_idx, source_bigram in enumerate(list(set(source_bigrams[1]))) : 
				# source_bigrams ['안녕', '차량', '량구', '구매', '매관', '관련', '련상', '상담', '담희', '희망', '망합', '합니', '니다']
				if source_bigram not in except_word_list :
					for target_bigram in target_bigrams : 
						# target_bigrams : ['안녕', '녕하', '하세', '세요']
						# 숫자 두자리는 제거
						if not isinstance(target_bigram, int) :
							if target_bigram == source_bigram : 
								same_count += 1
								same_grams.append(target_bigram)
			
			if len(same_grams) :
				fin_result.append([source_bigrams[0], same_count, same_grams]) 

	score_list = sorted(fin_result, key=lambda x: x[1], reverse=True)

	# print(score_list)

	for idx, rank in enumerate(score_list) : 		
		# print(rank)
		if idx > 2 : 
			break
		else :
			q_type = get_question_type(rank[0])
			# print(rank[2])
			# rank[2] : 일치하는 bigrams
			# print(f'이 문의 타입은 {q_type} 확률이 {idx + 1}번째로 높다.')
			# print(f'이 문의 타입은 {q_type} 확률이 {idx + 1}번째로 높다. \n {rank[2]}')
			print(f'[추천답변 {idx + 1}]')
			print(get_answer(rank[0], q_type))
			print()
			print('ㅡㅡㅡ'*15)
			print()

def mining_sentence(q_list, a_list, cursor) :
	# print(f'가져온 질문 >> {q_list}')
	# print(f'가져온 답변 >> {a_list}')
	kkma = Kkma()
	# 제외할 단어 목록
	global except_word_list
	q_fin_list = []
	
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
						in_result = [origin_word, morpheme[0]]
						result.append(in_result)
		out_result.append(result)
		q_fin_list.append(out_result)

	# print(q_fin_list)
	q_morpheme_list = []
	for idx, result in enumerate(q_fin_list) :
		# result : [[4311, [['제네시스', '제네시스'], ['매물', '매물'], ['차량번호', '차량'], ['차량번호', '번호'], ['대한', '대한'], ['상담', '상담'], ['문의', '문의']]], [4299, ...]
		for words in result[1] : 
			source_word = words[1]
			in_target_morpheme_words = []
			in_target_morpheme_words = [source_word, result[0]]
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
				in_group = []
				for in_idx, row in enumerate(rows) :
					in_group.append(row[0])
				in_target_morpheme_words.append(in_group)
				q_morpheme_list.append(in_target_morpheme_words)
			except Exception as e :
				print(f'****** + error! >> {e} >>>>> SELECT 오류!')
				continue
			finally : 
				pass
	
	# print(q_morpheme_list)

	a_fin_list = []
	for idx, a in enumerate(a_list) : 
		answer = [a[0], remove_html(a[1])]
		sentence = re.sub('[-=.#/?:$}\"\']', '', str(answer[1])).replace('[','').replace(']','')
		origin_word_list = list(dict.fromkeys(regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}|\d+]+', f'{sentence}')))
		# 형태소 분석
		out_result = []
		out_result.append(answer[0])
		result = []
		for origin_word in origin_word_list :
			if (origin_word not in except_word_list) : 
				for morpheme in kkma.pos(origin_word) :	
					if (len(morpheme[0]) > 1) and (morpheme[1] == 'NNG' or morpheme[1] == 'NNP' or morpheme[1] == 'NNB' or morpheme[1] == 'NNM') :
						in_result = []	
						in_result = [origin_word, morpheme[0]]
						result.append(in_result)
		out_result.append(result)
		a_fin_list.append(out_result)

	# print(a_fin_list)

	a_morpheme_word_list = []
	for a_morpheme_list in a_fin_list : 
		group = []
		in_group = []
		group.append(a_morpheme_list[0])
		for a_morphemes in a_morpheme_list[1] : 
			in_group.append(a_morphemes[1])
		group.append(in_group)
		a_morpheme_word_list.append(group)

	# print(a_morpheme_word_list)
	# a_morpheme_word_list = [[3648, ['안녕', '고객', '오토', '플러스']]]

	print(f'q >> {q_morpheme_list}')
	print(f'a >> {a_morpheme_word_list}')


	for q_morphemes in q_morpheme_list : 
	# 	# q_morphemes = ['차량', 3648, ['매니저', '세일즈', '문의', '그랜저', '감사']]
	# 	print(a_fin_list)
		for a_morphemes in a_morpheme_word_list :
			for q_morpheme in list(set(q_morphemes[2])) :
				for a_morpheme in list(set(a_morphemes[1])) :
					if q_morpheme == a_morpheme : 
						print(f'같다 >> {q_morpheme}')







def get_near_keyword(q_list, cursor) : 
	kkma = Kkma()
	# 제외할 단어 목록
	global except_word_list 
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
	now = time.localtime()
	start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	dbconn2 = pymssql.connect(host=db_infos2.get('host'), user=db_infos2.get('user'), password=db_infos2.get('password'), database=db_infos2.get('database'), port=db_infos2.get('port'))
	cursor2 = dbconn2.cursor()

	compare_sentence([[0, '결제 관련 문의 드립니다.']], cursor)
	
	# 2021.07.02
	# mining_sentence([[0, '해당 차 용도 변경 이력 문의드립니다. LF쏘나타  사진상에는 차량번호가 38하5346이고 성능점검기록부에는 과거 렌트 이력이 있는데 왜 보험이력에는 대여 이력도 없고 차량번호 변경 이력도 없는지 설명 부탁드립니다. ']], cursor)
	

	# Fin 
	# mining_sentence(get_question_list(cursor2), get_answer_list(cursor2), cursor)

	# print(sentence_to_2gram(get_question_list(cursor2)))
	# insert_db_2gram(sentence_to_2gram(get_question_list(cursor2)))


	# dbconn.commit()
	# dbconn.close()

	# dbconn2.commit()
	# cursor2.close()

	now = time.localtime()
	end_time = now
	print('ㅡ'*50)
	print('상담 내용 DB Commit/Close 완료!')
	print('상담 내용 분석 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('상담 내용 분석 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))


