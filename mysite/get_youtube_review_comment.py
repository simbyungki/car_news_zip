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
import pandas as pd
import xlrd
from bs4 import BeautifulSoup
from selenium import webdriver

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

def get_soup(url) :
	options = webdriver.ChromeOptions()
	options.headless = True
	options.add_argument('window-size=1920x1080')
	browser = webdriver.Chrome(r'../data/chromedriver.exe', options=options)
	browser.maximize_window()
	browser.get(url)

	# scroll (댓글 계속 로드)
	last_page_height = browser.execute_script("return document.documentElement.scrollHeight")
	while True:
		browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
		#  인터발 1이상으로 줘야 데이터 취득가능(롤링시 데이터 로딩 시간 때문)
		time.sleep(1)
		new_page_height = browser.execute_script("return document.documentElement.scrollHeight")

		if new_page_height == last_page_height:
			break
		last_page_height = new_page_height


	soup = BeautifulSoup(browser.page_source, 'lxml')
	return soup

# BeautifulSoup
def get_soup2(url) :
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
	res = requests.get(url, headers=headers)
	res.raise_for_status()
	res.encoding=None
	soup = BeautifulSoup(res.text, 'lxml')
	return soup

def youtube_search(keyword) :	
	search_response = youtube.search().list(
		q = keyword,
		part = 'id, snippet',
		order = 'relevance',
		# order = 'viewCount',
		maxResults = 10
	).execute()
	
	video_group = []
	
	for search_result in search_response.get('items', []) :
		in_info = {}
		in_info['video_id'] = search_result.get('id').get('videoId')
		in_info['video_title'] = search_result.get('snippet').get('title')
		in_info['video_pub_date'] = search_result.get('snippet').get('publishedAt')
		in_info['channel_name'] = search_result.get('snippet').get('channelTitle')
		in_info['channel_id'] = search_result.get('snippet').get('channelId')
		in_info['thumbnail'] = search_result.get('snippet').get('thumbnails').get('high', '').get('url', '')
		video_group.append(in_info)

	return video_group


def get_comments(cursor, apcursor, keyword, bono, daum_code) :
	print(keyword, '>> 시승기 영상정보 및 댓글 수집 시작')
	video_group = youtube_search(f'{keyword} 시승기')
	comment_group = []

	# 자동차 정보 입력
	car_infos = get_car_infos(daum_code)
	# print(car_infos)

	# APDB에서 자동차 정보 조회
	try : 
		apcursor.execute(f"""
			SELECT BMNAME, BOINAME , BONAME FROM ATB_NCAR_MODEL
			WHERE BONO = '{bono}'
			GROUP BY BMNAME, BOINAME, BONAME;
		""")

		aprow = apcursor.fetchone()
		bmname = aprow[0].encode('ISO-8859-1').decode('euc-kr')
		boiname = aprow[1].encode('ISO-8859-1').decode('euc-kr')
		boname = aprow[2].encode('ISO-8859-1').decode('euc-kr')
	except Exception as e :
		print(f'***** + error! >> {e}')
		

	try :
		cursor.execute(f"""
			INSERT INTO TBL_CAR_INFOS 
			(
				BMNAME, BOINAME, BONAME, BONO,
				DAUM_CODE, CAR_IMG_URL, CAR_PRICE,
				FUEL_EFFICIENCY, CAR_CC
			) 
			VALUES (
				"{bmname}", "{boiname}", "{boname}", "{bono}", 
				"{daum_code}", "{car_infos.get('car_img_url')}", "{car_infos.get('car_price')}",
				"{car_infos.get('car_per')}", "{car_infos.get('car_cc')}"
			) 
		""")
		cursor.execute("SELECT LAST_INSERT_ID();")
		inforow = cursor.fetchone()
		info_no = inforow[0]
		
	except Exception as e :
		print(f'***** + error! >> {e}')
	else : 
		print(f'**** [{boname} 시승기 영상] >> 유튜브 영상 댓글 수집 완료')

	for idx, video_info in enumerate(video_group) :
		url = f'https://www.youtube.com/watch?v={video_info.get("video_id")}'

		soup = get_soup(url)
		# video_title = soup.select('h1.title style-scope ytd-video-primary-info-renderer')
		user_id_list = soup.select('div#header-author > a > span')
		comment_list = soup.select('yt-formatted-string#content-text')
		registed_date_list = soup.select('yt-formatted-string.published-time-text')

		for i in range(len(user_id_list)):
			comment_set = []
			comment_set.append(video_info.get('video_id'))
			str_tmp = str(user_id_list[i].text)
			str_tmp = str_tmp.replace('\n', '')
			str_tmp = str_tmp.replace('\t', '')
			str_tmp = str_tmp.replace('   ','')
			comment_set.append(str_tmp)

			str_tmp = str(comment_list[i].text)
			str_tmp = str_tmp.replace('\n', '')
			str_tmp = str_tmp.replace('\t', '')
			str_tmp = str_tmp.replace('   ','')
			str_tmp = re.sub('\,', '&#44;', re.sub('[\"\'‘“”″′]', '&#8220;', str_tmp))
			comment_set.append(str_tmp)
			comment_set.append(len(str_tmp))

			str_tmp = str(registed_date_list[i].text)
			comment_set.append(str_tmp)
			comment_group.append(comment_set)
		
		print(f'[{idx +1}/{len(video_group)}] 댓글수집 완료')

	print(f'[{keyword} 시승기] Data 구조화 완료')

	# DB INSERT
	print('DB Insert 시작')
	for idx, comment in enumerate(comment_group) :
		try :
			cursor.execute(f"""
				INSERT INTO TBL_YOUTUBE_CAR_COMMENT_LIST 
				(
					COMMENT_VIDEO_ID, COMMENT_CONTENT, COMMENT_CONTENT_LENGTH, 
					ADD_DATE, MINNING_STATUS, PROC_STATUS, INFO_NO
				) 
				VALUES (
					"{comment[0]}", "{comment[2]}", {len(comment[2])}, 
					NOW(), 1, 1, "{info_no}"
				) 
			""")
			print(f'[{idx + 1}/{len(comment_group)}] 댓글 수집 완료')
		except Exception as e :
			print(f'***** + error! >> {e} >> {comment[2]}')	
			continue
		else : 
			print(f'**** [{boname} 시승기 영상] >> 유튜브 영상 댓글 수집 완료')
		
