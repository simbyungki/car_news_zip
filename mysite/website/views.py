from django.shortcuts import render, redirect
from .models import TblUsedCarNewsList
from .models import TblNewCarNewsList
from .models import TblReviewList
from .models import TblIndustryList
from datetime import datetime

import requests
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import mysql.connector

# dbconn = mysql.connector.connect(host='139.150.79.124', user='AP_ATC_INSP', password='autoplus2020!', database='AP_ATC_INSP', port="3306")

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

# 오토뷰 신차
def get_autoview_new() :
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
def get_autoview_industry() :
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
def get_autoview_review() :
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


# IT조선 신차	
def get_chosun_new() :
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
def get_chosun_review() :
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
def get_chosun_industry() :
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


# 오토헤럴드 국내 신차
def get_autoh_new_k() :
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

		# 상위 10개만 가져오기
		if idx == 9 :
			break


	return_data_dic['autoh_new_k'] = data_list
	new_car_list.append(return_data_dic)

# 오토헤럴드 국외 신차
def get_autoh_new_g() :
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

		# 상위 10개만 가져오기
		if idx == 9 :
			break

	return_data_dic['autoh_new_g'] = data_list
	new_car_list.append(return_data_dic)

# 오토헤럴드 중고차
def get_autoh_used() : 
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

		# 상위 10개만 가져오기
		if idx == 9 :
			break

	return_data_dic['autoh_used'] = data_list
	used_car_list.append(return_data_dic)

# 오토헤럴드 시승기
def get_autoh_review() :
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

		# 상위 10개만 가져오기
		if idx == 9 :
			break

	return_data_dic['autoh_review'] = data_list
	review_list.append(return_data_dic)

# 오토헤럴드 자동차 업계
def get_autoh_industry() :
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

		# 상위 10개만 가져오기
		if idx == 9 :
			break

	return_data_dic['autoh_industry'] = data_list
	industry_list.append(return_data_dic)


# 데일리카 중고차
def get_daily_used() :
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

			# 상위 10개만 가져오기
			# if idx == 9 :
			# 	break

	return_data_dic['daily_used'] = data_list
	used_car_list.append(return_data_dic)

# 데일리카 시승기
def get_daily_review() :
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

			# 상위 10개만 가져오기
			# if idx == 9 :
			# 	break

	return_data_dic['daily_review'] = data_list
	review_list.append(return_data_dic)

# 데일리카 자동차 업계
def get_daily_industry() :
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

			# 상위 10개만 가져오기
			# if idx == 9 :
			# 	break

	return_data_dic['daily_industry'] = data_list
	industry_list.append(return_data_dic)


# 오토모닝 신차
def get_automorning_new() :
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
		data_group['date'] = date

		data_list.append(data_group)

	return_data_dic['automoring_new'] = data_list
	new_car_list.append(return_data_dic)

# 오토모닝 중고차
def get_automorning_used() :
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
def get_automorning_review() :
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
		data_group['date'] = date

		data_list.append(data_group)

	return_data_dic['automoring_review'] = data_list
	review_list.append(return_data_dic)


# 오토다이어리 신차
def get_autodiary_new() :
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
def get_autodiary_industry() :
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
def get_autodiary_review() :
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


# 카가이 자동차 업계
def get_carguy_industry() :
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
def get_carguy_review() :
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


# 더드라이브 자동차 업계
def get_drive_industry() :
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
def get_drive_review() :
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
	get_autoh_new_k()
	get_autoh_new_g()
	get_autoview_new()
	get_chosun_new()
	get_automorning_new()
	get_autodiary_new()

	return new_car_list

# 중고차 뉴스 모음
def get_used_car() :
	get_autoh_used()
	get_daily_used()
	get_automorning_used()

	return used_car_list

# 시승기 모음
def get_review() :
	get_autoh_review()
	get_daily_review()
	get_autoview_review()
	get_chosun_review()
	get_automorning_review()
	get_autodiary_review()
	get_carguy_review()
	get_drive_review()

	return review_list

# 자동차 업계 뉴스 모음
def get_industry() :
	get_autoh_industry()
	get_daily_industry()
	get_autoview_industry()
	get_chosun_industry()
	get_autodiary_industry()
	get_carguy_industry()
	get_drive_industry()

	return industry_list


