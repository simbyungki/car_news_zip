from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

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
	browser = webdriver.Chrome(r'C:\Users\PC\Documents\simbyungki\git\car_news_zip\chromedriver.exe', options=options)
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
	printProgressBar(0, len(video_list[:10]), prefix = 'Progress:', suffix = 'Complete', length = 50)
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
			length_group.append(len(str_tmp))

			str_tmp = str(registed_date_list[i].text)
			registed_date_group.append(str_tmp)

		printProgressBar(idx + 1, len(video_list[:10]), prefix = 'Progress:', suffix = 'Complete', length = 50)
		print(f'[{idx +1}/{len(video_list[:10])}][{video.get("channel_name")}] {video.get("title")} 댓글 수집 완료!')
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


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


if __name__ == '__main__' : 

	# # 시작 시간 (전체 수행시간을 구하기 위함)
	# start = time.time()  
	
	# # 영상 검색 후 댓글 가져오기
	get_comments('기아자동차올뉴모닝')

	# # 종료 시간 (전체 수행시간을 구하기 위함)
	# end = time.time()
	# # 전체 수행시간
	# min, sec = divmod(round(end - start), 60)
	# print('*** 작업 총 소요 시간 : %02d분 %02d초' % (min, sec))

	

### 특정 제품, 상품 여론 평가를 위한 댓글을 수집해드립니다.
### 예를 들면 유튜브에서 "아이폰12프로 리뷰"로 검색을 하면 다양한 영상이 검색 됩니다.