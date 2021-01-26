from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

# https://developers.google.com/youtube/v3/docs
# DEVELOPER_KEY = 'AIzaSyA2AZ0G5sRKq3uDTa_KzDT2X0oJ9rdcZWk'
DEVELOPER_KEY = 'AIzaSyCHnGrLBzQJk3IvA-lhVRgfia5QUAIPb9k'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)


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
	channel_ifno = {}
	channel_infos = youtube.channels().list(
		id = channel_id,
		part = 'snippet',
	).execute()

	channel_ifno['channel_name'] = channel_infos['items'][0]['snippet']['title']
	channel_ifno['channel_desc'] = channel_infos['items'][0]['snippet']['description']
	channel_ifno['channel_thumbnail'] = channel_infos['items'][0]['snippet']['thumbnails']['medium']['url']

	return channel_ifno

# 재생 목록
def get_play_list(channel_id) : 
	playlist_group = youtube.playlists().list(
		channelId = channel_id,
		part = 'snippet',
		maxResults=20
	).execute()

	playlist = []
	for group in playlist_group['items']:
		info = {}
		info['title'] = group['snippet']['title']
		info['list_id'] = group['id']
		playlist.append(info)
	
	return playlist

# 채널 > 재생목록 ID > 영상 목록
def get_video_list(playlist_id) :
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

		# print('ㅡ'* 100)
		# print(playlistitems_list_response)

		for playlist_item in playlistitems_list_response['items'] :
			info = {}
			try :
				info['video_id'] = playlist_item['snippet']['resourceId']['videoId']
				info['title'] = playlist_item['snippet']['title']
				info['desc'] = playlist_item['snippet']['description']
				info['thumbnail'] = playlist_item['snippet']['thumbnails']['standard']['url']
			except : 
				info['video_id'] = playlist_item['snippet']['resourceId']['videoId']
				info['title'] = playlist_item['snippet']['title']
				info['desc'] = playlist_item['snippet']['description']
				info['thumbnail'] = '없다'

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



