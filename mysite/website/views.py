from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from .models import TblTotalCarNewsList, TblMemberList, TblNewsKeywordList, TblNewsKeywordMap
from datetime import datetime
from django.http import HttpResponse
from django.core import serializers

from konlpy.tag import Kkma
from wordcloud import WordCloud
import regex
import json
# import matplotlib.pyplot as plt

import requests
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import mysql.connector

dbconn = mysql.connector.connect(host='118.27.37.85', user='car_news_zip', password='dbsgPwls!2', database='CAR_NEWS_ZIP', port='3366')

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
	browser = webdriver.Chrome(r'C:\Users\PC\Documents\simbyungki\git\autoplus\chromedriver.exe', options=options)
	browser.maximize_window()
	browser.get(url)
	time.sleep(2)
	soup = BeautifulSoup(browser.page_source, 'lxml')
	return soup


new_car_list = []
used_car_list = []
review_list = []
industry_list = []
now_dt = datetime.today().strftime('%Y.%m.%d %H:%M%S')

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

# IT조선
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
		date = h_news.find('span', attrs={'class': 'date'}).get_text().strip()
		data_group = {}
		data_group['link'] = link
		data_group['img_url'] = img_url
		data_group['subject'] = subject
		data_group['summary'] = summary
		data_group['date'] = date
		data_list.append(data_group)

		# normal
		for news in news_list :
			link = news.find('div', 'txt_wrap').find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('div', attrs={'class': 'txt_dot1'}).get_text().strip()
			summary = news.find('span', attrs={'class': 'txt_dot2'}).get_text().strip()
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
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
		date = h_news.find('span', attrs={'class': 'date'}).get_text().strip()
		data_group = {}
		data_group['link'] = link
		data_group['img_url'] = img_url
		data_group['subject'] = subject
		data_group['summary'] = summary
		data_group['date'] = date
		data_list.append(data_group)

		# normal
		for news in news_list :
			link = news.find('div', 'txt_wrap').find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('div', attrs={'class': 'txt_dot1'}).get_text().strip()
			summary = news.find('span', attrs={'class': 'txt_dot2'}).get_text().strip()
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
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
		date = h_news.find('span', attrs={'class': 'date'}).get_text().strip()
		data_group = {}
		data_group['link'] = link
		data_group['img_url'] = img_url
		data_group['subject'] = subject
		data_group['summary'] = summary
		data_group['date'] = date
		data_list.append(data_group)

		# normal
		for news in news_list :
			link = news.find('div', 'txt_wrap').find('a')['href']
			img_url = news.find('img')['src']
			subject = news.find('div', attrs={'class': 'txt_dot1'}).get_text().strip()
			summary = news.find('span', attrs={'class': 'txt_dot2'}).get_text().strip()
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date

			data_list.append(data_group)

		return_data_dic['chosun_industry'] = data_list
		industry_list.append(return_data_dic)

# 오토헤럴드
class GetAutoH() :
	# 오토헤럴드 국내 신차
	def new_k() :
		url = 'http://autotimes.hankyung.com/apps/news.sub_list?popup=0&nid=02&c1=02&c2=01&c3=&newscate=&isslide=&page=1'
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


		return_data_dic['autoh_new_k'] = data_list
		new_car_list.append(return_data_dic)

	# 오토헤럴드 국외 신차
	def new_g() :
		url = 'http://autotimes.hankyung.com/apps/news.sub_list?popup=0&nid=02&c1=02&c2=02&c3=&newscate=&isslide=&page=1'
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

		return_data_dic['autoh_new_g'] = data_list
		new_car_list.append(return_data_dic)

	# 오토헤럴드 중고차
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
		url = 'http://autotimes.hankyung.com/apps/news.sub_list?popup=0&nid=06&c1=06&c2=&c3=&newscate=&isslide=&page=1'
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

# 데일리카
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

