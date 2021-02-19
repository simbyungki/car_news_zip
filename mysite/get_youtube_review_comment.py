from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import os, json
import mysql.connector
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
DEVELOPER_KEY = 'AIzaSyA2AZ0G5sRKq3uDTa_KzDT2X0oJ9rdcZWk'
# KING BK#
# DEVELOPER_KEY = 'AIzaSyB08WDZOdnWGqfcDKl4FB30LIRJzQS7JCQ'
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


def get_comments(dbconn, cursor, keyword, bmname, boiname, boname, bono) :
	video_group = youtube_search(f'{keyword} 시승기')
	comment_group = []
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
					COMMENT_VIDEO_ID, BMNAME, BOINAME, BONAME,
					BONO, COMMENT_CONTENT, COMMENT_CONTENT_LENGTH, ADD_DATE, 
					MINNING_STATUS, PROC_STATUS
				) 
				VALUES (
					"{comment[0]}", "{bmname}", "{boiname}", "{boname}" ,
					{bono}, "{comment[2]}", {len(comment[2])}, NOW(), 
					1, 1
				) 
			""")
			print(f'[{idx + 1}/{len(comment_group)}] 댓글 수집 완료')
		except Exception as e :
			print(f'***** + error! >> {e} >> {comment[2]}')	
		else : 
			print(f'**** [{boname}시승기 영상] >> 유튜브 영상 댓글 수집 완료')
		



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
	# get_comments(dbconn, cursor, 차종, BMNAME, BOINAME, BONAME, BONO)
	get_comments(dbconn, cursor, '제네시스 eq900', '제네시스', 'EQ900', 'EQ900', 1594)

	dbconn.commit()
	dbconn.close()
	# 종료 시간 (전체 수행시간을 구하기 위함)
	end = time.time()
	# 전체 수행시간
	min, sec = divmod(round(end - start), 60)
	print('*** 작업 총 소요 시간 : %02d분 %02d초' % (min, sec))