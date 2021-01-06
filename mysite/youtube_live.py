from pytchat import LiveChat
import pafy
import pandas as pd



if __name__ == '__main__' : 
	pafy.set_api_key('AIzaSyA2AZ0G5sRKq3uDTa_KzDT2X0oJ9rdcZWk')
	video_id = '63rkn0GB2nI'

	v = pafy.new(video_id)
	title = v.title
	author = v.author
	published = v.published

	empty_frame = pd.DataFrame(columns=['작성자', '채팅 내용', '작성시간'])
	empty_frame.to_csv('./youtube.csv', encoding='utf-8-sig')

	chat = LiveChat(video_id = video_id, topchat_only = 'FALSE')
	while chat.is_alive() : 
		try : 
			data = chat.get()
			items = data.items
			for c in items :
				print(f'{c.datetime} [{c.author.name}] - {c.message}')
				data.tick()
				data2 = {'작성자' : [c.author.name], '채팅 내용': [c.message], '작성시간': [c.datetime]}
				result = pd.DataFrame(data2)
				result.to_csv('youtube.csv', mode='a', header=False)
		except KeyboardInterrupt : 
			chat.terminate()
			break
		
	# kkma = Kkma()
	# name_list = [1,2,3,5,5,5,5,4,42,2,2,1,1,2]
	# count = Counter(name_list)
	# count_list = count.most_common(50)
	# for name in count_list :
	# 	print(name)

	# pass

