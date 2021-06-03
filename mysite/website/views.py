from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.db.models import Q
from .models import TblTotalCarNewsList, TblMemberList, TblNewsKeywordList, TblNewsKeywordMap, TblYoutubeCarCommentList, TblCarInfos, TblNewsAllKeywordList, TblNewsCarModelMap
from datetime import datetime
from django.http import HttpResponse
from django.core import serializers

import requests
import pandas as pd
import time
import mysql.connector
import pymssql
import os, json
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

# 보배드림 수집
from bs4 import BeautifulSoup
# BeautifulSoup
def get_soup(url) :
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
	res = requests.get(url, headers=headers)
	res.raise_for_status()
	res.encoding=None
	soup = BeautifulSoup(res.text, 'lxml')
	return soup

# 보배드림
today_year = 0
today_month = 0
class GetBobaeDream() :
	# 추천
	def recommend() :
		global today_year
		global today_month
		today_year = datetime.today().year
		today_month = datetime.today().month
		if today_month < 10 :
			today_month = '0' + str(today_month-1)

		url = 'https://bobaedream.co.kr/list.php?code=nnews&s_cate=&maker_no=&model_no=&or_gu=30&or_se=desc&s_selday=&pagescale=30&info3=&noticeShow=&bestCode=&bestDays=&bestbbs=&vdate=&ndate=&nmdate=&s_select=Subject&s_key='
		soup = get_soup(url)

		news_list = soup.select('table.clistTable02 tbody tr')
		# print(news_list)
		
		etc_list = []
		data_list = []
		return_data_dic = {}

		for idx, news in enumerate(news_list) :
			if idx > 4 :
				date = news.find('td', attrs={'class': 'date'}).get_text().strip()
				if today_month == date[:2] :
					print(f'이번달 뉴스 = {news.find("a", attrs={"class": "bsubject"}).get_text().strip()}')
					link = news.find('a', attrs={'class': 'bsubject'})['href']

					photo_dom = news.find('td', attrs={'class': 'photo01'})
					if photo_dom is not None :
						img_url = photo_dom.find('img')['src']
					else : 
						img_url = ''

					summary_dom = news.find('li', attrs={'class': 'board_list_text_02'})
					if summary_dom is not None :
						summary = summary_dom.get_text().strip()
					else : 
						summary = ''

					subject = news.find('a', attrs={'class': 'bsubject'}).get_text().strip()
					date = date.replace('/', '-')
					view_count = news.find('td', attrs={'class': 'count'}).get_text()
					recommend_count = news.find('td', attrs={'class': 'recomm'}).get_text()

					data_group = {}
					data_group['link'] = 'https://www.bobaedream.co.kr' + link
					data_group['img_url'] = 'https:' + img_url
					data_group['subject'] = subject
					data_group['summary'] = summary
					data_group['reporter'] = ''
					data_group['date'] = str(today_year) + '-' + date
					data_group['view_count'] = int(view_count)
					data_group['recommend_count'] = recommend_count

					data_list.append(data_group)

		return_data_dic['bobaedream_recoomend'] = data_list
		etc_list.append(return_data_dic)

		return etc_list

	# 조회수
	def viewCount() :
		today_year = datetime.today().year
		today_month = datetime.today().month
		if today_month < 10 :
			today_month = '0' + str(today_month-1)

		url = 'https://bobaedream.co.kr/list.php?code=nnews&s_cate=&maker_no=&model_no=&or_gu=20&or_se=desc&s_selday=&pagescale=30&info3=&noticeShow=&bestCode=&bestDays=&bestbbs=&vdate=&ndate=&nmdate=&s_select=Subject&s_key='
		soup = get_soup(url)

		news_list = soup.select('table.clistTable02 tbody tr')
		# print(news_list)
		
		etc_list = []
		data_list = []
		return_data_dic = {}

		for idx, news in enumerate(news_list) :
			if idx > 4 :
				date = news.find('td', attrs={'class': 'date'}).get_text().strip()
				if today_month == date[:2] :
					print(f'이번달 뉴스 = {news.find("a", attrs={"class": "bsubject"}).get_text().strip()}')
					link = news.find('a', attrs={'class': 'bsubject'})['href']

					photo_dom = news.find('td', attrs={'class': 'photo01'})
					if photo_dom is not None :
						img_url = photo_dom.find('img')['src']
					else : 
						img_url = ''

					summary_dom = news.find('li', attrs={'class': 'board_list_text_02'})
					if summary_dom is not None :
						summary = summary_dom.get_text().strip()
					else : 
						summary = ''

					subject = news.find('a', attrs={'class': 'bsubject'}).get_text().strip()
					date = date.replace('/', '-')
					view_count = news.find('td', attrs={'class': 'count'}).get_text()
					recommend_count = news.find('td', attrs={'class': 'recomm'}).get_text()

					data_group = {}
					data_group['link'] = 'https://www.bobaedream.co.kr' + link
					data_group['img_url'] = 'https:' + img_url
					data_group['subject'] = subject
					data_group['summary'] = summary
					data_group['reporter'] = ''
					data_group['date'] = str(today_year) + '-' + date
					data_group['view_count'] = int(view_count)
					data_group['recommend_count'] = recommend_count

					data_list.append(data_group)

		return_data_dic['bobaedream_view_count'] = data_list
		etc_list.append(return_data_dic)

		return etc_list


