from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import os

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

DEVELOPER_KEY = 'AIzaSyA2AZ0G5sRKq3uDTa_KzDT2X0oJ9rdcZWk'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

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

def youtube_search(keywords) :
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
	
	search_response = youtube.search().list(
		q = keywords,
		part = 'id, snippet',
		order = 'relevance',
		maxResults = 50
	).execute()
	
	video_list = []
	channel_list = []
	play_list = []
	video_id_list = []
	
	for search_result in search_response.get('items', []) :
		if search_result['id']['kind'] == 'youtube#video' : 
			video_list.append(
				{
					'channel_name' : search_result['snippet']['channelTitle'],
					'video_id' : search_result['id']['videoId'],
					'title' : search_result['snippet']['title'],
					'thumbnail' : search_result['snippet']['thumbnails']['high']['url'],
				}
			)
		# elif search_result['id']['kind'] == 'youtube#channel' :
		# 	channel_list.append([(search_result['snippet']['title'], search_result['id']['channelId'])])
		# elif search_result['id']['kind'] == 'youtube#playlist' : 
		# 	play_list.append([(search_result['snippet']['title'], search_result['id']['playlistId'])])
			
	return video_list

def get_comments(keyword) :
	video_list = youtube_search(f'{keyword} 시승기')

	user_id_group = []
	comment_group = []
	registed_date_group = []
	length_group = []
	
	for idx, video in enumerate(video_list[:10]) :
		url = f'https://www.youtube.com/watch?v={video.get("video_id")}'
		file_name = f'{keyword}_review_comments_youtube'

		soup = get_soup(url)
		user_id_list = soup.select('div#header-author > a > span')
		comment_list = soup.select('yt-formatted-string#content-text')
		registed_date_list = soup.select('yt-formatted-string.published-time-text')

		# replace / append data
		for i in range(len(user_id_list)):
			str_tmp = str(user_id_list[i].text)
			str_tmp = str_tmp.replace('\n', '')
			str_tmp = str_tmp.replace('\t', '')
			str_tmp = str_tmp.replace('   ','')
			user_id_group.append(str_tmp)

			str_tmp = str(comment_list[i].text)
			str_tmp = str_tmp.replace('\n', '')
			str_tmp = str_tmp.replace('\t', '')
			str_tmp = str_tmp.replace('   ','')
			comment_group.append(str_tmp)
			# print(f'[{i} / {len(user_id_list)}] {str_tmp}')
			length_group.append(len(str_tmp))

			str_tmp = str(registed_date_list[i].text)
			registed_date_group.append(str_tmp)

		print(f'[{idx +1}/{len(video_list[:10])}][{video.get("channel_name")}] {video.get("title")} >> 댓글 수집 완료!')
		time.sleep(2)
	
	pd_data = {'register': user_id_group, 'comment': comment_group, 'registed_date': registed_date_group, 'length': length_group}
	comments_pd = pd.DataFrame(pd_data)

	# to excel
	comments_pd.to_excel(f'../data/youtube_comments/{file_name}.xlsx', index=True, encoding='utf-8-sig')
	print(comments_pd)

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
	sentence_test('흠..역시 고루해 디자인...과도한 크롬 ㅡㅡ; 시대에 역행하는 뒷좌석은 직각 말리부와 다를것이 없다..   역시 유럽차와는 많이 다르고 힘든차...말리부 처음봤을때 이건 머여 라는 느낌 여기서도 느껴지는군..한마디로 별로라는..외산차의 무조건적인 믿음 국산차는 후접하다는 평..여기에서도 역시 느껴지는군..외산차 찬양')


	# 시작 시간 (전체 수행시간을 구하기 위함)
	start = time.time()  
	
	# 영상 검색 후 댓글 가져오기
	# get_comments('현대자동차그렌져HG')

	# 종료 시간 (전체 수행시간을 구하기 위함)
	end = time.time()
	# 전체 수행시간
	min, sec = divmod(round(end - start), 60)
	print('*** 작업 총 소요 시간 : %02d분 %02d초' % (min, sec))

	

### 특정 제품, 상품 여론 평가를 위한 댓글을 수집해드립니다.
### 예를 들면 유튜브에서 "아이폰12프로 리뷰"로 검색을 하면 다양한 영상이 검색 됩니다.