# 오토모닝
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
			date = news.find('li', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
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
			date = news.find('li', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
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
			date = news.find('li', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = link
			data_group['img_url'] = img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[:10]

			data_list.append(data_group)

		return_data_dic['automoring_review'] = data_list
		review_list.append(return_data_dic)

# 오토다이어리
class GetAutoDiary() :
	# 오토다이어리 신차
	def new() :
		url = 'https://www.autodiary.kr/category/news/new-car/'
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
		url = 'https://www.autodiary.kr/category/news/car-business/'
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
		url = 'https://www.autodiary.kr/category/impression/'
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

# 카가이
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
			date = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.carguy.kr' + link
			data_group['img_url'] = 'http://www.carguy.kr/news' + img_url[22:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[-16:-6]

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
			date = news.find('div', attrs={'class': 'list-dated'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.carguy.kr' + link
			data_group['img_url'] = 'http://www.carguy.kr/news' + img_url[22:-1]
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[-16:-6]

			data_list.append(data_group)

		return_data_dic['carguy_review'] = data_list
		review_list.append(return_data_dic)

# 더드라이브
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
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.thedrive.co.kr' + link
			data_group['img_url'] = 'http://www.thedrive.co.kr' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[-16:]

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
			date = news.find('span', attrs={'class': 'date'}).get_text().strip()
			data_group = {}
			data_group['link'] = 'http://www.thedrive.co.kr' + link
			data_group['img_url'] = 'http://www.thedrive.co.kr' + img_url
			data_group['subject'] = subject
			data_group['summary'] = summary
			data_group['date'] = date[-16:]

			data_list.append(data_group)

		return_data_dic['drive_review'] = data_list
		review_list.append(return_data_dic)


# 신차 뉴스 모음
def get_new_car() :
	GetAutoH.new_k()
	GetAutoH.new_g()
	GetAutoview.new()
	GetItChosun.new()
	GetAutoMorning.new()
	GetAutoDiary.new()

	return new_car_list

# 중고차 뉴스 모음
def get_used_car() :
	GetAutoH.used()
	GetDailyCar.used()
	GetAutoMorning.used()

	return used_car_list

# 시승기 모음
def get_review() :
	GetAutoH.review()
	GetDailyCar.review()
	GetAutoview.review()
	GetItChosun.review()
	GetAutoMorning.review()
	GetAutoDiary.review()
	GetCarguy.review()
	GetTheDrive.review()

	return review_list

# 자동차 업계 뉴스 모음
def get_industry() :
	GetAutoH.industry()
	GetDailyCar.industry()
	GetAutoview.industry()
	GetItChosun.industry()
	GetAutoDiary.industry()
	GetCarguy.industry()
	GetTheDrive.industry()

	return industry_list


# 기사 DB INSERT
# Custom 쿼리 실행 함수
def execute(query, bufferd=True) :
	global dbconn
	try :
		cursor = dbconn.cursor(buffered=bufferd)
		cursor.execute(query)
	except Exception as e :
		dbconn.rollback()
		raise e

def execute2(query, bufferd=True) :
	global dbconn
	cursor = dbconn.cursor(buffered=bufferd)
	try :
		cursor.execute(query)
	except Exception as e :
		dbconn.rollback()
		raise e



# 중고차 뉴스 INSERT
def insert_used_db() :
	try :
		print('ㅡ'*50)
		print('중고차 관련 기사 수집 시작!')
		
		media_code = 0
		media_name = ''
		news_code = 0
		for idx, news_list in enumerate(get_used_car()) :
			if idx == 0 :
				# 오토헤럴드
				media_code = 100
				media_name = '오토헤럴드'
			elif idx == 1 :
				# 데일리카
				media_code = 200
				media_name = '데일리카'
			elif idx == 2 :
				# 데일리카
				media_code = 500
				media_name = '오토모닝'

			for news_dict in news_list.values() :
				for news in news_dict : 
					if idx == 0 :
						# 오토헤럴드
						news_code = news.get('link')[-15:]
						url = f'http://autotimes.hankyung.com/apps/news.sub_view?popup=0&nid=05&c1=05&c2=02&c3=&nkey={news_code}'
					elif idx == 1 :
						# 데일리카
						news_code = news.get('link')[61:66]
						url = f'http://www.dailycar.co.kr/content/news.html?type=view&autoId={news_code}&from=%2Fcontent%2Fnews.html%3Ftype%3Dlist%26sub%3Dsell%26maker%3Dused'
					elif idx == 2 :
						# 오토모닝
						news_code = news.get('link')[-5:]
						url = f'http://www.automorning.com/news/article.html?no={news_code}'

					subject = re.sub('[-=.#/?:$}\"\']', '', news.get('subject'))
					summary = re.sub('[-=.#/?:$}\"\']', '', news.get('summary'))
					img_url = news.get('img_url')
					date = news.get('date').replace('/', '-').replace('.', '-')

					# newUsedCarNews = TblUsedCarNewsList.objects.create(
					# 	MEDIA_CODE = media_code,
					# 	MEDIA_NAME = media_name,
					# 	NEWS_CODE = news_code,
					# 	NEWS_TITLE = subject,
					# 	NEWS_SUMMARY = summary,
					# 	NEWS_IMG_URL = img_url,
					# 	NEWS_URL = url,
					# 	WRITE_DATE = date,
					# 	ADD_DATE = now_dt
					# )

					execute(f"""
						INSERT IGNORE INTO TBL_TOTAL_CAR_NEWS_LIST 
						(
							MEDIA_CODE, NEWS_CATEGORY, MEDIA_NAME, 
							NEWS_CODE, NEWS_TITLE, 
							NEWS_SUMMARY, NEWS_CONTENT, NEWS_IMG_URL,
							NEWS_URL, WRITE_DATE, 
							ADD_DATE, MINING_STATUS
						) 
						VALUES (
							"{media_code}", 1, "{media_name}", 
							"{news_code}", "{subject}", 
							"{summary}", "", "{img_url}", 
							"{url}", "{date}", 
							NOW(), 1
						) 
					""")
		
	except Exception as e :
		print(f'***** + error! >> {e}')	
	finally : 
		dbconn.commit()
		
		print('ㅡ'*50)
		print('중고차 관련 기사 수집 및 DB저장 완료!')
		print('ㅡ'*50)

# 신차 뉴스 INSERT
def insert_new_db() :
	try :
		print('ㅡ'*50)
		print('신차 관련 기사 수집 시작!')
		media_code = 0
		media_name = ''
		news_code = 0
		for idx, news_list in enumerate(get_new_car()) :
			if idx == 0 or idx == 1 :
				# 오토헤럴드
				media_code = 100
				media_name = '오토헤럴드'
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
			elif idx == 5 :
				# 오토다이어리
				media_code = 600
				media_name = '오토다이어리'

			for news_dict in news_list.values() :
				for news in news_dict : 
					if idx == 0 or idx == 1 :
						# 오토헤럴드
						news_code = news.get('link')[-15:]
						url = f'http://autotimes.hankyung.com/apps/news.sub_view?popup=0&nid=05&c1=05&c2=02&c3=&nkey={news_code}'
					elif idx == 2 :
						# 오토뷰
						news_code = news.get('link')[55:60]
						url = f'http://www.autoview.co.kr/content/article.asp?num_code={news_code}&news_section=new_car&pageshow=1'
					elif idx == 3 :
						# IT조선
						news_code = news.get('link')[39:]
						url = f'http://it.chosun.com/site/data/html_dir{news_code}'
					elif idx == 4 :
						# 오토모닝
						news_code = news.get('link')[-5:]
						url = f'http://www.automorning.com/news/article.html?no={news_code}'
					elif idx == 5 :
						# 오토다이어리
						news_code = news.get('link')[-17:]
						url = f'https://www.autodiary.kr{news_code}'

					subject = re.sub('[-=.#/?:$}\"\']', '', news.get('subject')).replace('\"', '')
					summary = re.sub('[-=.#/?:$}\"\']', '', news.get('summary')).replace('\"', '')
					img_url = news.get('img_url')
					date = news.get('date').replace('/', '-').replace('.', '-')
					
					# newNewCarNews = TblNewCarNewsList.objects.create(
					# 	MEDIA_CODE = media_code,
					# 	MEDIA_NAME = media_name,
					# 	NEWS_CODE = news_code,
					# 	NEWS_TITLE = subject,
					# 	NEWS_SUMMARY = summary,
					# 	NEWS_IMG_URL = img_url,
					# 	NEWS_URL = url,
					# 	WRITE_DATE = date,
					# 	ADD_DATE = now_dt
					# )

					execute(f"""
						INSERT IGNORE INTO TBL_TOTAL_CAR_NEWS_LIST 
						(
							MEDIA_CODE, NEWS_CATEGORY, MEDIA_NAME, 
							NEWS_CODE, NEWS_TITLE, 
							NEWS_SUMMARY, NEWS_CONTENT, NEWS_IMG_URL,
							NEWS_URL, WRITE_DATE, 
							ADD_DATE, MINING_STATUS
						) 
						VALUES (
							"{media_code}", 3, "{media_name}", 
							"{news_code}", "{subject}", 
							"{summary}", "", "{img_url}", 
							"{url}", "{date}", 
							NOW(), 1
						) 
					""")

	except Exception as e :
		print(f'***** + error! >> {e}')	
	finally : 
		dbconn.commit()
		print('ㅡ'*50)
		print('신차 관련 기사 수집 및 DB저장 완료!')
		print('ㅡ'*50)
	
# 시승기 INSERT
def insert_review_db() :
	try :
		print('ㅡ'*50)
		print('시승기 수집 시작!')
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
			elif idx == 5 :
				# 오토다이어리
				media_code = 600
				media_name = '오토다이어리'
			elif idx == 6 :
				# 카가이
				media_code = 700
				media_name = '카가이'
			elif idx == 7 :
				# 더드라이브
				media_code = 800
				media_name = '더드라이브'

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
					elif idx == 5 :
						# 오토다이어리
						news_code = news.get('link')[-17:]
						url = f'https://www.autodiary.kr{news_code}'
					elif idx == 6 :
						# 카가이
						news_code = news.get('link')[-5:]
						url = f'http://www.carguy.kr/news/articleView.html?idxno={news_code}'
					elif idx == 7 :
						# 더드라이브
						news_code = news.get('link')[-16:]
						url = f'http://www.thedrive.co.kr/news/newsview.php?ncode={news_code}'
					

					subject = re.sub('[-=.#/?:$}\"\']', '', news.get('subject')).replace('\"', '')
					summary = re.sub('[-=.#/?:$}\"\']', '', news.get('summary')).replace('\"', '')
					img_url = news.get('img_url')
					date = news.get('date').replace('/', '-').replace('.', '-')

					# newReview = TblReviewList.objects.create(
					# 	MEDIA_CODE = media_code,
					# 	MEDIA_NAME = media_name,
					# 	NEWS_CODE = news_code,
					# 	NEWS_TITLE = subject,
					# 	NEWS_SUMMARY = summary,
					# 	NEWS_IMG_URL = img_url,
					# 	NEWS_URL = url,
					# 	WRITE_DATE = date,
					# 	ADD_DATE = now_dt
					# )

					execute(f"""
						INSERT IGNORE INTO TBL_TOTAL_CAR_NEWS_LIST 
						(
							MEDIA_CODE, NEWS_CATEGORY, MEDIA_NAME, 
							NEWS_CODE, NEWS_TITLE, 
							NEWS_SUMMARY, NEWS_CONTENT, NEWS_IMG_URL,
							NEWS_URL, WRITE_DATE, 
							ADD_DATE, MINING_STATUS
						) 
						VALUES (
							"{media_code}", 5, "{media_name}", 
							"{news_code}", "{subject}", 
							"{summary}", "", "{img_url}", 
							"{url}", "{date}", 
							NOW(), 1
						) 
					""")
		
	except Exception as e :
		print(f'***** + error! >> {e}')	
	finally : 
		dbconn.commit()
		print('ㅡ'*50)
		print('시승기 수집 및 DB저장 완료!')
		print('ㅡ'*50)

# 자동차 업계 뉴스 INSERT
def insert_industry_db() :
	try :
		print('ㅡ'*50)
		print('자동차 업계 뉴스 수집 시작!')
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
			elif idx == 4 :
				# 오토다이어리
				media_code = 600
				media_name = '오토다이어리'
			elif idx == 5 :
				# 카가이
				media_code = 700
				media_name = '카가이'
			elif idx == 6 :
				# 더드라이브
				media_code = 800
				media_name = '더드라이브'

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
						# 오토다이어리
						news_code = news.get('link')[-17:]
						url = f'https://www.autodiary.kr{news_code}'
					elif idx == 5 :
						# 카가이
						news_code = news.get('link')[-5:]
						url = f'http://www.carguy.kr/news/articleView.html?idxno={news_code}'
					elif idx == 6 :
						# 더드라이브
						news_code = news.get('link')[-16:]
						url = f'http://www.thedrive.co.kr/news/newsview.php?ncode={news_code}'

					subject = re.sub('[-=.#/?:$}]\"\'', '', news.get('subject')).replace('\"', '')
					summary = re.sub('[-=.#/?:$}]\"\'', '', news.get('summary')).replace('\"', '')
					img_url = news.get('img_url')
					date = news.get('date').replace('/', '-').replace('.', '-')

					# newIndustry = TblIndustryList.objects.create(
					# 	MEDIA_CODE = media_code,
					# 	MEDIA_NAME = media_name,
					# 	NEWS_CODE = news_code,
					# 	NEWS_TITLE = subject,
					# 	NEWS_SUMMARY = summary,
					# 	NEWS_IMG_URL = img_url,
					# 	NEWS_URL = url,
					# 	WRITE_DATE = date,
					# 	ADD_DATE = now_dt
					# )

					execute(f"""
						INSERT IGNORE INTO TBL_TOTAL_CAR_NEWS_LIST 
						(
							MEDIA_CODE, NEWS_CATEGORY, MEDIA_NAME, 
							NEWS_CODE, NEWS_TITLE, 
							NEWS_SUMMARY, NEWS_CONTENT, NEWS_IMG_URL,
							NEWS_URL, WRITE_DATE, 
							ADD_DATE, MINING_STATUS
						) 
						VALUES (
							"{media_code}", 7, "{media_name}", 
							"{news_code}", "{subject}", 
							"{summary}", "", "{img_url}", 
							"{url}", "{date}", 
							NOW(), 1
						) 
					""")
		
	except Exception as e :
		print(f'***** + error! >> {e}')	
	finally : 
		dbconn.commit()
		print('ㅡ'*50)
		print('자동차 업계 뉴스 수집 및 DB저장 완료!')
		print('ㅡ'*50)


# 뉴스 기사 상세 크롤링 > INSERT 
# 오토헤럴드
def get_auto_h_detail() :
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

				execute(f"""
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

		return redirect('/')

# 데일리카
def get_dailycar_detail() :
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
				
				d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
				d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

				execute(f"""
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
		dbconn.commit()
		print('DB Commit / Close 완료!')

		return redirect('/')

# 오토뷰
def get_autoview_detail() :
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

				execute(f"""
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
		dbconn.commit()
		print('DB Commit 완료!')
		
		return redirect('/')

# IT조선
def get_it_chosun_detail() :
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

				execute(f"""
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
		dbconn.commit()
		print('DB Commit 완료!')
		
		return redirect('/')

# 오토모닝
def get_auto_morning_detail() :
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

				execute(f"""
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
		dbconn.commit()
		print('DB Commit 완료!')
		
		return redirect('/')

# 오토다이어리
def get_auto_diary_detail() :
	newsList = TblTotalCarNewsList.objects.all().filter(media_code=600).filter(news_content='')
	print('-'*30)
	print('오토다이어리')
	try :
		print('ㅡㅡㅡ'*30)
		for idx in range(len(newsList)) : 
			full_url = f'https://www.autodiary.kr{newsList.values()[idx].get("news_code")}'
			print(newsList.values()[idx].get('news_code'))
			try : 
				soup = get_soup(full_url)
				d_title = soup.find('h2', attrs={'class': 'entry-title'}).get_text().strip()
				d_content = soup.find('div', attrs={'class': 'post-content'}).get_text().strip()
				d_title = re.sub('[-=.#/?:$}\"\']', '', d_title)
				d_content = re.sub('[-=.#/?:$}\"\']', '', d_content)

				execute(f"""
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
		dbconn.commit()
		print('DB Commit 완료!')
		
		return redirect('/')

# 카가이
def get_carguy_detail() :
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

				execute(f"""
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
		dbconn.commit()
		print('DB Commit 완료!')
		
		return redirect('/')

# 더드라이브
def get_the_drive_detail() :
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

				execute(f"""
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
		dbconn.commit()
		print('DB Commit 완료!')
		
		return redirect('/')


# 목록 데이터 다시 불러오기
def reload_list_data(request) :
	insert_used_db()
	insert_new_db()
	insert_review_db()
	insert_industry_db()

	dbconn.close()
	print('목록 데이터 다시 불러오기 DB Commit 완료!')
	print('목록 데이터 다시 불러오기 DB Close 완료!')

	return redirect('/')

# 뉴스 상세 내용 가져오기
def load_detail_data(request) :
	get_auto_h_detail()
	get_dailycar_detail()
	get_autoview_detail()
	get_it_chosun_detail()
	get_auto_morning_detail()
	get_auto_diary_detail()
	get_carguy_detail()
	get_the_drive_detail()
	
	dbconn.commit()
	print('뉴스 상세 내용 가져오기 DB Commit 완료!')
	dbconn.close()
	print('뉴스 상세 내용 가져오기 DB Close 완료!')

	return redirect('/')



# 목록
def news_list(request) :
	today_date = datetime.today().strftime('%Y-%m-%d')
	context = {'today_date': today_date}
	user_id = request.session.get('user')
	if user_id :
		memb_name = TblMemberList.objects.filter(memb_id=user_id).values()[0].get('memb_name')
		context['user'] = memb_name
	else : 
		context['user'] = None

	return render(request, 'website/news_list.html', context)

# 뉴스 목록 가져오기 ajax
def list_data(request) :
	news_list = TblTotalCarNewsList.objects.all()
	if request.method == 'GET' :
		idx = int(request.GET.get('list_idx'))
		list_type = request.GET.get('list_type')
		start_idx = int(request.GET.get('start_idx'))
		load_length = int(request.GET.get('load_length'))
		search_keyword = request.GET.get('search_keyword')
		category_num = 1
		
	news = ''
	if list_type == 'media' : 
		#오토헤럴드 : 100, 데일리카 : 200, 오토뷰 : 300, IT조선 : 400, 오토모닝 : 500, 오토다이어리 : 600, 카가이 : 700, 더드라이브 : 800
		if idx == 0 :
			category_num = 100
		elif idx == 1 : 
			category_num = 200
		elif idx == 2 :
			category_num = 300
		elif idx == 3 :
			category_num = 400
		elif idx == 4 :
			category_num = 500
		elif idx == 5 :
			category_num = 600
		elif idx == 6 :
			category_num = 700
		elif idx == 7 :
			category_num = 800
		news = news_list.filter(media_code=category_num).order_by('-write_date')
	elif list_type == 'category' :
		if idx == 0 :
			category_num = 1
		elif idx == 1 : 
			category_num = 3
		elif idx == 2 :
			category_num = 5
		elif idx == 3 :
			category_num = 7
		news = news_list.filter(news_category=category_num).order_by('-write_date')
	elif list_type == 'all' : 
		news = news_list.filter(news_content__icontains=search_keyword).order_by('-write_date')
	
	set_news = serializers.serialize('json', news[start_idx:start_idx+load_length])
	return JsonResponse({'news': set_news, 'total_length': len(news)}, status=200)
	# return HttpResponse(serializers.serialize('json', news[start_idx:start_idx+load_length]), content_type="text/json-comment-filtered")

# 뉴스 클릭 수 ajax
def view_count(request) : 
	if request.method == 'GET' : 
		now_count = int(request.GET.get('now_count'))
		news_code = request.GET.get('news_code')
		after_count = now_count + 1
		execute(f"""
			UPDATE TBL_TOTAL_CAR_NEWS_LIST 
			SET VIEW_COUNT = "{after_count}"
			WHERE NEWS_CODE = "{news_code}"
		""")

	return HttpResponse(after_count, content_type="text/json-comment-filtered")


# 뉴스 분석
mining_result_data = []
def text_mining(request) :
	kkma = Kkma()
	car_news_list = TblTotalCarNewsList.objects.all().filter(mining_status=1)
	news_keyword_map = TblNewsKeywordMap.objects.all()
	except_word_list = []
	except_keyword_list = []
	context = {}
	origin_sentence_list = []
	news_no = 0
	user_id = request.session.get('user')
	if user_id :
		memb_name = TblMemberList.objects.filter(memb_id=user_id).values()[0].get('memb_name')
		context['user'] = memb_name
	else : 
		context['user'] = None

	# print(car_news_list[0].news_summary)
	for idx in range(len(car_news_list) - 1) :
		re_content = regex.findall(r'[\p{Hangul}|\p{Latin}|\p{Han}]+', f'{car_news_list[idx].news_content}')
		origin_sentence_list.append(car_news_list[idx].news_summary)
		# print(re_summary)
		# print('-'*50)
		in_result_data = []
		in_result_data.append(car_news_list[idx].news_no)
		for word in re_content :
			in_result_word = []	
			group = []
			if (word not in except_word_list) :
				word_g = []
				word_g.append(word)
				group.append(word_g)
				# print(word)
				# print('-'*50)
				for keyword in kkma.pos(word) :
					if (keyword not in except_keyword_list) :
						# print(keyword)
						# print('-'*50)
						in_result_word.append(keyword)
				group.append(in_result_word)
			in_result_data.append(group)
		mining_result_data.append(in_result_data)

	# print(mining_result_data)
	
	for out_idx, data_list in enumerate(mining_result_data) :
		try :
			# print(data_list)
			if out_idx == (len(mining_result_data) -1) :
				print('ㅡ'*50)
				print('바깥쪽 break!')
				break
			else :
				for idx, data in enumerate(data_list) :
					try : 
						# idx = 0 >> 형태소 분석 전 단어
						if idx == 0 :
							news_no = data_list[0]
						elif idx == (len(data_list) -2) :
							print('ㅡ'*50)
							print('안쪽 break!')
							break
						else : 
							origin_word = re.sub('[-=.#/?:$}\"\']', '', str(data[0])).replace('[','').replace(']','')
							print(f'*** : [{out_idx}/{len(mining_result_data)}][{idx}/{len(data_list)}][{news_no}][{origin_word}]')
							print('-'*50)
							print(f'[{car_news_list[idx].news_no}] >> 분석 / INSERT / DB COMMIT 완료')
							print('-'*50)
							for word in data[1] :
								# print('>>> : ', word[0])
								# print('>>> : ', word[1])
								# print(f'{word[0]} / {word[1]} >>> INSERT')
								# INSERT
								execute2(f"""
									INSERT IGNORE INTO TBL_NEWS_KEYWORD_LIST 
									(
										WORD_MORPHEME, WORD_CLASS
									) 
									VALUES (
										"{word[0]}", "{word[1]}"
									)
								""")
								execute2(f"""
									INSERT IGNORE INTO TBL_NEWS_KEYWORD_MAP 
									(
										WORD_ORIGIN, WORD_MORPHEME,
										NEWS_NO, WORD_COUNT
									) 
									VALUES (
										"{origin_word}", "{word[0]}",
										"{news_no}", 1
									)
								""")
								print(f'[{idx}/{len(data_list)}][{origin_word}] >> {word[0]} / {word[1]} / KEYWORD 추가 및 뉴스 매핑 완료!')
								execute2(f"""
									UPDATE TBL_TOTAL_CAR_NEWS_LIST
									SET MINING_STATUS = 3
									WHERE NEWS_NO = {news_no}
								""")

								dbconn.commit()
					
					except Exception as e :
						print(f'****** + error! >> {e}')
						print('안쪽 오류로 프로그램 종료됨!')
					finally : 
						print('ㅡ'*50)
						print(f'[{out_idx}/{len(mining_result_data)}]>[{car_news_list[idx].news_no}] >> 분석 / INSERT / DB COMMIT 완료')
						print('ㅡ'*50)	
					
		except Exception as e :
			print(f'+++[{out_idx}/{len(mining_result_data)}]+++ + error! >> {e}')
			print('바깥쪽 오류로 프로그램 종료됨!')
		finally : 
			print('ㅡ'*50)
			print('바깥쪽 for문 종료')
			print('ㅡ'*50)
	
	dbconn.close()
	print('ㅡ'*50)
	print('DB CLOSE / 작업 완료!')
	return redirect('/text_mining_result/')

def text_mining_result(request) :
	global mining_result_data
	car_news_list = TblTotalCarNewsList.objects.all().filter(mining_status=1)
	today_date = datetime.today().strftime('%Y-%m-%d')
	context = {'today_date': today_date}
	user_id = request.session.get('user')
	if user_id :
		memb_name = TblMemberList.objects.filter(memb_id=user_id).values()[0].get('memb_name')
		context['user'] = memb_name
	else : 
		context['user'] = None
	
	origin_sentence_list = []

	for idx in range(len(car_news_list)) :
		origin_sentence_list.append(car_news_list[idx].news_summary)

	context['mining_result_list'] = mining_result_data
	context['origin_sentence_list'] = origin_sentence_list
	return render(request, 'website/text_mining_result.html', context)

# 회원
def login(request) :
	newsList = TblTotalCarNewsList.objects.all().filter(media_code=100)
	context = {'page_group': 'login-p'}
	user_id = request.session.get('user')
	if user_id :
		memb_name = TblMemberList.objects.filter(memb_id=user_id).values()[0].get('memb_name')
		context['user'] = memb_name
	else : 
		context['user'] = None

	if request.method == 'POST' : 
		memb_id = request.POST['memb-id']
		password = request.POST['pw']
		
		if TblMemberList.objects.filter(memb_id = memb_id, password = password).exists() == True :
			request.session['user'] = memb_id
			return redirect('/')
		else :
			return render(request, 'website/login.html', context)
	else :
		return render(request, 'website/login.html', context)

def logout(request) : 
	if request.session.get('user') : 
		del request.session['user']

	return redirect('/')

def join(request) : 
	context = {'page_group': 'join-p'}
	user_id = request.session.get('user')
	if user_id :
		memb_name = TblMemberList.objects.filter(memb_id=user_id).values()[0].get('memb_name')
		context['user'] = memb_name
	else : 
		context['user'] = None

	if request.method == 'POST' : 
		memb_id = request.POST.get('memb-id', None)
		memb_name = request.POST.get('memb-name', None)
		gender = request.POST.get('gender', None)
		password = request.POST.get('pw', None)
		re_password = request.POST.get('re-pw', None)
		if not (memb_id and gender and password and re_password) : 
			context['error'] = '* 모든 값을 입력해주세요.'
			return render(request, 'website/join.html', context)
		elif password != re_password : 
			context['error'] = '* 비밀번호가 다릅니다.'
			context = {
				'memb_id': memb_id,
				'memb_name': memb_name,
				'gender': gender
			}
			return render(request, 'website/join.html', context)
		elif TblMemberList.objects.filter(memb_id = memb_id).exists() == True : 
			context['error'] = '* 이미 존재하는 아이디입니다.'
			context = {
				'memb_name': memb_name,
				'gender': gender
			}
			return render(request, 'website/join.html', context)
		else :
			new_member = TblMemberList(
				memb_id = memb_id,
				memb_name = memb_name,
				gender = gender,
				password = password
			)
			new_member.save()

			context['join_result'] = 'success'

			print(f'회원가입 완료! >> {memb_id}({gender})')
			return redirect('/login/')
	else : 
		return render(request, 'website/join.html', context)
