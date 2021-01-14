from oauth2client.client import GoogleCredentials
from googleapiclient import discovery
from googleapiclient import errors

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = 'AIzaSyA2AZ0G5sRKq3uDTa_KzDT2X0oJ9rdcZWk'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# https://blog.naver.com/doublet7411/221514043955
# https://blog.naver.com/doublet7411/221514090972

def youtube_search(keywords) :
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    
    search_response = youtube.search().list(
        q = keywords,
        part = 'id, snippet',
        maxResults = 50
    ).execute()
    
    videos = []
    channels = []
    playlists = []
    
    for search_result in search_response.get('items', []) :
        if search_result['id']['kind'] == 'youtube#video' : 
            videos.append('%s (%s)' % (search_result['snippet']['title'], search_result['id']['videoId']))
        elif search_result['id']['kind'] == 'youtube#channel' :
            channels.append('%s (%s)' % (search_result['snippet']['title'], search_result['id']['channelId']))
        elif search_result['id']['kind'] == 'youtube#playlist' : 
            playlists.append('%s (%s)' % (search_result['snippet']['title'], search_result['id']['playlistId']))

            
    return videos

if __name__ == '__main__' : 
	print(youtube_search('gv80시승'))