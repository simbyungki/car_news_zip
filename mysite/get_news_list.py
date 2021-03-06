import requests
import time
import schedule
import re
import regex
import mysql.connector
import os, json
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
## 장고 프로젝트를 사용할 수 있도록 환경을 구축
import django
django.setup()

from website.models import TblTotalCarNewsList, TblMemberList, TblNewsKeywordList, TblNewsKeywordMap
from datetime import datetime
from konlpy.tag import Kkma
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

new_car_list = []
used_car_list = []
review_list = []
industry_list = []
etc_list = []

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


# BeautifulSoup
def get_soup(url) :
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
	res = requests.get(url, headers=headers)
	res.raise_for_status()
	res.encoding=None
	soup = BeautifulSoup(res.text, 'lxml')
	return soup

# 셀레니움 (동적 DATA)
def get_soup2(url) :
	options = webdriver.ChromeOptions()
	options.headless = True
	options.add_argument('window-size=1920x1080')
	browser = webdriver.Chrome(r'C:\Users\PC\Documents\simbyungki\git\car_news_zip\chromedriver.exe', options=options)
	browser.maximize_window()
	browser.get(url)
	time.sleep(2)
	soup = BeautifulSoup(browser.page_source, 'lxml')
	return soup

# 기사 DB INSERT
# Custom 쿼리 실행 함수

