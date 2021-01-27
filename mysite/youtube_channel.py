# coding=<utf-8>
import os, json
import mysql.connector
import pymssql
import time
import re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

# https://developers.google.com/youtube/v3/docs
# BK
# DEVELOPER_KEY = 'AIzaSyA2AZ0G5sRKq3uDTa_KzDT2X0oJ9rdcZWk'
# AUTOPLUS
# DEVELOPER_KEY = 'AIzaSyCHnGrLBzQJk3IvA-lhVRgfia5QUAIPb9k'
# KING BK
# DEVELOPER_KEY = 'AIzaSyB08WDZOdnWGqfcDKl4FB30LIRJzQS7JCQ'
# 용과장님 리본
DEVELOPER_KEY = 'AIzaSyBdTgUi0BB1A6OYqQBP4jGrUfDkVTk00Dc'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath('./mysite'))
# SECURITY WARNING: keep the secret key used in production secret!
db_info_file = os.path.join(BASE_DIR, 'db_conn_ap_test.json')
# db_info_file = os.path.join(BASE_DIR, 'db_conn.json')
with open(db_info_file) as f :
	db_infos = json.loads(f.read())


# 영상검색으로 채널 아이디 구하기
def get_channel_id(keyword) :
	search_response = youtube.search().list(
		q = keyword,
		order = 'relevance',
		part = 'snippet',
		maxResults = 50
	).execute()
	channel_id = search_response['items'][0]['id']['channelId']

	return channel_id

# 채널 정보
def get_channel_info(channel_id) :
	channel_info = {}
	channel_infos = youtube.channels().list(
		id = channel_id,
		part = 'snippet',
	).execute()
	
	channel_info['channel_id'] = channel_id
	channel_info['channel_name'] = channel_infos['items'][0]['snippet']['title']
	channel_info['channel_desc'] = channel_infos['items'][0]['snippet']['description']
	channel_info['channel_thumbnail'] = channel_infos['items'][0]['snippet']['thumbnails']['medium']['url']

	return channel_infos['items'][0]['snippet']


# 재생 목록
def get_play_list(channel_id) : 
	playlist_group = youtube.playlists().list(
		channelId = channel_id,
		part = 'snippet',
		maxResults=20
	).execute()

	# 재생목록 아이디와 타이틀 모두 저장
	playlist = []
	# 재생목록 아이디만 저장
	play_id_list = []
	for group in playlist_group['items']:
		info = {}
		info['title'] = group['snippet']['title']
		info['list_id'] = group['id']
		playlist.append(info)
		play_id_list.append(group['id'])

	return play_id_list

# 채널 > 재생목록 ID > 영상 목록
def get_video_list(playlist_id, channel_no) :
	video_ids = []
	video_titles = []
	video_dates = []

	playlist_videos = youtube.playlistItems().list(
		playlistId = playlist_id,
		part = 'snippet',
		maxResults = 50,
	)

	playlist_in_videos = []

	while playlist_videos :
		playlistitems_list_response = playlist_videos.execute()
		for playlist_item in playlistitems_list_response['items'] :
			info = {}
			try :
				info['channel_no'] = channel_no
				info['video_id'] = playlist_item['snippet']['resourceId']['videoId']
				info['title'] = re.sub('[-=.#/?:$}\"\']', '', playlist_item['snippet']['title'])
				info['desc'] = re.sub('[-=.#/?:$}\"\']', '', playlist_item['snippet']['description'])
				info['thumbnail'] = playlist_item['snippet']['thumbnails']['medium']['url']
				info['pub_date'] = playlist_item['snippet']['publishedAt']
				info['view_count'] = get_video_info(playlist_item['snippet']['resourceId']['videoId'])[0]['view_count']
				info['like_count'] = get_video_info(playlist_item['snippet']['resourceId']['videoId'])[0]['like_count']
				info['dislike_count'] = get_video_info(playlist_item['snippet']['resourceId']['videoId'])[0]['dislike_count']
			except : 
				info['channel_no'] = channel_no
				info['video_id'] = playlist_item['snippet']['resourceId']['videoId']
				info['title'] = re.sub('[-=.#/?:$}\"\']', '', playlist_item['snippet']['title'])
				info['desc'] = re.sub('[-=.#/?:$}\"\']', '', playlist_item['snippet']['description'])
				info['thumbnail'] = 'None'
				info['pub_date'] = playlist_item['snippet']['publishedAt']
				info['view_count'] = get_video_info(playlist_item['snippet']['resourceId']['videoId'])[0]['view_count']
				info['like_count'] = get_video_info(playlist_item['snippet']['resourceId']['videoId'])[0]['like_count']
				info['dislike_count'] = get_video_info(playlist_item['snippet']['resourceId']['videoId'])[0]['dislike_count']
			
			playlist_in_videos.append(info)
			playlist_videos = youtube.playlistItems().list_next(playlist_videos, playlistitems_list_response)

	return playlist_in_videos

# 비디오 아이디(`s) > 비디오 정보 
def get_video_info(video_ids) :
	video_info_list = []

	video_infos = youtube.videos().list(
		id = video_ids,
		part = ['snippet','statistics'],
	)

	idx = 0
	while video_infos :
		video_infos_response = video_infos.execute()
		for video_item in video_infos_response['items'] :
			info = {}
			info['video_id'] = video_ids[idx]
			info['pub_date'] = video_item['snippet']['publishedAt']
			info['view_count'] = video_item['statistics']['viewCount']
			info['like_count'] = video_item['statistics']['likeCount']
			info['dislike_count'] = video_item['statistics']['dislikeCount']

			idx += 1
			video_info_list.append(info)
			video_infos = youtube.playlistItems().list_next(video_infos, video_infos_response)

	return video_info_list