# 기사 DB INSERT
# Custom 쿼리 실행 함수
def execute(query, bufferd=True) :
	global dbconn
	try :
		cursor = dbconn.cursor(buffered=bufferd)
		cursor.execute(query)
		dbconn.commit()
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
					execute(f"""
							INSERT IGNORE INTO TBL_USED_CAR_NEWS_LIST 
							(
								MEDIA_CODE, MEDIA_NAME, 
								NEWS_CODE, NEWS_TITLE, 
								NEWS_CONTENT, NEWS_IMG_URL,
								NEWS_URL, WRITE_DATE, 
								ADD_DATE
							) 
							VALUES (
								"{media_code}", "{media_name}", 
								"{news_code}", "{subject}", 
								"{summary}", "{img_url}", 
								"{url}", "{date}", 
								NOW()
							) 
						""")
		
		print('ㅡ'*50)
		print('중고차 관련 기사 수집 및 DB저장 완료!')
		print('ㅡ'*50)
	except Exception as e :
		print(e)
	finally : 
		pass

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
					execute(f"""
							INSERT IGNORE INTO TBL_NEW_CAR_NEWS_LIST 
							(
								MEDIA_CODE, MEDIA_NAME, 
								NEWS_CODE, NEWS_TITLE, 
								NEWS_CONTENT, NEWS_IMG_URL,
								NEWS_URL, WRITE_DATE, 
								ADD_DATE
							) 
							VALUES (
								"{media_code}", "{media_name}", 
								"{news_code}", "{subject}", 
								"{summary}", "{img_url}", 
								"{url}", "{date}", 
								NOW()
							) 
						""")

		print('ㅡ'*50)
		print('신차 관련 기사 수집 및 DB저장 완료!')
		print('ㅡ'*50)
	except Exception as e :
		print(e)
	finally : 
		pass
	
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
					execute(f"""
							INSERT IGNORE INTO TBL_REVIEW_LIST 
							(
								MEDIA_CODE, MEDIA_NAME, 
								NEWS_CODE, NEWS_TITLE, 
								NEWS_CONTENT, NEWS_IMG_URL,
								NEWS_URL, WRITE_DATE, 
								ADD_DATE
							) 
							VALUES (
								"{media_code}", "{media_name}", 
								"{news_code}", "{subject}", 
								"{summary}", "{img_url}", 
								"{url}", "{date}", 
								NOW()
							) 
						""")
		print('ㅡ'*50)
		print('시승기 수집 및 DB저장 완료!')
		print('ㅡ'*50)
	except Exception as e :
		print(e)
	finally : 
		pass

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
					execute(f"""
							INSERT IGNORE INTO TBL_INDUSTRY_LIST 
							(
								MEDIA_CODE, MEDIA_NAME, 
								NEWS_CODE, NEWS_TITLE, 
								NEWS_CONTENT, NEWS_IMG_URL,
								NEWS_URL, WRITE_DATE, 
								ADD_DATE
							) 
							VALUES (
								"{media_code}", "{media_name}", 
								"{news_code}", "{subject}", 
								"{summary}", "{img_url}", 
								"{url}", "{date}", 
								NOW()
							) 
						""")
		print('ㅡ'*50)
		print('자동차 업계 뉴스 수집 및 DB저장 완료!')
		print('ㅡ'*50)
	except Exception as e :
		print(e)
	finally : 
		pass



# 데이터 다시 불러오기
def reload_data(request) :
	cursor = dbconn.cursor()

	insert_used_db()
	insert_new_db()
	insert_review_db()
	insert_industry_db()

	dbconn.commit()
	print('DB Commit 완료!')
	dbconn.close()
	print('DB Close 완료!')

	return redirect('/')

# 목록
def news_list(request) :
	today_date = datetime.today().strftime('%Y-%m-%d')
	used_news_list = TblUsedCarNewsList.objects.all().order_by('-write_date')
	new_news_list = TblNewCarNewsList.objects.all().order_by('-write_date')
	review_list = TblReviewList.objects.all().order_by('-write_date')
	industry_list = TblIndustryList.objects.all().order_by('-write_date')
	return render(request, 'website/news_list.html', {
		'used_news_list': used_news_list, 
		'today_date': today_date, 
		'new_news_list': new_news_list, 
		'review_list': review_list, 
		'industry_list': industry_list,
	})