def get_car_infos(model_code) :
	url = f'https://auto.daum.net/newcar/model/{model_code}'
				
	soup = get_soup2(url)

	car_infos = {}

	car_info_area = soup.find('div', attrs={'class': 'box_model'})
	car_info_left = car_info_area.find('div', attrs={'class': 'info_model'}).findAll('table', attrs={'class', 'tbl_info'})[0]
	car_info_right = car_info_area.find('div', attrs={'class': 'info_model'}).findAll('table', attrs={'class', 'tbl_info'})[1]
	car_price = car_info_left.findAll('tr')[0].find('td').get_text().strip()
	car_per = car_info_left.findAll('tr')[2].find('td').get_text().strip()
	car_cc = car_info_right.findAll('tr')[1].find('td').get_text().strip()
	car_img_url = soup.find('div', attrs={'class': 'wrap_model'}).find('img')['src']

	# print(car_price, car_per, car_cc, netizen_grade)
	car_infos['car_price'] = car_price
	car_infos['car_per'] = car_per
	car_infos['car_cc'] = car_cc
	car_infos['car_img_url'] = car_img_url
	
	return car_infos


def car_comments() : 
	excel_path = '../data/youtube_comments/트레일블레이저_review_comments_youtube.xlsx'
	df = pd.read_excel(excel_path, usecols='B:D')

	comment_list = []
	
	for row in df.values :
		temp_dict = {}
		temp_dict['register'] = row[0]
		temp_dict['comment'] = row[1]
		temp_dict['registed_date'] = row[2]
		comment_list.append(temp_dict)

	return comment_list


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
		print(f' ★  위 문장은 {result_per}% 확률로 긍정적인 문장입니다.') 

if __name__ == '__main__' : 
	# sentence_test('흠..역시 고루해 디자인...과도한 크롬 ㅡㅡ; 시대에 역행하는 뒷좌석은 직각 말리부와 다를것이 없다..   역시 유럽차와는 많이 다르고 힘든차...말리부 처음봤을때 이건 머여 라는 느낌 여기서도 느껴지는군..한마디로 별로라는..외산차의 무조건적인 믿음 국산차는 후접하다는 평..여기에서도 역시 느껴지는군..외산차 찬양')

	# 시작 시간 (전체 수행시간을 구하기 위함)
	start = time.time()  

	# 영상 검색 후 댓글 가져오기
	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	apdbconn = pymssql.connect(host=db_infos.get('ap_host'), user=db_infos.get('ap_user'), password=db_infos.get('ap_password'), database=db_infos.get('ap_database'), port=db_infos.get('ap_port'), charset='ISO-8859-1')
	apcursor = apdbconn.cursor()
	# get_comments(dbconn, cursor, 차종, BONO, 다음자동차 모델코드)
	# get_comments(cursor, apcursor, '제네시스 g80 dh', 2515, 'mtx000wspp9f')
	# get_comments(cursor, apcursor, '제네시스 eq900', 1594, 'm06000wxpphw')
	# get_comments(cursor, apcursor, '쉐보레 임팔라', 1568, 'myi000v1ppp2')
	# get_comments(cursor, apcursor, '올뉴 K7', 1598, 'mgc00034ppzk')
	# get_comments(cursor, apcursor, '더뉴카니발', 2656, 'mzt0002gpp8e')
	get_comments(cursor, apcursor, '더뉴쏘렌토', 2611, 'm3q0002oppqm')
	# https://auto.daum.net/newcar/model/ma600020ppal#rating

	# get_car_infos(dbconn, cursor, 다음자동차 모델코드)
	# print(get_car_infos('mgc00034ppzk'))

	apdbconn.close()

	dbconn.commit()
	dbconn.close()
	# 종료 시간 (전체 수행시간을 구하기 위함)
	end = time.time()
	# 전체 수행시간
	min, sec = divmod(round(end - start), 60)
	print('*** 작업 총 소요 시간 : %02d분 %02d초' % (min, sec))