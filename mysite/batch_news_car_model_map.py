import requests
import time
import re
import regex
import os, json
import mysql.connector
import pymssql
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
## 장고 프로젝트를 사용할 수 있도록 환경을 구축
import django
django.setup()

from website.models import TblTotalCarNewsList, TblMemberList, TblNewsKeywordList, TblNewsKeywordMap, TblNewsCarModelMap
from datetime import datetime


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


# APDB에서 차량 모델 조회
def getCarModelList() :
	dbconn2 = pymssql.connect(host=db_infos2.get('host'), user=db_infos2.get('user'), password=db_infos2.get('password'), database=db_infos2.get('database'), port=db_infos2.get('port'), charset='EUC-KR')
	cursor2 = dbconn2.cursor()

	carModelList = []

	cursor2.execute(f"""
		SELECT
			DISTINCT BONO,
			BONAME
		FROM 
			ATB_NCAR_MODEL
	""")
	rows = cursor2.fetchall()
	
	for idx, row in enumerate(rows) :
		model = []
		model.append(row[0])
		model.append(row[1])
		carModelList.append(model)


	cursor2.close()
	dbconn2.close()

	print(len(carModelList))
	return carModelList
	

def getNewsMatchingList(carModelList) :
	# dbconn = pymssql.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'), charset='EUC-KR')
	# cursor = dbconn.cursor()

	carNewsList = TblTotalCarNewsList.objects.values().filter(car_model_bat_status=1)
	newsCarMap = TblNewsCarModelMap()

	print(f'**** 차량모델과 뉴스기사 매칭 및 DB저장 시작! [모델 : {len(carModelList)}건 // 뉴스 : {len(carNewsList)}건]')

	try :
		insert_map_list = []
		insert_update_news_list = []
		for idx, carNews in enumerate(carNewsList) :
			news_title = carNews.get('news_title')
			news_content = carNews.get('news_content')
			for carModel in carModelList : 
				if carModel[1] in news_title : 
					if carModel[1] in news_content : 
						## carModel[0] = BONO
						## carModel[1] = 모델명
						print(f'뉴스와 차량 매칭! >> [{carModel[0]}]{carModel[1]} ///// {carNews.get("news_title")}')
						insert_map_list.append(TblNewsCarModelMap(bono = carModel[0], boname = carModel[1], news_no = carNews.get('news_no'), map_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
				# 		insert_map_list.append(TblNewsCarModelMap(bono = carModel[0], boname = carModel[1], news_no = carNews.get('news_no')))
			thisNews = TblTotalCarNewsList.objects.get(news_no = carNews.get("news_no"))
			thisNews.car_model_bat_status = 3
			thisNews.save()

		TblNewsCarModelMap.objects.bulk_create(insert_map_list)
	except Exception as e :
		print(f'*+++++ + error! >> {e}')
		pass
	finally : 
		print('ㅡ'*50)
		print('**** 차량모델과 뉴스기사 매칭 및 DB저장 완료!')
		print('ㅡ'*50)


	# for idx, carNews in enumerate(carNewsList) :
	# 	news_title = carNews.get('news_title')
	# 	for carModel in carModelList : 
	# 		if carModel[1] in news_title : 
	#			if carModel[1] in news_content : 
					# ## carModel[0] = BONO
					# ## carModel[1] = 모델명
					# print(f'result = [{carModel[0]}]{carModel[1]} >> {carNews.get("news_no")}')
					# try :
					# 	cursor.execute(f"""
					# 		INSERT IGNORE INTO TBL_NEWS_CAR_MODEL_MAP 
					# 		(
					# 			BONO, NEWS_NO, MAP_DATE
					# 		) 
					# 		VALUES (
					# 			{carModel[0]}, {carNews.get("news_no")}, NOW()
					# 		) 
					# 	""")
					# except Exception as e :
					# 	print(f'*+++++ + error! >> {e}')
					# 	pass
					# finally : 
					# 	print('**** 차량모델과 뉴스기사 매칭 및 DB저장 완료!')
					# 	print('ㅡ'*50)
	# dbconn.commit()
	# cursor.close()
	# dbconn.close()


if __name__ == '__main__' : 
	now = time.localtime()
	start_time = now

	getNewsMatchingList(getCarModelList())

	now = time.localtime()
	end_time = now

	print('ㅡ'*50)
	print('차량모델과 뉴스기사 매칭 DB Commit/Close 완료!')
	print('차량모델과 뉴스기사 매칭 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('차량모델과 뉴스기사 매칭 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))