# 접속자 IP
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def connect_log_insert(infos) :
	today_date = datetime.today().strftime('%Y-%m-%d')
	now_time = datetime.today().strftime('%H:%M:%S')
	
	dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
	cursor = dbconn.cursor()

	# LOG DB INSERT
	try : 
		cursor.execute(f"""
			INSERT INTO LOG_CONNECT_LIST (
				PAGE_NAME, REFERER_URL, USER_IP, 
				CONNECT_YMD, CONNECT_TIME, CONNECT_DATE
			) 
			VALUES (
				"{infos.get('page_name')}", "{infos.get('referer')}", "{infos.get('user_ip')}", 
				"{today_date}", "{now_time}", NOW()
			)
		""")
	except Exception as e :
		print(f'****** + error! >> {e} >> 오류!')
	else :
		dbconn.commit()
		dbconn.close()
		print(f'[{today_date} {now_time}][{infos.get("user_ip")}] >> {infos.get("page_name")} >> Log commit 완료')
		print(cursor.rowcount, "record Inserted.") 

def search_log_insert(infos) : 
	today_date = datetime.today().strftime('%Y-%m-%d')
	now_time = datetime.today().strftime('%H:%M:%S')
	try : 
		dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
		cursor = dbconn.cursor()
		cursor.execute(f"""
			INSERT INTO LOG_SEARCH_LIST (
				SEARCH_WORD, SEARCH_RETURN_COUNT, SEARCHER_IP, 
				SEARCH_YMD, SEARCH_TIME, SEARCH_DATE
			) 
			VALUES (
				"{infos.get('search_keyword')}", {infos.get('search_result_count')}, "{infos.get('searcher_ip')}", 
				"{today_date}", "{now_time}", NOW()
			)
		""")
	except Exception as e :
		print(f'****** + error! >> {e} >> 오류!')
	else :
		dbconn.commit()
		dbconn.close()
		print(f'[{today_date} {now_time}][{infos.get("searcher_ip")}] >> {infos.get("search_keyword")} >> Log commit 완료')
		# print(cursor.rowcount, "record Inserted.") 

# 목록
def news_list(request) :
	context = {}
	context['today_date'] = datetime.today().strftime('%Y-%m-%d')
	context['page_group'] = 'news-list-p'
	user_id = request.session.get('user')
	if user_id :
		memb_name = TblMemberList.objects.filter(memb_id=user_id).values()[0].get('memb_name')
		context['user'] = memb_name
	else : 
		context['user'] = None

	infos = {}
	infos['referer'] = request.headers.get('referer')
	infos['page_name'] = '/news_list'
	infos['user_ip'] = get_ip(request)
	connect_log_insert(infos)
	
	return render(request, 'website/news_list.html', context)