# 오토뷰
class GetAutoview() :
	# 오토뷰 신차
	def new() :
		url = 'http://www.autoview.co.kr/content/news/news_new_car.asp?page=1&pageshow=1'
				
		soup = get_soup(url)

		h_news_list = soup.find('div', attrs={'class': 'top_article'}).find_all('li')
		news_list = soup.find('div', attrs={'class': 'section newslist'}).find_all('li')

		data_list = []
		return_data_dic = {}

		for h_news in h_news_list :
			link = h_news.find('a')['href']
			img_url = h_news.find('div', attrs={'class', 'thumb'})['style']
			subject = h_news.find('div', attrs={'class': 'tit'}).get_text().strip()
			summary = h_news.find('div', attrs={'class': 'txt'}).get_text().strip()
			date = h_news.find('div', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.autoview.co.kr'+ link
			data_group['img_url'] = img_url[21:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)
		
		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('div', attrs={'class', 'thumb'})['style']
			subject = news.find('div', attrs={'class': 'tit'}).get_text().strip()
			summary = news.find('div', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('div', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.autoview.co.kr'+ link
			data_group['img_url'] = img_url[21:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['autoview_new'] = data_list
		new_car_list.append(return_data_dic)

	# 오토뷰 자동차 산업
	def industry() :
		url = 'http://www.autoview.co.kr/content/news/news_cominfo.asp'
				
		soup = get_soup(url)

		h_news_list = soup.find('div', attrs={'class': 'top_article'}).find_all('li')
		news_list = soup.find('div', attrs={'class': 'section newslist'}).find_all('li')

		data_list = []
		return_data_dic = {}

		for h_news in h_news_list :
			link = h_news.find('a')['href']
			img_url = h_news.find('div', attrs={'class', 'thumb'})['style']
			subject = h_news.find('div', attrs={'class': 'tit'}).get_text().strip()
			summary = h_news.find('div', attrs={'class': 'txt'}).get_text().strip()
			date = h_news.find('div', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.autoview.co.kr'+ link
			data_group['img_url'] = img_url[21:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)
		
		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('div', attrs={'class', 'thumb'})['style']
			subject = news.find('div', attrs={'class': 'tit'}).get_text().strip()
			summary = news.find('div', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('div', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.autoview.co.kr'+ link
			data_group['img_url'] = img_url[21:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['autoview_industry'] = data_list
		industry_list.append(return_data_dic)

	# 오토뷰 자동차 시승기
	def review() :
		url = 'http://www.autoview.co.kr/content/buyer_guide/guide_road.asp?page=1&pageshow=1'
				
		soup = get_soup(url)

		h_news_list = soup.find('div', attrs={'class': 'top_article'}).find_all('li')
		news_list = soup.find('div', attrs={'class': 'section newslist'}).find_all('li')

		data_list = []
		return_data_dic = {}

		for h_news in h_news_list :
			link = h_news.find('a')['href']
			img_url = h_news.find('div', attrs={'class', 'thumb'})['style']
			subject = h_news.find('div', attrs={'class': 'tit'}).get_text().strip()
			summary = h_news.find('div', attrs={'class': 'txt'}).get_text().strip()
			date = h_news.find('div', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.autoview.co.kr'+ link
			data_group['img_url'] = img_url[21:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)
		
		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('div', attrs={'class', 'thumb'})['style']
			subject = news.find('div', attrs={'class': 'tit'}).get_text().strip()
			summary = news.find('div', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('div', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.autoview.co.kr'+ link
			data_group['img_url'] = img_url[21:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['autoview_review'] = data_list
		review_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=300).filter(news_content='')
		print('-'*30)
		print('오토뷰')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.autoview.co.kr/content/article.asp?num_code={newsList.values()[idx].get("news_code")}&news_section=new_car&pageshow=1'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('div', attrs={'class': 'view_title'}).find('h4').get_text().strip()
					d_content = soup.find('div', attrs={'class': 'article_text'}).get_text().strip()
					
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# IT조선 #
class GetItChosun() :
	# IT조선 신차	
	def new() :
		url = 'http://it.chosun.com/svc/list_in/list.html?catid=32&pn=1'
		soup = get_soup(url)

		h_news = soup.find('div', attrs={'class': 'thumb_big'})
		news_list = soup.select('.add_item_wrap > li')

		data_list = []
		return_data_dic = {}

		# headline
		link = h_news.find('div', attrs={'class': 'txt_wrap'}).find('a')['href']
		img_url = h_news.find('img')['src']
		subject = h_news.find('span', attrs={'class': 'tt'}).get_text().strip()
		summary = h_news.find('span', attrs={'class': 'txt'}).get_text().strip()
		reporter = h_news.find('span', attrs={'class': 'name'}).get_text().strip()
		date = h_news.find('span', attrs={'class': 'date'}).get_text().strip()
		data_group = {}
		data_group['link'] = link
		data_group['img_url'] = img_url
		data_group['subject'] = subject
		data_group['summary'] = summary
		data_group['reporter'] = reporter
		data_group['date'] = date
		data_list.append(data_group)

		# normal
		for news in news_list :
			link = news.find('div', 'txt_wrap').find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('div', attrs={'class': 'txt_dot1'}).get_text().strip()
			summary = news.find('span', attrs={'class': 'txt_dot2'}).get_text().strip()
			reporter = news.find('span', attrs={'class': 'name'}).get_text().strip()
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['chosun_new'] = data_list
		new_car_list.append(return_data_dic)

	# IT조선 시승기	
	def review() :
		url = 'http://it.chosun.com/svc/list_in/list.html?catid=33&pn=1'
		soup = get_soup(url)

		h_news = soup.find('div', attrs={'class': 'thumb_big'})
		news_list = soup.select('.add_item_wrap > li')

		data_list = []
		return_data_dic = {}

		# headline
		link = h_news.find('div', attrs={'class': 'txt_wrap'}).find('a')['href']
		img_url = h_news.find('img')['src']
		subject = h_news.find('span', attrs={'class': 'tt'}).get_text().strip()
		summary = h_news.find('span', attrs={'class': 'txt'}).get_text().strip()
		reporter = h_news.find('span', attrs={'class': 'name'}).get_text().strip()
		date = h_news.find('span', attrs={'class': 'date'}).get_text().strip()
		data_group = {}
		data_group['link'] = link
		data_group['img_url'] = img_url
		data_group['subject'] = subject
		data_group['summary'] = summary
		data_group['reporter'] = reporter
		data_group['date'] = date
		data_list.append(data_group)

		# normal
		for news in news_list :
			link = news.find('div', 'txt_wrap').find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('div', attrs={'class': 'txt_dot1'}).get_text().strip()
			summary = news.find('span', attrs={'class': 'txt_dot2'}).get_text().strip()
			reporter = news.find('span', attrs={'class': 'name'}).get_text().strip()
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['chosun_new'] = data_list
		review_list.append(return_data_dic)

	# IT조선 자동차업계	
	def industry() :
		url = 'http://it.chosun.com/svc/list_in/list.html?catid=31&pn=1'
		soup = get_soup(url)

		h_news = soup.find('div', attrs={'class': 'thumb_big'})
		news_list = soup.select('.add_item_wrap > li')

		data_list = []
		return_data_dic = {}

		# headline
		link = h_news.find('div', attrs={'class': 'txt_wrap'}).find('a')['href']
		img_url = h_news.find('img')['src']
		subject = h_news.find('span', attrs={'class': 'tt'}).get_text().strip()
		summary = h_news.find('span', attrs={'class': 'txt'}).get_text().strip()
		reporter = h_news.find('span', attrs={'class': 'name'}).get_text().strip()
		date = h_news.find('span', attrs={'class': 'date'}).get_text().strip()
		data_group = {}
		data_group['link'] = link
		data_group['img_url'] = img_url
		data_group['subject'] = subject
		data_group['summary'] = summary
		data_group['reporter'] = reporter
		data_group['date'] = date
		data_list.append(data_group)

		# normal
		for news in news_list :
			link = news.find('div', 'txt_wrap').find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('div', attrs={'class': 'txt_dot1'}).get_text().strip()
			summary = news.find('span', attrs={'class': 'txt_dot2'}).get_text().strip()
			reporter = news.find('span', attrs={'class': 'name'}).get_text().strip()
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['chosun_industry'] = data_list
		industry_list.append(return_data_dic)
	
	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=400).filter(news_content='')
		print('-'*30)
		print('IT조선')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://it.chosun.com/site/data/html_dir/{newsList.values()[idx].get("news_code")}'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('h1', attrs={'id': 'news_title_text_id'}).get_text().strip()
					d_content = soup.find('div', attrs={'id': 'news_body_id'}).get_text().strip()
					
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 오토헤럴드
class GetAutoH() :
	def new() :
		url = 'http://autotimes.hankyung.com/apps/news.sub_list?popup=0&nid=02&c1=02&c2=04&c3=&newscate=&isslide=&page=1'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.newest_list > dl')

		# normal
		for idx, news in enumerate(news_list) :
			link = news.find('dt').find('a')['href']
			subject = news.find('dt').find('a').get_text().strip()
			summary = news.find('dd', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('dd', attrs={'class': 'date'}).get_text().strip()
			if news.find('dd', attrs={'class', 'thum'}) :
				img_url = news.find('dd', attrs={'class', 'thum'}).find('img')['src']
			else :
				img_url = ''

			data_group = {}
			data_group['link'] = link
			if img_url != '' :
				data_group['img_url'] = 'http://autotimes.hankyung.com' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[0:-6]

			data_list.append(data_group)

			# 상위 15개만 가져오기
			if idx == 14 :
				break
			
		return_data_dic['autoh_new'] = data_list
		new_car_list.append(return_data_dic)

	# 오토헤럴드 중고차 (21.01.28 페이지 없어짐)
	def used() : 
		url = 'http://autotimes.hankyung.com/apps/news.sub_list?popup=0&nid=05&c1=05&c2=02&c3=&newscate=&isslide=&page=1'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.newest_list > dl')

		# normal
		for idx, news in enumerate(news_list) :
			link = news.find('dt').find('a')['href']
			subject = news.find('dt').find('a').get_text().strip()
			summary = news.find('dd', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('dd', attrs={'class': 'date'}).get_text().strip()
			if news.find('dd', attrs={'class', 'thum'}) :
				img_url = news.find('dd', attrs={'class', 'thum'}).find('img')['src']
			else :
				img_url = ''

			data_group = {}
			data_group['link'] = link
			if img_url != '' :
				data_group['img_url'] = 'http://autotimes.hankyung.com' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[0:-6]

			data_list.append(data_group)

			# 상위 15개만 가져오기
			if idx == 14 :
				break

		return_data_dic['autoh_used'] = data_list
		used_car_list.append(return_data_dic)

	# 오토헤럴드 시승기
	def review() :
		url = 'http://autotimes.hankyung.com/apps/news.sub_list?popup=0&nid=02&c1=02&c2=05&c3=&newscate=&isslide=&page=1'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.newest_list > dl')

		# normal
		for idx, news in enumerate(news_list) :
			link = news.find('dt').find('a')['href']
			subject = news.find('dt').find('a').get_text().strip()
			summary = news.find('dd', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('dd', attrs={'class': 'date'}).get_text().strip()
			if news.find('dd', attrs={'class', 'thum'}) :
				img_url = news.find('dd', attrs={'class', 'thum'}).find('img')['src']
			else :
				img_url = ''

			data_group = {}
			data_group['link'] = link
			if img_url != '' :
				data_group['img_url'] = 'http://autotimes.hankyung.com' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[0:-6]

			data_list.append(data_group)

			# 상위 15개만 가져오기
			if idx == 14 :
				break

		return_data_dic['autoh_review'] = data_list
		review_list.append(return_data_dic)

	# 오토헤럴드 자동차 업계
	def industry() :
		url = 'http://autotimes.hankyung.com/apps/news.sub_list?popup=0&nid=03&c1=03&c2=&c3=&newscate=&isslide=&page=1'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.newest_list > dl')

		# normal
		for idx, news in enumerate(news_list) :
			link = news.find('dt').find('a')['href']
			subject = news.find('dt').find('a').get_text().strip()
			summary = news.find('dd', attrs={'class': 'txt'}).get_text().strip()
			date = news.find('dd', attrs={'class': 'date'}).get_text().strip()
			if news.find('dd', attrs={'class', 'thum'}) :
				img_url = news.find('dd', attrs={'class', 'thum'}).find('img')['src']
			else :
				img_url = ''

			data_group = {}
			data_group['link'] = link
			if img_url != '' :
				data_group['img_url'] = 'http://autotimes.hankyung.com' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[0:-6]

			data_list.append(data_group)

			# 상위 15개만 가져오기
			if idx == 14 :
				break

		return_data_dic['autoh_industry'] = data_list
		industry_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=100).filter(news_content='')
		print('-'*30)
		print('오토헤럴드')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = 'http://autotimes.hankyung.com/apps/news.sub_view?popup=0&nid=05&c1=05&c2=02&c3=&nkey=' + newsList.values()[idx].get('news_code')
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('div', attrs={'class': 'view-title'}).find('h2').get_text().strip()
					d_content = soup.find('div', attrs={'class': 'view_report'}).get_text().strip()
					
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 데일리카 #
class GetDailyCar() :
	# 데일리카 중고차
	def used() :
		url = 'http://www.dailycar.co.kr/content/news.html?type=list&sub=sell&maker=used'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.nwslistwrap > .nwslist')

		# normal
		for idx, news in enumerate(news_list) :
			# 광고 제외
			if 'ad nwslist' not in str(news) :
				link = news.find('section', attrs={'class': 'nwslist_title'}).find('a')['href']
				subject = news.find('section', attrs={'class': 'nwslist_title'}).find('a').get_text().strip()
				summary = news.find('section', attrs={'class': 'nwslist_summary'}).get_text().strip()
				date = news.find('date').get_text().strip()
				img_url = news.find('div', attrs={'class', 'fixedratio'}).find('img')['src']
				# /data/news_xml_img/Id0000000216/ns107631.jpg
				# /data_thumb/gallery/Id0000000198/98680_240.jpg

				data_group = {}
				data_group['link'] = 'http://www.dailycar.co.kr'+ link
				data_group['img_url'] = 'http://www.dailycar.co.kr'+ img_url
				data_group['subject'] = subject
				data_group['summary'] = summary
				data_group['date'] = date[:10]

				data_list.append(data_group)

				# 상위 15개만 가져오기
				# if idx == 14 :
				# 	break

		return_data_dic['daily_used'] = data_list
		used_car_list.append(return_data_dic)

	# 데일리카 시승기
	def review() :
		url = 'http://www.dailycar.co.kr/content/news.html?gu=12'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.nwslistwrap > .nwslist')

		# normal
		for idx, news in enumerate(news_list) :
			# 광고 제외
			if 'ad nwslist' not in str(news) :
				link = news.find('section', attrs={'class': 'nwslist_title'}).find('a')['href']
				subject = news.find('section', attrs={'class': 'nwslist_title'}).find('a').get_text().strip()
				summary = news.find('section', attrs={'class': 'nwslist_summary'}).get_text().strip()
				date = news.find('date').get_text().strip()
				img_url = news.find('div', attrs={'class', 'fixedratio'}).find('img')['src']
				# /data/news_xml_img/Id0000000216/ns107631.jpg
				# /data_thumb/gallery/Id0000000198/98680_240.jpg

				data_group = {}
				data_group['link'] = 'http://www.dailycar.co.kr'+ link
				data_group['img_url'] = 'http://www.dailycar.co.kr'+ img_url
				data_group['subject'] = subject
				data_group['summary'] = summary
				data_group['date'] = date[:10]

				data_list.append(data_group)

				# 상위 15개만 가져오기
				# if idx == 14 :
				# 	break

		return_data_dic['daily_review'] = data_list
		review_list.append(return_data_dic)

	# 데일리카 자동차 업계
	def industry() :
		url = 'http://www.dailycar.co.kr/content/news.html?sub=news2'
		soup = get_soup(url)

		data_list = []
		return_data_dic = {}

		news_list = soup.select('.nwslistwrap > .nwslist')

		# normal
		for idx, news in enumerate(news_list) :
			# 광고 제외
			if 'ad nwslist' not in str(news) :
				link = news.find('section', attrs={'class': 'nwslist_title'}).find('a')['href']
				subject = news.find('section', attrs={'class': 'nwslist_title'}).find('a').get_text().strip()
				summary = news.find('section', attrs={'class': 'nwslist_summary'}).get_text().strip()
				date = news.find('date').get_text().strip()
				img_url = news.find('div', attrs={'class', 'fixedratio'}).find('img')['src']
				# /data/news_xml_img/Id0000000216/ns107631.jpg
				# /data_thumb/gallery/Id0000000198/98680_240.jpg

				data_group = {}
				data_group['link'] = 'http://www.dailycar.co.kr'+ link
				data_group['img_url'] = 'http://www.dailycar.co.kr'+ img_url
				data_group['subject'] = subject
				data_group['summary'] = summary
				data_group['date'] = date[:10]

				data_list.append(data_group)

				# 상위 15개만 가져오기
				# if idx == 14 :
				# 	break

		return_data_dic['daily_industry'] = data_list
		industry_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=200).filter(news_content='')
		print('-'*30)
		print('데일리카')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.dailycar.co.kr/content/news.html?type=view&autoId={newsList.values()[idx].get("news_code")}&from=%2Fcontent%2Fnews.html%3Ftype%3Dlist%26sub%3Dsell%26maker%3Dused'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('span', attrs={'id': 'content_titleonly'}).get_text().strip()
					d_content = soup.find('span', attrs={'id': 'content_bodyonly'}).get_text().strip()
					soup.select_one('span#content_bodyonly').figure.decompose()
					d_reporter = soup.select_one('span#content_bodyonly').get_text().strip()[6:12]
					
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}", REPORTER_NAME = "{d_reporter}" 
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 오토모닝 # 
class GetAutoMorning() :
	# 오토모닝 신차
	def new() :
		url = 'http://www.automorning.com/news/section_list_all.html?sec_no=84'
		soup = get_soup(url)

		news_list = soup.select('.ara_001 > .art_list_all > li')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('h2', attrs={'class': 'clamp c2'}).get_text().strip()
			summary = news.find('p', attrs={'class': 'ffd clamp c2'}).get_text().strip()
			reporter = summary[6:12]
			date = news.find('li', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date[:10]

			data_list.append(data_group)

		return_data_dic['automoring_new'] = data_list
		new_car_list.append(return_data_dic)

	# 오토모닝 중고차
	def used() :
		url = 'http://www.automorning.com/news/section_list_all.html?sec_no=85'
		soup = get_soup(url)

		news_list = soup.select('.ara_001 > .art_list_all > li')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('h2', attrs={'class': 'clamp c2'}).get_text().strip()
			summary = news.find('p', attrs={'class': 'ffd clamp c2'}).get_text().strip()
			reporter = summary[6:12]
			date = news.find('li', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date[:10]

			data_list.append(data_group)

		return_data_dic['automoring_used'] = data_list
		used_car_list.append(return_data_dic)

	# 오토모닝 시승기
	def review() :
		url = 'http://www.automorning.com/news/section_list_all.html?sec_no=87'
		soup = get_soup(url)

		news_list = soup.select('.ara_001 > .art_list_all > li')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('h2', attrs={'class': 'clamp c2'}).get_text().strip()
			summary = news.find('p', attrs={'class': 'ffd clamp c2'}).get_text().strip()
			reporter = summary[6:12]
			date = news.find('li', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date[:10]

			data_list.append(data_group)

		return_data_dic['automoring_review'] = data_list
		review_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=500).filter(news_content='')
		print('-'*30)
		print('오토모닝')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.automorning.com/news/article.html?no={newsList.values()[idx].get("news_code")}'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('div', attrs={'class': 'art_top'}).find('h2').get_text().strip()
					d_content = soup.find('div', attrs={'id': 'news_body_area'}).get_text().strip()
					
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 오토다이어리 #
class GetAutoDiary() :
	# 오토다이어리 신차
	def new() :
		url = 'http://www.autodiary.kr/category/news/new-car/'
		soup = get_soup(url)

		news_list = soup.select('#posts-container > div')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('h2', attrs={'class': 'entry-title'}).get_text().strip()
			summary = ''
			date = news.find('span', attrs={'class': 'updated'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[:10]

			data_list.append(data_group)

		return_data_dic['autodiary_new'] = data_list
		new_car_list.append(return_data_dic)

	# 오토다이어리 자동차 업계
	def industry() :
		url = 'http://www.autodiary.kr/category/news/car-business/'
		soup = get_soup(url)

		news_list = soup.select('#posts-container > div')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a')['href']
			if news.find('img') :  
				img_url = news.find('img')['src']
			else :
				img_url = ''
			subject = news.find('h2', attrs={'class': 'entry-title'}).get_text().strip()
			summary = ''
			date = news.find('span', attrs={'class': 'updated'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[:10]

			data_list.append(data_group)

		return_data_dic['autodiary_industry'] = data_list
		industry_list.append(return_data_dic)

	# 오토다이어리 시승기
	def review() :
		url = 'http://www.autodiary.kr/category/impression/'
		soup = get_soup(url)

		news_list = soup.select('#posts-container > div')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('h2', attrs={'class': 'entry-title'}).get_text().strip()
			summary = ''
			date = news.find('span', attrs={'class': 'updated'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[:10]

			data_list.append(data_group)

		return_data_dic['autodiary_review'] = data_list
		review_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=600).filter(news_content='')
		print('-'*30)
		print('오토다이어리')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.autodiary.kr{newsList.values()[idx].get("news_code")}'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('h2', attrs={'class': 'entry-title'}).get_text().strip()
					d_content = soup.find('div', attrs={'class': 'post-content'}).get_text().strip()
					d_content_tree = soup.find('div', attrs={'class': 'post-content'}).find_all('p')
					reporter = d_content_tree[len(d_content_tree) -1].get_text()[0:4]
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}", REPORTER_NAME = "{reporter}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 카가이 #
class GetCarguy() :
	# 카가이 자동차 업계
	def industry() :
		url = 'http://www.carguy.kr/news/articleList.html?page=1&total=3201&sc_section_code=S1N1&view_type=sm'
		soup = get_soup(url)

		news_list = soup.select('.article-list-content > .list-block')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'list-titles'}).find('a')['href']
			img_url = news.find('div', attrs={'class': 'list-image'})['style']
			subject = news.find('div', attrs={'class': 'list-titles'}).get_text().strip()
			summary = news.find('p', attrs={'class': 'list-summary'}).get_text().strip()
			info = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.carguy.kr' + link
			data_group['img_url'] = 'http://www.carguy.kr/news' + img_url[22:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = info[5:12]
			data_group['date'] = info[-16:-6]

			data_list.append(data_group)

		return_data_dic['carguy_industry'] = data_list
		industry_list.append(return_data_dic)

	# 카가이 시승기
	def review() :
		url = 'http://www.carguy.kr/news/articleList.html?page=1&total=1477&sc_section_code=S1N3&view_type=sm'
		soup = get_soup(url)

		news_list = soup.select('.article-list-content > .list-block')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'list-titles'}).find('a')['href']
			img_url = news.find('div', attrs={'class': 'list-image'})['style']
			subject = news.find('div', attrs={'class': 'list-titles'}).get_text().strip()
			summary = news.find('p', attrs={'class': 'list-summary'}).get_text().strip()
			info = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.carguy.kr' + link
			data_group['img_url'] = 'http://www.carguy.kr/news' + img_url[22:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = info[5:12]
			data_group['date'] = info[-16:-6]

			data_list.append(data_group)

		return_data_dic['carguy_review'] = data_list
		review_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=700).filter(news_content='')
		print('-'*30)
		print('카가이')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.carguy.kr/news/articleView.html?idxno={newsList.values()[idx].get("news_code")}'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('div', attrs={'class': 'article-head-title'}).get_text().strip()
					d_content = soup.find('div', attrs={'id': 'article-view-content-div'}).get_text().strip()
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 더드라이브 #
class GetTheDrive() :
	# 더드라이브 자동차 업계
	def industry() :
		url = 'http://www.thedrive.co.kr/news/newsList.php?tid=181930993&pagenum=0'
		soup = get_soup(url)

		news_list = soup.select('#listWrap > .listPhoto')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('p', attrs={'class': 'img'}).find('a')['href']
			img_url = news.find('p', attrs={'class': 'img'}).find('img')['src']
			subject = news.find('dt').get_text().strip()
			summary = news.find('dd', attrs={'class': 'conts'}).get_text().strip()
			reporter = news.find('dd', attrs={'class': 'winfo'}).find('a').get_text().strip()
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.thedrive.co.kr' + link
			data_group['img_url'] = 'http://www.thedrive.co.kr' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['drive_industry'] = data_list
		industry_list.append(return_data_dic)

	# 더드라이브 시승기
	def review() :
		url = 'http://www.thedrive.co.kr/news/newsList.php?tid=181930911&pagenum=0'
		soup = get_soup(url)

		news_list = soup.select('#listWrap > .listPhoto')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('p', attrs={'class': 'img'}).find('a')['href']
			img_url = news.find('p', attrs={'class': 'img'}).find('img')['src']
			subject = news.find('dt').get_text().strip()
			summary = news.find('dd', attrs={'class': 'conts'}).get_text().strip()
			reporter = news.find('dd', attrs={'class': 'winfo'}).find('a').get_text().strip()
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.thedrive.co.kr' + link
			data_group['img_url'] = 'http://www.thedrive.co.kr' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['drive_review'] = data_list
		review_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=800).filter(news_content='')
		print('-'*30)
		print('더드라이브')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.thedrive.co.kr/news/newsview.php?ncode={newsList.values()[idx].get("news_code")}'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('div', attrs={'class': 'viewTitle'}).find('h3').get_text().strip()
					d_content = soup.find('div', attrs={'id': 'viewConts'}).get_text().strip()
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 모터그래프
class GetMotorGraph() :
	# 신차
	def new() :
		url = 'https://www.motorgraph.com/news/articleList.html?page=1&total=1103&sc_section_code=&sc_sub_section_code=S2N2&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&sc_word2=&sc_andor=&sc_order_by=E&view_type=sm'
		soup = get_soup(url)

		news_list = soup.find('section', attrs={'class': 'article-list-content'}).findAll('div', attrs={'class': 'list-block'})
		
		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'list-image'}).find('a')['href']
			img_url = news.find('div', attrs={'class': 'list-image'})['style'][22:-1]
			subject = news.find('div', attrs={'class': 'list-titles'}).find('strong').get_text().strip()
			summary = news.find('p', attrs={'class': 'list-summary'}).find('a').get_text().strip()
			reporter = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			reporter = re.search(r'\|(.*?)\|', reporter).group(1).strip()
			date = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()[-16:-6]
			data_group = {}
			data_group['link'] = 'https://www.motorgraph.com' + link
			data_group['img_url'] = 'https://www.motorgraph.com/news/' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['motorgraph_new'] = data_list
		new_car_list.append(return_data_dic)

	# 시승기 (국산)
	def review_k() :
		url = 'https://www.motorgraph.com/news/articleList.html?page=1&total=142&sc_section_code=&sc_sub_section_code=S2N4&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&sc_word2=&sc_andor=&sc_order_by=E&view_type=sm'
		soup = get_soup(url)

		news_list = soup.find('section', attrs={'class': 'article-list-content'}).findAll('div', attrs={'class': 'list-block'})
		
		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'list-image'}).find('a')['href']
			img_url = news.find('div', attrs={'class': 'list-image'})['style'][22:-1]
			subject = news.find('div', attrs={'class': 'list-titles'}).find('strong').get_text().strip()
			summary = news.find('p', attrs={'class': 'list-summary'}).find('a').get_text().strip()
			reporter = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			reporter = re.search(r'\|(.*?)\|', reporter).group(1).strip()
			date = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()[-16:-6]
			data_group = {}
			data_group['link'] = 'https://www.motorgraph.com' + link
			data_group['img_url'] = 'https://www.motorgraph.com/news/' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['motorgraph_review_k'] = data_list
		review_list.append(return_data_dic)

	# 시승기 (수입)
	def review_g() :
		url = 'https://www.motorgraph.com/news/articleList.html?page=1&total=344&sc_section_code=&sc_sub_section_code=S2N5&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&sc_word2=&sc_andor=&sc_order_by=E&view_type=sm'
		soup = get_soup(url)

		news_list = soup.find('section', attrs={'class': 'article-list-content'}).findAll('div', attrs={'class': 'list-block'})
		
		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'list-image'}).find('a')['href']
			img_url = news.find('div', attrs={'class': 'list-image'})['style'][22:-1]
			subject = news.find('div', attrs={'class': 'list-titles'}).find('strong').get_text().strip()
			summary = news.find('p', attrs={'class': 'list-summary'}).find('a').get_text().strip()
			reporter = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			reporter = re.search(r'\|(.*?)\|', reporter).group(1).strip()
			date = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()[-16:-6]
			data_group = {}
			data_group['link'] = 'https://www.motorgraph.com' + link
			data_group['img_url'] = 'https://www.motorgraph.com/news/' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)
			
		return_data_dic['motorgraph_review_g'] = data_list
		review_list.append(return_data_dic)

	# 자동차 업계
	def industry() :
		url = 'https://www.motorgraph.com/news/articleList.html?page=1&total=1280&sc_section_code=&sc_sub_section_code=S2N15&sc_serial_code=&sc_area=&sc_level=&sc_article_type=&sc_view_level=&sc_sdate=&sc_edate=&sc_serial_number=&sc_word=&sc_word2=&sc_andor=&sc_order_by=E&view_type=sm'
		soup = get_soup(url)

		news_list = soup.find('section', attrs={'class': 'article-list-content'}).findAll('div', attrs={'class': 'list-block'})
		
		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'list-image'}).find('a')['href']
			img_url = news.find('div', attrs={'class': 'list-image'})['style'][22:-1]
			subject = news.find('div', attrs={'class': 'list-titles'}).find('strong').get_text().strip()
			summary = news.find('p', attrs={'class': 'list-summary'}).find('a').get_text().strip()
			reporter = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			reporter = re.search(r'\|(.*?)\|', reporter).group(1).strip()
			date = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()[-16:-6]
			data_group = {}
			data_group['link'] = 'https://www.motorgraph.com' + link
			data_group['img_url'] = 'https://www.motorgraph.com/news/' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)
			
		return_data_dic['motorgraph_industry'] = data_list
		industry_list.append(return_data_dic)

		# 본문 수집
	
	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=900).filter(news_content='')
		print('-'*30)
		print('모터그래프')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'https://www.motorgraph.com/news/articleView.html?idxno={newsList.values()[idx].get("news_code")}'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('div', attrs={'class': 'article-head-title'}).get_text().strip()
					d_content = soup.find('div', attrs={'id': 'articleBody'}).get_text().strip()
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 탑라이더
class GetTopRider() :
	# 신차
	def new() :
		url = 'http://www.top-rider.com/news/articleList.html?sc_sub_section_code=S2N3&view_type=sm'
		soup = get_soup(url)

		news_list = soup.find('section', attrs={'id': 'section-list'}).find('ul', attrs={'class': 'type2'}).findAll('li')
		
		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a', attrs={'class': 'thumb'})['href']
			img_url = news.find('a', attrs={'class': 'thumb'}).find('img')['src']
			subject = news.find('h4', attrs={'class': 'titles'}).find('a').get_text().strip()
			summary = news.find('p', attrs={'class': 'lead'}).get_text().strip()
			reporter = news.find('span', attrs={'class': 'byline'}).findAll('em')[1].get_text().strip()
			date = news.find('span', attrs={'class': 'byline'}).findAll('em')[2].get_text().strip()[0:10]
			data_group = {}
			data_group['link'] = 'http://www.top-rider.com' + link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['toprider_new'] = data_list
		new_car_list.append(return_data_dic)

	# 시승기
	def review() :
		url = 'http://www.top-rider.com/news/articleList.html?sc_section_code=S1N8&view_type=sm'
		soup = get_soup(url)

		news_list = soup.find('section', attrs={'id': 'section-list'}).find('ul', attrs={'class': 'type2'}).findAll('li')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a', attrs={'class': 'thumb'})['href']
			img_url = news.find('a', attrs={'class': 'thumb'}).find('img')['src']
			subject = news.find('h4', attrs={'class': 'titles'}).find('a').get_text().strip()
			summary = news.find('p', attrs={'class': 'lead'}).get_text().strip()
			reporter = news.find('span', attrs={'class': 'byline'}).findAll('em')[1].get_text().strip()
			date = news.find('span', attrs={'class': 'byline'}).findAll('em')[2].get_text().strip()[0:10]
			data_group = {}
			data_group['link'] = 'http://www.top-rider.com' + link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['toprider_review_k'] = data_list
		review_list.append(return_data_dic)

	# 자동차 업계
	def industry() :
		url = 'http://www.top-rider.com/news/articleList.html?sc_sub_section_code=S2N44&view_type=sm'
		soup = get_soup(url)

		news_list = soup.find('section', attrs={'id': 'section-list'}).find('ul', attrs={'class': 'type2'}).findAll('li')
		
		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('a', attrs={'class': 'thumb'})['href']
			img_url = news.find('a', attrs={'class': 'thumb'}).find('img')['src']
			subject = news.find('h4', attrs={'class': 'titles'}).find('a').get_text().strip()
			summary = news.find('p', attrs={'class': 'lead'}).get_text().strip()
			reporter = news.find('span', attrs={'class': 'byline'}).findAll('em')[1].get_text().strip()
			date = news.find('span', attrs={'class': 'byline'}).findAll('em')[2].get_text().strip()[0:10]
			data_group = {}
			data_group['link'] = 'http://www.top-rider.com' + link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)
			
		return_data_dic['toprider_industry'] = data_list
		industry_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=1000).filter(news_content='')
		print('-'*30)
		print('탑라이더')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.top-rider.com/news/articleView.html?idxno={newsList.values()[idx].get("news_code")}'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('h3', attrs={'class': 'heading'}).get_text().strip()
					d_content = soup.find('article', attrs={'id': 'article-view-content-div'}).get_text().strip()
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 글로벌 모터즈
class GetGlobalMotors() :
	# 신차 (국산)
	def new_k() :
		url = 'http://www.globalmotors.co.kr/list.php?ct=g010201&sidx=1'
		soup = get_soup(url)

		news_list = soup.find('div', attrs={'class': 'list_1d_con'}).findAll('li')
		
		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'w1'}).select_one('a')['href']
			img_url = news.find('div', attrs={'class': 'w1'}).select_one('a').find('img')['src']
			subject = news.find('div', attrs={'class': 'w2'}).select_one('.t1').get_text().strip()
			summary = news.find('div', attrs={'class': 'w2'}).select_one('.t3').find('a').get_text().strip()
			date = news.find('div', attrs={'class': 'w2'}).select_one('.t2').get_text().strip()[0:10]
			data_group = {}
			data_group['link'] = 'http://www.globalmotors.co.kr' + link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['globalmotors_new_k'] = data_list
		new_car_list.append(return_data_dic)

	# 신차 (수입)
	def new_g() :
		url = 'http://www.globalmotors.co.kr/list.php?ct=g010202&sidx=1'
		soup = get_soup(url)

		news_list = soup.find('div', attrs={'class': 'list_1d_con'}).findAll('li')
		
		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('div', attrs={'class': 'w1'}).select_one('a')['href']
			img_url = news.find('div', attrs={'class': 'w1'}).select_one('a').find('img')['src']
			subject = news.find('div', attrs={'class': 'w2'}).select_one('.t1').get_text().strip()
			summary = news.find('div', attrs={'class': 'w2'}).select_one('.t3').find('a').get_text().strip()
			date = news.find('div', attrs={'class': 'w2'}).select_one('.t2').get_text().strip()[0:10]
			data_group = {}
			data_group['link'] = 'http://www.globalmotors.co.kr' + link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['globalmotors_new_g'] = data_list
		new_car_list.append(return_data_dic)

	# 본문 수집
	@staticmethod
	def detail(dbconn, cursor) :
		newsList = TblTotalCarNewsList.objects.all().filter(media_code=1200).filter(news_content='')
		print('-'*30)
		print('글로벌모터즈')
		try :
			print('ㅡㅡㅡ'*30)
			for idx in range(len(newsList)) : 
				full_url = f'http://www.globalmotors.co.kr/view.php?ud={newsList.values()[idx].get("news_code")}_5&ssk=g010200'
				print(newsList.values()[idx].get('news_code'))
				try : 
					soup = get_soup(full_url)
					d_title = soup.find('div', attrs={'class': 'vcon_top_tit'}).find('h2').get_text().strip()
					d_content = soup.find('div', attrs={'class': 'text detailCont'}).get_text().strip()
					d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
					d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

					cursor.execute(f"""
						UPDATE TBL_TOTAL_CAR_NEWS_LIST 
						SET NEWS_TITLE = "{d_title}", NEWS_CONTENT = "{d_content}"
						WHERE NEWS_CODE = "{newsList.values()[idx].get('news_code')}" AND NEWS_CONTENT = ""
					""")
					time.sleep(3)
					print(f'{newsList.values()[idx].get("news_code")} :: 기사 본문 스크랩 완료! [{idx + 1} / {len(newsList)}]')
				except Exception as e :
					print(f'*+++++ + error! >> {e}')	
				print('ㅡㅡㅡ'*30)
		except Exception as e :
			print(f'***** + error! >> {e}')	
		finally : 
			pass

