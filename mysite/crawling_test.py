import requests
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'DES-CBC3-SHA'
import re
import regex
import time
import os, json
from datetime import datetime
from bs4 import BeautifulSoup

def get_soup(url) :
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
	res = requests.get(url, headers = headers, verify = False)
	res.raise_for_status()
	res.encoding=None
	soup = BeautifulSoup(res.text, 'lxml')
	return soup

###
# 뉴스 목록 콘텐츠 가져오기
###
def get_news_list() :
	page_number = 1
	total_news = []
	for idx in range(1) : 
		page_number = idx + 1
		print(f'>> {page_number}번 페이지 작업 시작합니다.')
		url = f'https://www.bobaedream.co.kr/list?code=national&s_cate=&maker_no=&model_no=&or_gu=10&or_se=desc&s_selday=&pagescale=30&info3=&noticeShow=&s_select=Subject&s_key=&level_no=&vdate=&type=list&page={page_number}'
		soup = get_soup(url)
		tr_list = soup.select('#boardlist tbody tr["itemtype"]')
		# print(len(board_list))
		for idx, tr in enumerate(tr_list) :
			tr_no = tr.select_one('.num01').get_text().strip()
			# link_url = tr.select_one('.bsubject')['href']
			news_code = tr.select_one('.bsubject')['href'][-12:-5]
			title = tr.select_one('.bsubject').get_text().strip()
			writer = tr.select_one('.author').get_text().strip()
			date = tr.select_one('.date').get_text().strip()
			# print(tr_no, link_url, title, writer, date)
			in_obj = {}
			in_obj['tr_no'] = tr_no
			in_obj['news_code'] = news_code
			in_obj['title'] = title
			in_obj['writer'] = writer
			in_obj['date'] = date
			total_news.append(in_obj)    
			time.sleep(0.2)
	print(f'>>>> 총 {len(total_news)}개의 뉴스 수집 완료!')
	return total_news


# print(get_news_list())


###
# 뉴스 상세 콘텐츠 가져오기
###
def get_news_detail(cont_no) : 
	print(f'>> 뉴스 상세 내용 수집 시작합니다.')
	url = f'https://www.bobaedream.co.kr/view?code=national&No={cont_no}&bm=1'
	soup = get_soup(url)
	detail = soup.select_one('#print_area')
	title = detail.select_one('.writerProfile dl dt strong').get_text().strip()
	content = detail.select_one('.bodyCont').get_text().strip()
	print(title, content)
	# for news in total_news : 
	# 	# print(news)
	# 	cont_no = news['news_code']
	# 	url = f'https://www.bobaedream.co.kr/view?code=national&No={cont_no}&bm=1'
	# 	soup = get_soup(url)
	# 	detail = soup.select_one('#print_area')
	# 	title = detail.select_one('.writerProfile dl dt strong').get_text().strip()
	# 	content = detail.select_one('.bodyCont').get_text().strip()
	# 	news['title'] = title
	# 	news['content'] = content
	# 	time.sleep(0.5)
	# print(total_news)

get_news_detail('2051646')

# total_news = [{'news_code': '2051688', 'title': '없다', 'content': '없다'}]
# get_news_detail(total_news)