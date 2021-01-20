from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.db.models import Q
from .models import TblTotalCarNewsList, TblMemberList, TblNewsKeywordList, TblNewsKeywordMap
from datetime import datetime
from django.http import HttpResponse
from django.core import serializers

import pandas as pd
import time
import mysql.connector

dbconn = mysql.connector.connect(host='118.27.37.85', user='car_news_zip', password='dbsgPwls!2', database='CAR_NEWS_ZIP', port='3366')
def execute(query, bufferd=True) :
	global dbconn
	try :
		cursor = dbconn.cursor(buffered=bufferd)
		cursor.execute(query)
	except Exception as e :
		dbconn.rollback()
		raise e
	finally : 
		dbconn.commit()
		cursor.close()
		# dbconn.close()

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

# 뉴스 분석
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

# 로그인
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
		elif idx == 8 :
			category_num = 900
		news = news_list.filter(media_code=category_num).order_by('-write_date')
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
	elif list_type == 'all' : 
		news = news_list.filter(Q(news_content__icontains=search_keyword) | Q(news_title__icontains=search_keyword) ).order_by('-write_date')
	
	set_news = serializers.serialize('json', news[start_idx:start_idx+load_length])
	return JsonResponse({'news': set_news, 'total_length': len(news)}, status=200)

# 뉴스 클릭 수 ajax
def view_count(request) : 
	if request.method == 'GET' : 
		now_count = int(request.GET.get('now_count'))
		news_code = request.GET.get('news_code')
		after_count = now_count + 1
		try : 
			print(f'조회수 >> {now_count} >> {after_count}')
			execute(f"""
				UPDATE TBL_TOTAL_CAR_NEWS_LIST 
				SET VIEW_COUNT = "{after_count}"
				WHERE NEWS_CODE = "{news_code}"
			""")
		except Exception as e :
			print(f'****** + error! >> {e} >> 오류!')
			pass
		finally : 
			print(f'[{news_code} 조회수 증가] {now_count} >> {after_count}')

	return HttpResponse(after_count, content_type="text/json-comment-filtered")


def car_comments(request) : 
	context = {}
	user_id = request.session.get('user')
	if user_id :
		memb_name = TblMemberList.objects.filter(memb_id=user_id).values()[0].get('memb_name')
		context['user'] = memb_name
	else : 
		context['user'] = None
	default_path = '../../car_news_zip/data/youtube_comments/'

	if request.method == 'POST' : 
		excel_path = f'{default_path}{request.POST["car-model"]}_review_comments_youtube.xlsx'
		df = pd.read_excel(excel_path, usecols='B:E', engine='openpyxl')
		# 정렬 조건 (댓글 길이 기준 내림차순)
		df = df.sort_values(by=['length'], axis=0, ascending=False)
		comment_list = []
		
		for row in df.values :
			temp_dict = {}
			temp_dict['register'] = row[0]
			temp_dict['comment'] = row[1]
			temp_dict['registed_date'] = row[2]
			comment_list.append(temp_dict)

		context['data'] = comment_list
		context['car_model'] = request.POST["car-model"]
		
		return render(request, 'website/car_comments.html', context)
	else :
		
		return render(request, 'website/car_comments.html', context)