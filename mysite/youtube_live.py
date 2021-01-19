from pytchat import LiveChat
import pafy
import pandas as pd


if __name__ == '__main__' : 
	pafy.set_api_key('AIzaSyA2AZ0G5sRKq3uDTa_KzDT2X0oJ9rdcZWk')
	video_id = 'gHg5OMZR9EI'
	file_name = '20210119_reborn_show_chat'

	v = pafy.new(video_id)
	title = v.title
	author = v.author
	published = v.published

	empty_frame = pd.DataFrame(columns=['작성자', '채팅 내용', '작성시간'])
	empty_frame.to_csv(f'C:/Users/PC/Desktop/{file_name}.csv', encoding='utf-8-sig')

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
				result.to_csv(f'C:/Users/PC/Desktop/{file_name}.csv', mode='a', header=False)
		except KeyboardInterrupt : 
			chat.terminate()
			break
		