# 모터매거진
class GetMotorMagazine() : 
	# 자동차 업계
	def industry() :
		url = 'http://www.motormag.co.kr/list/6'
		soup = get_soup(url)

		news_list = soup.find('div', attrs={'class': 'slist_default'}).findAll('ul')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('li', attrs={'class': 'img'}).find('a')['href']
			img_url = news.find('li', attrs={'class': 'img'}).find('a').find('img')['src']
			subject = news.find('li', attrs={'class': 'title'}).find('a').get_text().strip()
			summary = ''
			reporter = ''
			date = ''
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)
			
		return_data_dic['motormagazine_industry'] = data_list
		industry_list.append(return_data_dic)

	# 시승기
	def review() :
		url = 'http://www.motormag.co.kr/list/4'
		soup = get_soup(url)

		news_list = soup.find('div', attrs={'class': 'slist_default'}).findAll('ul')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('li', attrs={'class': 'img'}).find('a')['href']
			img_url = news.find('li', attrs={'class': 'img'}).find('a').find('img')['src']
			subject = news.find('li', attrs={'class': 'title'}).find('a').get_text().strip()
			summary = ''
			reporter = ''
			date = ''
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['motormagazine_review'] = data_list
		# print(return_data_dic)
		review_list.append(return_data_dic)

