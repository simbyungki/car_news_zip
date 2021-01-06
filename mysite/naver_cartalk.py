import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import csv
import time

# 그렌져 IG 테스트
# 2017 = 66917
# 2018 = 122017
# 2019 = 127461

# 네이버 자동차 토크 댓글 수집
def get_car_talk() :
	comment_data = [] 
	url = 'https://auto.naver.com/car/talk.nhn?yearsId=66917'
	model_id_list = [66917, 122017, 127461]
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
		'referer': url 
	}
	page_cnt = 1
	for model_id in model_id_list :
		while True :
			url = f'https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=auto1&templateId=&pool=cbox&_callback=jQuery17027007885873388005_1609724711797&lang=ko&country=&objectId={model_id}&categoryId=&pageSize=10&indexSize=10&groupId=&listType=OBJECT&pageType=default&page={page_cnt}&refresh=false&sort=NEW&_=1609725469399'
			r = requests.get(url, headers=headers)
			cont = BeautifulSoup(r.content, 'html.parser')
			total_comment = str(cont).split('comment":')[1].split(",")[0]

			# 댓글내용분리
			comment = re.findall('"contents":([^\*]*),"userIdNo"', str(cont))
			# 등록일시분리
			reg_date = re.findall('"regTime":([^\*]*),"regTimeGmt"', str(cont))
			
			for idx in range(len(comment)) :
				comment_data.append([comment[idx], reg_date[idx][:17]])

			if int(total_comment) <= ((page_cnt) * 10): 
				break 
			else :  
				page_cnt += 1

	def return_comment_list(comments): 
		flatList = [] 
		for elem in comments: 
			flatList.append(elem)
			# 댓글만 수집하는 경우
			# if type(elem) == list: 
			# 	for e in elem: 
			# 		flatList.append(e) 
			# else: 
			# 	flatList.append(elem) 
		
		# print(flatList)
		return flatList

	comment_list = return_comment_list(comment_data)
	# print(len(comment_list))

	df = pd.DataFrame(columns = ['No', 'Date', 'Content'])
	printProgressBar(0, len(comment_list), prefix = 'Progress:', suffix = 'Complete', length = 50)

	for idx, comment in enumerate(comment_list) :
		# print(comment[1] , comment[0])
		# time.sleep(0.1)
		printProgressBar(idx + 1, len(comment_list), prefix = 'Progress:', suffix = 'Complete', length = 50)
		df = df.append(pd.DataFrame([[idx, comment[1] , comment[0]]], columns=['No', 'Date', 'Content']), ignore_index=True)
	df.set_index('No', inplace=True)
	df.to_csv('C:/Users/PC/Documents/simbyungki/git/car_news_zip/mysite/comment_grandeur_ig.csv', encoding='utf-8-sig')
	

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

if __name__ == '__main__' : 
	get_car_talk()
	pass