# 뉴스 상세
def news_detail(request) : 
	news_code = request.GET.get('news_code')
	keyword = request.GET.get('keyword')
	news = TblTotalCarNewsList.objects.values().filter(news_code=news_code)
	context = {}
	context['today_date'] = datetime.today().strftime('%Y-%m-%d')
	context['news'] = news[0]
	context['keyword'] = keyword
	context['page_group'] = 'news-detail-p'

	infos = {}
	infos['referer'] = request.headers.get('referer')
	infos['page_name'] = '/news_detail'
	infos['user_ip'] = get_ip(request)
	connect_log_insert(infos)

	return render(request, 'website/news_detail.html', context)



# 뉴스, 카 매핑 테이블
def boname_to_car_infos(bonames) : 
	matching_car_list = []
	#print(bonames)
	for boname in bonames : 
		url = 'http://182.162.143.85/getCarListTotal.php'
		params = {'searchQuery': boname, 'productType': 9}
		res = requests.get(url, params)
		# print(res.status_code)
		# print(res.headers['content-type'])
		# print(res.encoding)
		# print(res.text)
		# print(res.json())
		# print(res.json()['resultData'])

		if isinstance(res.json()['resultData'], dict) :
			if res.json()['resultData']['ALL_TOTAL'] > 0 : 
				print(f'boname >> {res.json()["resultData"]["ALL_TOTAL"]}')
				carList = res.json()['resultData']['ALL']
				for carInfos in carList :
					if carInfos.get('hpselSta') == 'HA02' : 
						inData = {}
						# 현대캐피탈 상품 제외 (BJ07, BJ02) >> 링크 연결 불가
						# if carInfos.get('baeSta') != 'BJ02' or carInfos.get('baeSta') != 'BJ07' :
						if not (carInfos.get('baeSta') == 'BJ02' or carInfos.get('baeSta') == 'BJ07') :
							if carInfos.get('baeSta') == 'BJ03' : 
								brand = 'acar'
							elif carInfos.get('baeSta') == 'BJ12' :
								brand = 'rcar'
							inData['brand'] = brand
							inData['prod_id'] = carInfos.get('productId')
							inData['bm_name'] = carInfos.get('bmName')
							inData['boi_name'] = carInfos.get('boiName')
							inData['grade_name'] = carInfos.get('gradeName')
							inData['car_photo'] = carInfos.get('carPhoto1')
							# 연료
							inData['fuel'] = carInfos.get('fuel')
							# 사고유무
							inData['aci_gbn'] = carInfos.get('aciGbn')
							# 주행거리
							inData['car_navi'] = carInfos.get('carNavi')
							# 판매가
							inData['amt_sel'] = int(carInfos.get('amtSel')) - int(carInfos.get('amtSelDc'))
							# 년식
							inData['regi_date'] = carInfos.get('regiDate')[:-3].replace('-', '년 ') + '월'
							matching_car_list.append(inData)
	return matching_car_list

# 뉴스 상세 (신규)
def new_news_detail(request) : 
	news_code = request.GET.get('news_code')
	keyword = request.GET.get('keyword')
	news = TblTotalCarNewsList.objects.values().filter(news_code=news_code)
	news_no = news[0]['news_no']
	matching_car_list = TblNewsCarModelMap.objects.values().filter(news_no=news_no).exclude(boname='GT')
	
	bonames = []
	for matching_car in matching_car_list : 
		print(matching_car.get('boname'))
		bonames.append(matching_car.get('boname'))

	print(f'bonames >> {bonames}')
	car_infos = boname_to_car_infos(bonames)

	context = {}
	context['today_date'] = datetime.today().strftime('%Y-%m-%d')
	context['news'] = news[0]
	context['keyword'] = keyword
	context['page_group'] = 'news-detail-p'
	context['news_no'] = news_no
	context['matching_bo_names'] = bonames
	context['matching_car_infos'] = car_infos
	context['matching_car_count'] = len(car_infos)

	infos = {}
	infos['referer'] = request.headers.get('referer')
	infos['page_name'] = '/new_news_detail'
	infos['user_ip'] = get_ip(request)
	connect_log_insert(infos)

	if len(car_infos) > 0 :
		print(f'car list len = {len(car_infos)}')
		print(f'boname list = {bonames}')
		print(f'news no = {news_no}')

	return render(request, 'website/new_news_detail.html', context)

