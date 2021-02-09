from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.db.models import Q
from .models import TblTotalCarNewsList, TblMemberList, TblNewsKeywordList, TblNewsKeywordMap, TblYoutubeCarCommentList
from datetime import datetime
from django.http import HttpResponse
from django.core import serializers

import requests
import pandas as pd
import time
import mysql.connector
import os, json
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath('./mysite'))
# SECURITY WARNING: keep the secret key used in production secret!
db_info_file = os.path.join(BASE_DIR, 'db_conn.json')
with open(db_info_file) as f :
	db_infos = json.loads(f.read())

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
	context['page_group'] = 'news-list'
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

# 로그인
def login(request) :
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
# 로그아웃
def logout(request) : 
	if request.session.get('user') : 
		del request.session['user']

	return redirect('/')
# 회원가입
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


def car_comments(request) : 
	infos = {}
	infos['referer'] = request.headers.get('referer')
	infos['page_name'] = '/car_comments'
	infos['user_ip'] = get_ip(request)
	connect_log_insert(infos)
	context = {}
	context['page_group'] = 'car-comments-list'
	
	return render(request, 'website/car_comments.html', context)
	


def car_comment_list_data(request) : 
	comment_list = TblYoutubeCarCommentList.objects.all()

	if request.method == 'GET' :
		start_idx = int(request.GET.get('start_idx'))
		load_length = int(request.GET.get('load_length'))
		bono = int(request.GET.get('bono'))

		comments = comment_list.filter(bono = bono).order_by('-comment_content_length')
		video_ids = comment_list.filter(bono = bono).values('comment_video_id').distinct()
		video_id_list = []
		for video_id in video_ids :
			video_id_list.append(video_id.get('comment_video_id'))

		set_comments = serializers.serialize('json', comment_list[start_idx:start_idx+load_length])
		return JsonResponse({'comment_list': set_comments, 'total_length': len(comment_list), 'video_ids': video_id_list}, status=200)