import requests
import time
import schedule
import re
import regex
import mysql.connector
import os, json
import traceback
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
## 장고 프로젝트를 사용할 수 있도록 환경을 구축
import django
django.setup()

from website.models import TblTotalCarNewsList, TblMemberList, TblNewsKeywordList, TblNewsKeywordMap
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

new_car_list = []
used_car_list = []
review_list = []
industry_list = []



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath('./mysite'))
# SECURITY WARNING: keep the secret key used in production secret!
db_info_file = os.path.join(BASE_DIR, 'db_conn.json')
with open(db_info_file) as f :
	db_infos = json.loads(f.read())


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

# 오토뷰
class GetAutoview() :
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


# 뉴스 본문 수집
def load_detail_data() :
	now = time.localtime()
	start_time = now

	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	now = time.localtime()
	print('뉴스 상세 내용 가져오기 시작!')

	GetAutoH.detail(dbconn, cursor)
	GetDailyCar.detail(dbconn, cursor)
	GetAutoview.detail(dbconn, cursor)
	GetItChosun.detail(dbconn, cursor)
	GetAutoMorning.detail(dbconn, cursor)
	# GetAutoDiary.detail(dbconn, cursor)
	GetCarguy.detail(dbconn, cursor)
	GetTheDrive.detail(dbconn, cursor)
	GetMotorGraph.detail(dbconn, cursor)
	
	print('뉴스 상세 내용 가져오기 완료!')
	dbconn.commit()
	dbconn.close()

	now = time.localtime()
	end_time = now
	print('ㅡ'*50)
	print('뉴스 상세 내용 가져오기 DB Commit/Close 완료!')
	print('뉴스 상세 내용 가져오기 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('뉴스 상세 내용 가져오기 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))
	
				
	
# SQL 실행
def get_conn_cursor() :
	try:
		dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
		cursor = dbconn.cursor(dictionary=True)
		cursor.execute('SELECT NOW();')
		return dbconn, cursor
	except Exception:
		traceback.print_stack()
		print('재시도')
		return get_conn_cursor()



if __name__ == '__main__' : 
	load_detail_data()