if __name__ == '__main__' :
	# print(get_channel_info(get_channel_id('모트라인')))
	
	print(get_video_info(['MPPF80yLRsQ', 'bpY3_PjujD4']))

	# print(len(get_play_list(get_channel_id('모터그래프'))))
	# [
	# 	{'title': '리본쇼 차량 리스트', 'list_id': 'PLU7cN9HulzoY4mfdrhvR_Vl64-qAKCcwD'}, 
	# 	{'title': '�🎥어서와와,오토플러스는는처음이지지?', 'list_id': 'PLU7cN9HulzobO1YzDGD-91Px3Z8U7JIUf'}, 
	# 	{'title': 차원이이다른른실시간간라이브브쇼쇼!리본 나의의유일한한!럭키옥션⏰⏰', 'list_id': 'PLU7cN9HulzobJvv2hRQmFWba5LmMpv4pi'}, 
	# 	{'title': �🎬오.플.소차차량소소개개', 'list_id': 'PLU7cN9HulzoYLHGiJxfs3GTYOFftoQoH-'}, 
	# 	{'title' ��중고고차의 바른 기준,오토플플러스리리본쇼�🎊', 'list_id': 'PLU7cN9HulzoY5RAnLRxC-ci8XDrIFIRL_'}, 
	# 	{'title': 이벤트트추첨영상상', 'list_id': 'PLU7cN9HulzoYrBqu-ImZQCYjkR6bCurrr'}, 
	# 	{'title': ��오플플의달인인🥇🥇', 'list_id': 'PLU7cN9HulzoaB2dWEKiRL-s4qMi_RCnmF'}, {'titid': 'PLU7cN9Hulzob5HnVnWLBOsTEBNv3crlaZ'}, 
	# 	{'title': '자동차의 새로운기준, 리본카', 'list_id': 'PLU7cN9HulzobDpB6JHQ9sSYSiMAstzGvM'}, 
	# 	{'title': '행사영상', 'list_id': 'PLU7cN9HulzoZkcoMHCtbLS0aM4WlKruE0'}, 
	# 	{'title': '리본카 ��단단하나의의유일한한!럭키옥션⏰⏰', 'list_id': 'PLU7cN9HulzobJvv2hRQmFWba5LmMpv4pi'}, 
	# 	{'title': �🎬오.플.소차차량소소개개', 'list_id': 'PLU7cN9HulzoYLHGiJxfs3GTYOFftoQoH-'}, 
	# 	{'title' ��중고고차의 바른 기준,오토플플러스리리본본카카!',PS C:\Users\PC\Documents\simbyungki\git\car_news_zip\mysite> python youtube_channel.py_id': 'PLU7cN9Hulzob5HnVnWLBOsTEBNv3crlaZ'}, 
	# 	{'title': '자동차의 새로운기준, 리본카', 'list_id': 'PLU7cN9HulzobDpB6JHQ9sSYSiMAstzGvM'}, 
	# 	{'title': '행사영상', 'list_id': 'PLU7cN9HulzoZkcoMHCtbLS0aM4WlKruE0'}, 
	# 	{'title': '리본카 누리기', 'list_id': 'PLU7cN9HulzoYUOKQH_X0-ld9K-tCc0_S-'}, 
	# 	{'title': '자동차스트레스연구소', 'list_id': 'PLU7cN9Hulzoauc5grgcf4FaC7gxdFT8sY'}
	# ]

	# print(get_video_list('PLoykoHin5zIaCXtbB4kStCdjIYh-6Sezw'))
	# [
	# 	{'video_id': '68JnMB4PfVw', 'title': '쏘울 EV 5인승', 'desc': '중고차의 바른 기준 #오토플러스 #리본카\n\n쏘울 EV 5인승\n연식 : 2018년 01월\n주행거리 : 7,297km\n컬러 : 흰색투톤\n냄새케어 : 1등급\n사고유무 : 무사고 \n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/smartbuy/WUSB050001.rb?productId=C21010600037', 'thumbnail': 'https://i.ytimg.com/vi/68JnMB4PfVw/sddefault.jpg'}, 
	# 	{'video_id': 'f8vn_ONhmK0', 'title': 'GV80 3.0 디젤 AWD', 'desc': '중고차의 바른 기준 #오토플러스 #리본카\n\nGV80 3.0 디젤 AWD\n연식 : 2020년 01월\n주행거리 : 10,046km\n컬러 : 멜버른 그레이(무광)\n냄새케어 : 1등급\n사고유무 : 무사고 \n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/smartbuy/WUSB050001.rb?productId=C20122800029', 'thumbnail': 'https://i.ytimg.com/vi/f8vn_ONhmK0/sddefault.jpg'}, 
	# 	{'video_id': 'MbnH8-4d-DU', 'title': 'G80 3.3 GDi 력셔리', 'desc': '중고차의 바른 기준 #오토플러스 #리본카\n\nG80 3.3 GDi 력셔리\n연식 : 2019년 05월\n주행거리 : 26,980km\n컬러 : 검정\n냄새케어 : 1등급\n사고유무 : 무사고 \n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/smartbuy/WUSB050001.rb?productId=C20122100010', 'thumbnail': 'https://i.ytimg.com/vi/MbnH8-4d-DU/sddefault.jpg'}, 
	# 	{'video_id': 'kjFMYjHacN4', 'title': 'Deleted video', 'desc': 'This video is unavailable.', 'thumbnail': '없다'}, 
	# 	{'video_id': 'fPyJvMQkosg', 'title': '더 뉴K3 1.6 GDI 디럭스', 'desc': '중고차의 바른 기준 #오토플러스 #리본카\n\n더 뉴K3 1.6 GDI 디럭스\n연식 : 2016년 12월\n주행거리 : 61,662km\n컬러 : 흰색\n냄새케어 : 1등급\n사고유무 : 무사고 \n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/smartbuy/WUSB050001.rb?productId=C20121600033', 'thumbnail': 'https://i.ytimg.com/vi/fPyJvMQkosg/sddefault.jpg'}, 
	# 	{'video_id': 'JWD7p25-OQQ', 'title': '올 뉴아반떼 CN7 가솔린 1.6 인스퍼레이션', 'desc': '중고차의 바른 기준 #오토플러스 #리본카\n\n올 뉴아반떼 CN7 가솔린 1.6 인스퍼레이션\n연식 : 2020년 04월\n주행거리 : 3,437km\n컬러 : 사이버 그레이\n냄새케어 : 1등급\n사고유무 : 무사고 \n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/smartbuy/WUSB050001.rb?productId=C20121400006', 'thumbnail': 'https://i.ytimg.com/vi/JWD7p25-OQQ/sddefault.jpg'}, 
	# 	{'video_id': 'lXuWx-tYwuk', 'title': 'EQ900 리무진 5.0 GDi 프레스티지', 'desc': '중고차의 바른 기준 #오토플러스 #리본카\n\n\nEQ900 리무진 5.0 GDi 프레스티지\n연식 : 2016년 04월\n주행거리 :  25,248km\n컬러 : 검정\n냄새케어 : 3등급\n사고유무 : 무사고 \n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/smartbuy/WUSB050001.rb?productId=C20122800016', 'thumbnail': 'https://i.ytimg.com/vi/lXuWx-tYwuk/sddefault.jpg'}, 
	# 	{'video_id': 'mgi7OnSfNZ0', 'title': '모닝 어반 1.0 가솔린 시그니처 (허니비)', 'desc': '중고차의 바른 기준 #오토플러스 #리본카\n\n#모닝어반_특가 (특.별.혜.택)\n1. 오늘 상담 남기고\n올해 안에 계약금 넣으시고\n1월 10일까지 구매하시면 = 150만원 할인!!!!\n.\n2. 오늘 상담만 남기시고,\n1월 말까지 구매하시면 = 100만원 할인!!!!!!!\n.\n모닝 어반 1.0 가솔린 시그니처\n연식 : 2020년 05월\n주행거리 :  1,201km\n컬러 : 허니비\n냄새케어 : 1등급\n사고유무 : 무사고 \n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/smartbuy/WUSB050001.rb?productId=C20092300073', 'thumbnail': 'https://i.ytimg.com/vi/mgi7OnSfNZ0/sddefault.jpg'}, 
	# 	{'video_id': 'HrAykvskhdk', 'title': '모닝 어반 1.0 가솔린 시그니처 (샤이니 레드)', 'desc': '중고차의 바른 기준 #오토플러스 #리본카\n\n#모닝어반_특가 (특.별.혜.택)\n1. 오늘 상담 남기고\n올해 안에 계약금 넣으시고\n1월 10일까지 구매하시면 = 150만원 할인!!!!\n.\n2. 오늘 상담만 남기시고,\n1월 말까지 구매하시면 = 100만원 할인!!!!!!!\n.\n.\n모닝 어반 1.0 가솔린 시그니처\n연식 : 2020년 05월\n주행거리 :  531km\n컬러 : 샤이니레드\n냄새케어 : 1 등급\n사고유무 : 무사고 \n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/smartbuy/WUSB050001.rb?productId=C20092300109', 'thumbnail': 'https://i.ytimg.com/vi/HrAykvskhdk/sddefault.jpg'}, 
	# 	{'video_id': 'jKvZWkKTlVE', 'title': 'X3(3세대) 20d xDrive x라인', 'desc': '중고차의 바른 기준 #오토플러스 #리본카\n\nX3(3세대) 20d xDrive x라인\n연식 : 2020년 2월\n주행거리 : 19,097km\n컬러 : 은색\n냄새케어 : 1등급\n사고유무 : 무사고 \n\n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/smartbuy/WUSB050001.rb?productId=C20102700010', 'thumbnail': 'https://i.ytimg.com/vi/jKvZWkKTlVE/sddefault.jpg'}, 
	# 	{'video_id': 'UTGZX_TguIc', 'title': '더 뉴쏘렌토 디젤 R2.0 2WD 노블레스', 'desc': '중고차의 바른 기준 #오토플러스 #리본카\n\n#더_뉴쏘렌토 디젤 R2.0 2WD 노블레스\n연식 : 2018년 12월\n주행거리 : 33,765km\n컬러 : 흰색\n냄새케어 : 3등급\n사고유무 : 무사고 \n\n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/smartbuy/WUSB050001.rb?productId=C20102700004', 'thumbnail': 'https://i.ytimg.com/vi/UTGZX_TguIc/sddefault.jpg'}, 
	# 	{'video_id': 'm9YLxzSC-DA', 'title': '더 뉴카니발 9인승 디젤 프레스티지', 'desc': '중고차의 바른 기준 #오토플러스 \n\n더 뉴카니발 9인승 디젤 프레스티지\n연식 : 2018년 11월\n주행거리 :  28,035km\n컬러 : 검정\n사고유무 : 무사고 \n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/acar/ACVP020001?productId=C20092400033', 'thumbnail': 'https://i.ytimg.com/vi/m9YLxzSC-DA/sddefault.jpg'}, 
	# 	{'video_id': 'ApWWMAmDdac', 'title': 'GV80 3.5T 가솔린 AWD', 'desc': '중고차의 바른 기준 #오토플러스 #리본카\n\nGV80 3.5T 가솔린 AWD\n연식 : 2020년 05월\n주행거리 :  10km\n컬러 : 검정\n냄새케어 : 1등급\n사고유무 : 무사고 \n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/smartbuy/WUSB050001.rb?productId=C20111200020', 'thumbnail': 'https://i.ytimg.com/vi/ApWWMAmDdac/sddefault.jpg'}, 
	# 	{'video_id': 'G8Pkv-5cQAU', 'title': 'K7 프리미어 3.0 LPi 프레스티지', 'desc': '중고차의 바른 기준 #오토플러스 #리본카\n\nK7 프리미어 3.0 LPi 프레스티지\n연식 : 2020년 05월\n주행거리 :  39km\n컬러 : 쥐색\n냄새케어 : 1등급\n사고유무 : 무사고 \n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/smartbuy/WUSB050001.rb?productId=C20111200021', 'thumbnail': 'https://i.ytimg.com/vi/G8Pkv-5cQAU/sddefault.jpg'}, 	
	# 	{'video_id': 'VrLMeA9srHk', 'title': 'G90 3.8 AWD 럭셔리', 'desc': '중고차의 바른 기준 #오토플러스 #리본카\n\n연식 : 2019년 03월\n주행거리 :  39,088km\n컬러 : 검정색\n냄새케어 : 1등급\n사고유무 : 무사고 \n.\n.\n.\n[ 차량 바로보기 ]\nhttps://www.autoplus.co.kr/smartbuy/WUSB050001.rb?productId=C20120200014', 'thumbnail': 'https://i.ytimg.com/vi/VrLMeA9srHk/sddefault.jpg'}
	# ]