# 데이터 조합
def get_result_data() : 
	video_list_group = []
	# 채널 아이디로 영상 목록 조회
	channel_infos = get_channel_ids()
	for channel_info in channel_infos :
		print('ㅡ'* 60)
		print(f'[{channel_info.get("no")}] {channel_info.get("id")}')
		print('ㅡ'* 60)
		play_list_group = get_play_list(channel_info.get('id'))
		for idx, play_list in enumerate(play_list_group) :
			video_list = get_video_list(play_list, channel_info.get('no'))
			print('ㅡ'* 30)
			print(f'[{idx+1}/{len(play_list_group)}] 번째 영상 그룹')
			print('ㅡ'* 30)
			for idx, video in enumerate(video_list) :
				print(f'ㅡㅡ[{idx+1}/{len(video_list)}] 영상 정보 수집 완료!')
				video_list_group.append(video)
		
	# print(len(video_list_group))
	return video_list_group


# DB > 채널 아이디 목록
def get_channel_ids() :
	dbconn = pymssql.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'), charset='utf8')
	cursor = dbconn.cursor()

	# 채널 아이디 get
	channel_info = []
	cursor.execute(f"""
		SELECT CHANNEL_NO, CHANNEL_ID 
		FROM TBL_CHANNEL_LIST
		WHERE STATUS = 1
	""")
	rows = cursor.fetchall()
	dbconn.close()

	for row in rows :
		info = {}
		info['no'] = row[0]
		info['id'] = row[1]
		channel_info.append(info)

	return channel_info
	

# DB 동영상 정보 입력
def insert_db_video_infos(video_infos) :

	dbconn = pymssql.connect(host=db_infos.get('host'), user=db_infos.get('user'), password=db_infos.get('password'), database=db_infos.get('database'), port=db_infos.get('port'), charset='utf8')
	cursor = dbconn.cursor()
	
	for idx, video_info in enumerate(video_infos) :
		try :
			print(f'ㅡㅡ[{idx}/{len(video_infos)}] DB INSERT >> {video_info.get("title")}')
			# print(f"{video_info.get('video_id')}, {video_info.get('title')}, '내용', {video_info.get('thumbnail')}, {video_info.get('pub_date')}, {video_info.get('view_count')}, {video_info.get('like_count')}, {video_info.get('dislike_count')}, {video_info.get('channel_no')}")
			# VIDEO_ID 중복 체크 후 Insert
			cursor.execute(f"""
				INSERT INTO TBL_VIDEO_LIST 
					(VIDEO_ID, VIDEO_TITLE, VIDEO_DESC, VIDEO_THUMBNAIL, VIDEO_DATE, YOUTUBE_VIEW, YOUTUBE_LIKE, YOUTUBE_UNLIKE, CHANNEL_NO)
				SELECT 
					'{video_info.get("video_id")}', '{video_info.get("title")}', '{video_info.get("desc")}', '{video_info.get("thumbnail")}', '{video_info.get("pub_date")}', 
					{video_info.get("view_count")}, {video_info.get("like_count")}, {video_info.get("dislike_count")}, {video_info.get("channel_no")}
				WHERE NOT EXISTS
					(SELECT '' FROM TBL_VIDEO_LIST K WHERE K.VIDEO_ID='{video_info.get("video_id")}')
				
			""")
			time.sleep(0.5)
			# 최신 값으로 업데이트
			cursor.execute(f"""
				UPDATE TBL_VIDEO_LIST SET
					VIDEO_TITLE='{video_info.get("title")}', 
					VIDEO_DESC='{video_info.get("desc")}', 
					VIDEO_THUMBNAIL='{video_info.get("thumbnail")}', 
					VIDEO_DATE='{video_info.get("pub_date")}', 
					YOUTUBE_VIEW={video_info.get("view_count")}, 
					YOUTUBE_LIKE={video_info.get("like_count")}, 
					YOUTUBE_UNLIKE={video_info.get("dislike_count")}, 
					CHANNEL_NO={video_info.get("channel_no")}
				WHERE 
					VIDEO_ID='{video_info.get("video_id")}'
			""")
			time.sleep(0.5)			
		except Exception as e :
			print(f'****** ERROR : {e} *******')
			continue
	
	dbconn.commit()
	dbconn.close()
	


	




if __name__ == '__main__' :
	# print(get_channel_id('youngin ing'))

	# 1. admin에서 등록한 채널 아이디 목록을 가져온다. (사용 중인 채널아이디만 (STATUS = 1))
	
	now = time.localtime()
	start_time = now

	insert_db_video_infos(get_result_data())
	# 채널 입력 > 재생목록 아이디
	# print(get_play_list('UC2DoArGfQAO8wkkr3E1BHnw'))

	# 재생목록 아이디 > 영상목록
	# print(get_video_list('PL--_EJcFjzor3VUCyPg3zhsDf3QCgPi2a', 2))

	now = time.localtime()
	end_time = now
	print('ㅡ'*50)
	print('유튜브 영상 정보 수집 및 DB Insert/Commit/Close 완료!')
	print('유튜브 영상 정보 수집 작업 시작 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (start_time.tm_year, start_time.tm_mon, start_time.tm_mday, start_time.tm_hour, start_time.tm_min, start_time.tm_sec))
	print('유튜브 영상 정보 수집 작업 종료 시간 > %04d/%02d/%02d %02d:%02d:%02d' % (end_time.tm_year, end_time.tm_mon, end_time.tm_mday, end_time.tm_hour, end_time.tm_min, end_time.tm_sec))