# 카이즈유
class GetCarIsYou() :
	def new() : 
		url = 'https://www.carisyou.com/magazine/NEWCARINTRO'
		soup = get_soup(url)

		news_list = soup.find('div', attrs={'class': 'magazine_article_list'}).findAll('dl')

		data_list = []
		return_data_dic = {}

		for news in news_list :
			link = news.find('p', attrs={'class': 'title'}).find('a')['href']
			img_url = news.find('dt').find('a').find('img')['src']
			subject = news.find('p', attrs={'class': 'title'}).find('a').get_text().strip()
			summary = news.find('p', attrs={'class': 'text'}).find('a').get_text().strip()
			reporter = ''
			date = news.find('p', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'https://www.carisyou.com/magazine/NEWCARINTRO/' + link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['reporter'] = reporter
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['carisnew_new'] = data_list
		new_car_list.append(return_data_dic)


# 중고차 뉴스 모음
def get_used_car() :
	# GetAutoH.used()
	GetDailyCar.used()
	GetAutoMorning.used()

	return used_car_list

# 신차 뉴스 모음
def get_new_car() :
	GetAutoH.new()
	GetAutoview.new()
	GetItChosun.new()
	GetAutoMorning.new()
	# GetAutoDiary.new()
	GetMotorGraph.new()
	GetTopRider.new()
	GetGlobalMotors.new_k()
	GetGlobalMotors.new_g()
	GetCarIsYou.new()

	return new_car_list

# 시승기 모음
def get_review() :
	GetAutoH.review()
	GetDailyCar.review()
	GetAutoview.review()
	GetItChosun.review()
	GetAutoMorning.review()
	# GetAutoDiary.review()
	GetCarguy.review()
	GetTheDrive.review()
	GetMotorGraph.review_k()
	GetMotorGraph.review_g()
	GetTopRider.review()
	GetMotorMagazine.review()

	return review_list

# 자동차 업계 뉴스 모음
def get_industry() :
	GetAutoH.industry()
	GetDailyCar.industry()
	GetAutoview.industry()
	GetItChosun.industry()
	# GetAutoDiary.industry()
	GetCarguy.industry()
	GetTheDrive.industry()
	GetMotorGraph.industry()
	GetTopRider.industry()
	GetMotorMagazine.industry()

	return industry_list

# 기타 (보배드림) 뉴스 모음
	# GetBobaeDream.recommend()

	

# 중고차 뉴스 INSERT
def insert_used_db(dbconn, cursor) :
	try :
		print('**** 중고차 관련 기사 수집 시작!')
		
		media_code = 0
		media_name = ''
		news_code = 0
		for idx, news_list in enumerate(get_used_car()) :
			if idx == 0 :
				# # 오토헤럴드 (21.01.28 페이지 없어짐)
				# media_code = 100
				# media_name = '오토헤럴드'
				# 데일리카
				media_code = 200
				media_name = '데일리카'
			elif idx == 1 :
				# 오토모닝
				media_code = 500
				media_name = '오토모닝'
			for news_dict in news_list.values() :
				for news in news_dict : 
					if idx == 0 :
						# # 오토헤럴드 (21.01.28 페이지 없어짐)
						# news_code = news.get('link')[-15:]
						# url = f'http://autotimes.hankyung.com/apps/news.sub_view?popup=0&nid=05&c1=05&c2=02&c3=&nkey={news_code}'
						# 데일리카
						news_code = news.get('link')[61:66]
						url = f'http://www.dailycar.co.kr/content/news.html?type=view&autoId={news_code}&from=%2Fcontent%2Fnews.html%3Ftype%3Dlist%26sub%3Dsell%26maker%3Dused'
					elif idx == 1 :
						# 오토모닝
						news_code = news.get('link')[-5:]
						url = f'http://www.automorning.com/news/article.html?no={news_code}'

					subject = re.sub('\,', '&#44;', re.sub('[\"\'‘“”″′]', '&#8220;', news.get('subject')))
					summary = re.sub('\,', '&#44;', re.sub('[\"\'‘“”″′]', '&#8220;', news.get('summary')))
					reporter = news.get('reporter')
					img_url = news.get('img_url')
					date = news.get('date').replace('/', '-').replace('.', '-')

					cursor.execute(f"""
						INSERT IGNORE INTO TBL_TOTAL_CAR_NEWS_LIST 
						(
							MEDIA_CODE, NEWS_CATEGORY, MEDIA_NAME, 
							NEWS_CODE, NEWS_TITLE, 
							NEWS_SUMMARY, NEWS_CONTENT, REPORTER_NAME,
							NEWS_IMG_URL, NEWS_URL, WRITE_DATE, 
							ADD_DATE, MINING_STATUS
						) 
						VALUES (
							"{media_code}", 1, "{media_name}", 
							"{news_code}", "{subject}", 
							"{summary}", "수집 중입니다.", "{reporter}",
							"{img_url}", "{url}", "{date}", 
							NOW(), 1
						) 
					""")
	except Exception as e :
		print(f'***** + error! >> {e}')	
		pass
	finally : 
		print('**** 중고차 관련 기사 수집 및 DB저장 완료!')
		print('ㅡ'*50)

# 신차 뉴스 INSERT
def insert_new_db(dbconn, cursor) :
	try :
		print('**** 신차 관련 기사 수집 시작!')
		media_code = 0
		media_name = ''
		news_code = 0
		for idx, news_list in enumerate(get_new_car()) :
			if idx == 0 :
				# 오토헤럴드
				media_code = 100
				media_name = '오토헤럴드'
			elif idx == 1 :
				# 오토뷰
				media_code = 300
				media_name = '오토뷰'
			elif idx == 2 :
				# IT조선
				media_code = 400
				media_name = 'IT조선'
			elif idx == 3 :
				# 오토모닝
				media_code = 500
				media_name = '오토모닝'
			# elif idx == 4 :
			# 	# 오토다이어리
			# 	media_code = 600
			# 	media_name = '오토다이어리'
			elif idx == 4 :
				# 모터그래프
				media_code = 900
				media_name = '모터그래프'
			elif idx == 5 :
				# 탑라이더
				media_code = 1000
				media_name = '탑라이더'
			elif idx == 6 :
				# 글로벌모터즈 (국산)
				media_code = 1200
				media_name = '글로벌모터즈'
			elif idx == 7 : 
				# 글로벌모터즈 (수입)
				media_code = 1200
				media_name = '글로벌모터즈'
			elif idx == 8 : 
				# 카이즈유
				media_code = 1400
				media_name = '카이즈유'

			for news_dict in news_list.values() :
				for news in news_dict : 
					if idx == 0 :
						# 오토헤럴드
						news_code = news.get('link')[-15:]
						url = f'http://autotimes.hankyung.com/apps/news.sub_view?popup=0&nid=05&c1=05&c2=02&c3=&nkey={news_code}'
					elif idx == 1 :
						# 오토뷰
						news_code = news.get('link')[55:60]
						url = f'http://www.autoview.co.kr/content/article.asp?num_code={news_code}&news_section=new_car&pageshow=1'
					elif idx == 2 :
						# IT조선
						news_code = news.get('link')[39:]
						url = f'http://it.chosun.com/site/data/html_dir{news_code}'
					elif idx == 3 :
						# 오토모닝
						news_code = news.get('link')[-5:]
						url = f'http://www.automorning.com/news/article.html?no={news_code}'
					# elif idx == 4 :
					# 	# 오토다이어리
					# 	news_code = news.get('link')[-17:]
					# 	url = f'http://www.autodiary.kr{news_code}'
					elif idx == 4 : 
						# 모터그래프
						news_code = news.get('link')[-5:]
						url = f'https://www.motorgraph.com/news/articleView.html?idxno={news_code}'
					elif idx == 5 :
						# 탑라이더
						news_code = news.get('link')[-5:]
						url = f'http://www.top-rider.com/news/articleView.html?idxno={news_code}'
					elif idx == 6 :
						# 글로벌모터즈 (국산)
						news_code = news.get('link')[42:70]
						url = f'http://www.globalmotors.co.kr/view.php?ud={news_code}&ssk=g010201'
					elif idx == 7 :
						# 글로벌모터즈 (수입)
						news_code = news.get('link')[42:70]
						url = f'http://www.globalmotors.co.kr/view.php?ud={news_code}&ssk=g010202'
					elif idx == 8 :
						# 카이즈유
						news_code = news.get('link')[-5:]
						# https://www.carisyou.com/magazine/NEWCARINTRO/76712
						url = f'https://www.carisyou.com/magazine/NEWCARINTRO/{news_code}'

					subject = re.sub('\,', '&#44;', re.sub('[\"\'‘“”″′]', '&#8220;', news.get('subject')))
					summary = re.sub('\,', '&#44;', re.sub('[\"\'‘“”″′]', '&#8220;', news.get('summary')))
					reporter = news.get('reporter')
					img_url = news.get('img_url')
					date = news.get('date').replace('/', '-').replace('.', '-')

					cursor.execute(f"""
						INSERT IGNORE INTO TBL_TOTAL_CAR_NEWS_LIST 
						(
							MEDIA_CODE, NEWS_CATEGORY, MEDIA_NAME, 
							NEWS_CODE, NEWS_TITLE, 
							NEWS_SUMMARY, NEWS_CONTENT, REPORTER_NAME,
							NEWS_IMG_URL, NEWS_URL, WRITE_DATE, 
							ADD_DATE, MINING_STATUS
						) 
						VALUES (
							"{media_code}", 3, "{media_name}", 
							"{news_code}", "{subject}", 
							"{summary}", "", "{reporter}",
							"{img_url}", "{url}", "{date}", 
							NOW(), 1
						) 
					""")

	except Exception as e :
		print(f'***** + error! >> {e}')	
	finally : 
		print('**** 신차 관련 기사 수집 및 DB저장 완료!')
		print('ㅡ'*50)
	
# 시승기 INSERT
def insert_review_db(dbconn, cursor) :
	try :
		print('**** 시승기 수집 시작!')
		media_code = 0
		media_name = ''
		news_code = 0
		for idx, news_list in enumerate(get_review()) :
			if idx == 0 :
				# 오토헤럴드
				media_code = 100
				media_name = '오토헤럴드'
			elif idx == 1 :
				# 데일리카
				media_code = 200
				media_name = '데일리카'
			elif idx == 2 :
				# 오토뷰
				media_code = 300
				media_name = '오토뷰'
			elif idx == 3 :
				# IT조선
				media_code = 400
				media_name = 'IT조선'
			elif idx == 4 :
				# 오토모닝
				media_code = 500
				media_name = '오토모닝'
			# elif idx == 5 :
			# 	# 오토다이어리
			# 	media_code = 600
			# 	media_name = '오토다이어리'
			elif idx == 5 :
				# 카가이
				media_code = 700
				media_name = '카가이'
			elif idx == 6 :
				# 더드라이브
				media_code = 800
				media_name = '더드라이브'
			elif idx == 7 or idx == 8 :
				# 모터그래프
				media_code = 900
				media_name = '모터그래프'
			elif idx == 9 :
				# 탑라이더
				media_code = 1000
				media_name = '탑라이더'
			elif idx == 10 : 
				# 모터매거진
				media_code = 1300
				media_name = '모터매거진'

			for news_dict in news_list.values() :
				for news in news_dict : 
					if idx == 0 :
						# 오토헤럴드
						news_code = news.get('link')[-15:]
						url = f'http://autotimes.hankyung.com/apps/news.sub_view?popup=0&nid=06&c1=06&c2=&c3=&nkey={news_code}'
					elif idx == 1 :
						# 데일리카
						news_code = news.get('link')[61:66]
						url = f'http://www.dailycar.co.kr/content/news.html?type=view&autoId={news_code}&from=%2Fcontent%2Fnews.html'
					elif idx == 2 :
						# 오토뷰
						news_code = news.get('link')[78:83]
						url = f'http://www.autoview.co.kr/content/buyer_guide/guide_road_article.asp?num_code={news_code}&news_section=car_ride&pageshow=3'
					elif idx == 3 :
						# IT조선
						news_code = news.get('link')[39:]
						url = f'http://it.chosun.com/site/data/html_dir{news_code}'
					elif idx == 4 :
						# 오토모닝
						news_code = news.get('link')[-5:]
						url = f'http://www.automorning.com/news/article.html?no={news_code}'
					# elif idx == 5 :
					# 	# 오토다이어리
					# 	news_code = news.get('link')[-17:]
					# 	url = f'http://www.autodiary.kr{news_code}'
					elif idx == 5 :
						# 카가이
						news_code = news.get('link')[-5:]
						url = f'http://www.carguy.kr/news/articleView.html?idxno={news_code}'
					elif idx == 6 :
						# 더드라이브
						news_code = news.get('link')[-16:]
						url = f'http://www.thedrive.co.kr/news/newsview.php?ncode={news_code}'
					elif idx == 7 or idx == 8 :
						news_code = news.get('link')[-5:]
						url = f'https://www.motorgraph.com/news/articleView.html?idxno={news_code}'
					elif idx == 9 :
						news_code = news.get('link')[-5:]
						url = f'http://www.top-rider.com/news/articleView.html?idxno={news_code}'
					elif idx == 10 :
						news_code = news.get('link')[26:30]
						url = f'http://www.motormag.co.kr/{news_code}'

					subject = re.sub('\,', '&#44;', re.sub('[\"\'‘“”″′]', '&#8220;', news.get('subject')))
					summary = re.sub('\,', '&#44;', re.sub('[\"\'‘“”″′]', '&#8220;', news.get('summary')))
					reporter = news.get('reporter')
					img_url = news.get('img_url')
					date = news.get('date').replace('/', '-').replace('.', '-')
					cursor.execute(f"""
						INSERT IGNORE INTO TBL_TOTAL_CAR_NEWS_LIST 
						(
							MEDIA_CODE, NEWS_CATEGORY, MEDIA_NAME, 
							NEWS_CODE, NEWS_TITLE, 
							NEWS_SUMMARY, NEWS_CONTENT, REPORTER_NAME,
							NEWS_IMG_URL, NEWS_URL, WRITE_DATE, 
							ADD_DATE, MINING_STATUS
						) 
						VALUES (
							"{media_code}", 5, "{media_name}", 
							"{news_code}", "{subject}", 
							"{summary}", "", "{reporter}",
							"{img_url}", "{url}", "{date}", 
							NOW(), 1
						) 
					""")
		
	except Exception as e :
		print(f'***** + error! >> {e}')	
	finally : 
		print('**** 시승기 수집 및 DB저장 완료!')
		print('ㅡ'*50)

# 자동차 업계 뉴스 INSERT
def insert_industry_db(dbconn, cursor) :
	try :
		print('**** 자동차 업계 뉴스 수집 시작!')
		media_code = 0
		media_name = ''
		news_code = 0
		for idx, news_list in enumerate(get_industry()) :
			if idx == 0 :
				# 오토헤럴드
				media_code = 100
				media_name = '오토헤럴드'
			elif idx == 1 :
				# 데일리카
				media_code = 200
				media_name = '데일리카'
			elif idx == 2 :
				# 오토뷰
				media_code = 300
				media_name = '오토뷰'
			elif idx == 3 :
				# IT조선
				media_code = 400
				media_name = 'IT조선'
			# elif idx == 4 :
			# 	# 오토다이어리
			# 	media_code = 600
			# 	media_name = '오토다이어리'
			elif idx == 4 :
				# 카가이
				media_code = 700
				media_name = '카가이'
			elif idx == 5 :
				# 더드라이브
				media_code = 800
				media_name = '더드라이브'
			elif idx == 6 :
				# 모터그래프
				media_code = 900
				media_name = '모터그래프'
			elif idx == 7 :
				# 탑라이더
				media_code = 1000
				media_name = '탑라이더'
			elif idx == 8 : 
				media_code = 1300
				media_name = '모터매거진'

			for news_dict in news_list.values() :
				for news in news_dict : 
					if idx == 0 :
						# 오토헤럴드
						news_code = news.get('link')[-15:]
						url = f'http://autotimes.hankyung.com/apps/news.sub_view?popup=0&nid=06&c1=06&c2=&c3=&nkey={news_code}'
					elif idx == 1 :
						# 데일리카
						news_code = news.get('link')[61:66]
						url = f'http://www.dailycar.co.kr/content/news.html?type=view&autoId={news_code}&from=%2Fcontent%2Fnews.html'
					elif idx == 2 :
						# 오토뷰
						news_code = news.get('link')[78:83]
						url = f'http://www.autoview.co.kr/content/buyer_guide/guide_road_article.asp?num_code={news_code}&news_section=car_ride&pageshow=3'
					elif idx == 3 :
						# IT조선
						news_code = news.get('link')[39:]
						url = f'http://it.chosun.com/site/data/html_dir{news_code}'
					# elif idx == 4 :
					# 	# 오토다이어리
					# 	news_code = news.get('link')[-17:]
					# 	url = f'http://www.autodiary.kr{news_code}'
					elif idx == 4 :
						# 카가이
						news_code = news.get('link')[-5:]
						url = f'http://www.carguy.kr/news/articleView.html?idxno={news_code}'
					elif idx == 5 :
						# 더드라이브
						news_code = news.get('link')[-16:]
						url = f'http://www.thedrive.co.kr/news/newsview.php?ncode={news_code}'
					elif idx == 6 :
						# 모터그래프
						news_code = news.get('link')[-5:]
						url = f'https://www.motorgraph.com/news/articleView.html?idxno={news_code}'
					elif idx == 7 :
						# 탑라이더
						news_code = news.get('link')[-5:]
						url = f'http://www.top-rider.com/news/articleView.html?idxno={news_code}'
					elif idx == 8 : 
						news_code = news.get('link')[26:30]
						url = f'http://www.motormag.co.kr/{news_code}'

					subject = re.sub('\,', '&#44;', re.sub('[\"\'‘“”″′]', '&#8220;', news.get('subject')))
					summary = re.sub('\,', '&#44;', re.sub('[\"\'‘“”″′]', '&#8220;', news.get('summary')))
					reporter = news.get('reporter')
					img_url = news.get('img_url')
					date = news.get('date').replace('/', '-').replace('.', '-')

					cursor.execute(f"""
						INSERT IGNORE INTO TBL_TOTAL_CAR_NEWS_LIST 
						(
							MEDIA_CODE, NEWS_CATEGORY, MEDIA_NAME, 
							NEWS_CODE, NEWS_TITLE, 
							NEWS_SUMMARY, NEWS_CONTENT, REPORTER_NAME,
							NEWS_IMG_URL, NEWS_URL, WRITE_DATE, 
							ADD_DATE, MINING_STATUS
						) 
						VALUES (
							"{media_code}", 7, "{media_name}", 
							"{news_code}", "{subject}", 
							"{summary}", "", "{reporter}",
							"{img_url}", "{url}", "{date}", 
							NOW(), 1
						) 
					""")
		
	except Exception as e :
		print(f'***** + error! >> {e}')	
	finally : 
		print('**** 자동차 업계 뉴스 수집 및 DB저장 완료!')
		print('ㅡ'*50)


# 뉴스 목록 새로 수집
def reload_list_data() :
	now = time.localtime()
	start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	print('뉴스 받아오기 시작!')

	insert_used_db(dbconn, cursor)
	insert_new_db(dbconn, cursor)
	insert_review_db(dbconn, cursor)
	insert_industry_db(dbconn, cursor)

	dbconn.commit()
	dbconn.close()

	now = time.localtime()
	end_time = now
	print('ㅡ'*50)
	print('뉴스 받아오기 DB Commit/Close 완료!')
	print('뉴스 받아오기 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('뉴스 받아오기 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))

	
if __name__ == '__main__' : 
	# print(get_new_car())
	reload_list_data()