# 뉴스 트렌드
def news_trend(request) : 
	news_keyword_list = TblNewsAllKeywordList.objects.all()
	context = {}
	context['today_date'] = datetime.today().strftime('%Y-%m-%d')
	context['page_group'] = 'news-trend-p'

	return render(request, 'website/news_trend.html', context)

# 로그인
def login(request) :
	context = {}
	context['page_group'] = 'login-p'
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
# 로그아웃
def logout(request) : 
	if request.session.get('user') : 
		del request.session['user']

	return redirect('/')
# 회원가입
def join(request) : 
	context = {}
	context['page_group'] = 'join-p'
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
			context['memb_id'] = memb_id
			context['memb_name'] = memb_name
			context['gender'] = gender
			return render(request, 'website/join.html', context)
		elif TblMemberList.objects.filter(memb_id = memb_id).exists() == True : 
			context['error'] = '* 이미 존재하는 아이디입니다.'
			context['memb_name'] = memb_name
			context['gender'] = gender
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


# Ajax
# 뉴스 목록 가져오기 ajax
def news_list_data(request) :
	news_list = TblTotalCarNewsList.objects.all()
	today_date = datetime.today().strftime('%Y-%m-%d')
	if request.method == 'GET' :
		idx = int(request.GET.get('list_idx'))
		list_type = request.GET.get('list_type')
		start_idx = int(request.GET.get('start_idx'))
		load_length = int(request.GET.get('load_length'))
		search_keyword = request.GET.get('search_keyword')
		category_num = 1
	
		news = ''
		today_uploads = {}
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
			elif idx == 8 :
				category_num = 900
			elif idx == 9 :
				category_num = 1000
			elif idx == 10 :
				category_num = 1200
			news = news_list.filter(media_code=category_num).order_by('-write_date')

			today_uploads['auto_h'] = len(news_list.filter(add_date__contains = today_date).filter(media_code = 100))
			today_uploads['daily_car'] = len(news_list.filter(add_date__contains = today_date).filter(media_code = 200))
			today_uploads['autoview'] = len(news_list.filter(add_date__contains = today_date).filter(media_code = 300))
			today_uploads['it_chosun'] = len(news_list.filter(add_date__contains = today_date).filter(media_code = 400))
			today_uploads['auto_morning'] = len(news_list.filter(add_date__contains = today_date).filter(media_code = 500))
			today_uploads['auto_diary'] = len(news_list.filter(add_date__contains = today_date).filter(media_code = 600))
			today_uploads['carguy'] = len(news_list.filter(add_date__contains = today_date).filter(media_code = 700))
			today_uploads['the_drive'] = len(news_list.filter(add_date__contains = today_date).filter(media_code = 800))
			today_uploads['motorgraph'] = len(news_list.filter(add_date__contains = today_date).filter(media_code = 900))
			today_uploads['toprider'] = len(news_list.filter(add_date__contains = today_date).filter(media_code = 1000))
			today_uploads['global_motors'] = len(news_list.filter(add_date__contains = today_date).filter(media_code = 1200))
		elif list_type == 'category' :
			if idx == 0 :
				category_num = 7
			elif idx == 1 : 
				category_num = 1
			elif idx == 2 :
				category_num = 3
			elif idx == 3 :
				category_num = 5
			news = news_list.filter(news_category=category_num).order_by('-write_date')

			today_uploads['industry'] = len(news_list.filter(add_date__contains = today_date).filter(news_category = 7))
			today_uploads['used'] = len(news_list.filter(add_date__contains = today_date).filter(news_category = 1))
			today_uploads['new'] = len(news_list.filter(add_date__contains = today_date).filter(news_category = 3))
			today_uploads['review'] = len(news_list.filter(add_date__contains = today_date).filter(news_category = 5))
		elif list_type == 'all' : 
			# 검색
			news = news_list.filter( Q(news_content__icontains=search_keyword) | Q(news_title__icontains=search_keyword) ).order_by('-write_date')
			# LOG DB INSERT
			infos = {}
			if len(news) > 0 :
				infos['search_result_count'] = len(news)
			else : 
				infos['search_result_count'] = 0
			infos['searcher_ip'] = get_ip(request)
			infos['search_keyword'] = search_keyword
			search_log_insert(infos)

		set_news = serializers.serialize('json', news[start_idx:start_idx+load_length])
		return JsonResponse({'news': set_news, 'total_length': len(news), 'today_news': today_uploads}, status=200)

# 뉴스 클릭 수 ajax
def view_count(request) : 
	if request.method == 'GET' : 
		now_count = int(request.GET.get('now_count'))
		news_code = request.GET.get('news_code')
		after_count = now_count + 1
		try : 
			dbconn = mysql.connector.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'))
			cursor = dbconn.cursor()
			cursor.execute(f"""
				UPDATE 
					TBL_TOTAL_CAR_NEWS_LIST 
				SET 
					VIEW_COUNT = "{after_count}"
				WHERE 
					NEWS_CODE = "{news_code}"
			""")
		except Exception as e :
			print(f'****** + error! >> {e} >> 오류!')
		else : 
			dbconn.commit()
			dbconn.close()
			print(f'[{news_code} 조회수 증가] {now_count} >> {after_count} >> commit 완료')

		return HttpResponse(after_count, content_type="text/json-comment-filtered")


def car_review_list(request) : 
	infos = {}
	infos['referer'] = request.headers.get('referer')
	infos['page_name'] = '/car_review_list'
	infos['user_ip'] = get_ip(request)
	connect_log_insert(infos)
	context = {}
	context['page_group'] = 'car-review-list'
	
	return render(request, 'website/car_review_list.html', context)

def car_review_detail(request) : 
	infos = {}
	infos['referer'] = request.headers.get('referer')
	infos['page_name'] = '/car_review_detail'
	infos['user_ip'] = get_ip(request)
	connect_log_insert(infos)

	if request.method == 'GET' :
		bono = int(request.GET.get('bono'))
		news_keyword_list = TblNewsAllKeywordList.objects.all()

		print('bono', bono)

		context = {}
		context['page_group'] = 'car-comments-detail'
	
	return render(request, 'website/car_review_detail.html', context)

def car_review_list_data(request) : 
	comment_list = TblYoutubeCarCommentList.objects.all()
	car_info_list = TblCarInfos.objects.all()

	if request.method == 'GET' :
		start_idx = int(request.GET.get('start_idx'))
		load_length = int(request.GET.get('load_length'))
		bono = int(request.GET.get('bono'))

		car_info_group = {}
		car_infos = car_info_list.filter(bono = bono)
		for car_info in car_infos :
			info_no = car_info.info_no
			car_info_group['bmname'] = car_info.bmname
			car_info_group['boiname'] = car_info.boiname
			car_info_group['boname'] = car_info.boname
			car_info_group['car_img_url'] = car_info.car_img_url
			car_info_group['car_price'] = car_info.car_price
			car_info_group['fuel_efficiency'] = car_info.fuel_efficiency
			car_info_group['car_cc'] = car_info.car_cc
		
		comments = comment_list.filter(info_no = info_no).order_by('-comment_content_length')
		video_ids = comment_list.filter(info_no = info_no).values('comment_video_id').distinct()
		video_id_list = []
		for video_id in video_ids :
			video_id_list.append(video_id.get('comment_video_id'))


		# for comment in comments :
		# 	print(comment.boname)
				


		set_comments = serializers.serialize('json', comments[start_idx:start_idx + load_length])
		return JsonResponse({
			'comment_list': set_comments, 
			'total_length': len(comments), 
			'video_ids': video_id_list,
			# 'car_list': car_info_list,
			'car_infos': car_info_group
		}, status=200)


def sortNewsList(obj):
	return obj['view_count']

def bobaenews(request) :
	context = {}
	context['recommends'] = GetBobaeDream.recommend()[0].get('bobaedream_recoomend')
	view_count_list = GetBobaeDream.viewCount()[0].get('bobaedream_view_count')
	view_count_list.sort(key=sortNewsList, reverse=True)
	context['view_count'] = view_count_list
	context['today_year'] = today_year
	context['today_month'] = today_month
	# print(context['recommends'])
	# print(context['view_count'])
	# print(GetBobaeDream.viewCount()[0].get('bobaedream_view_count'))

	return render(request, 'website/bobaenews.html', context)

