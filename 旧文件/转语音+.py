import requests
import os

path='music'
with open('1.txt',encoding='utf-8')as f:
	data=[i.strip() for i in f if i.strip()!='']
print('len(data):',len(data))
i=1
for text in data:
	print('len(text):',len(text))
	data={
		'lan':'zh',
		'spd':'7',
		'source':'web',
		'text':text
	}
	web='https://fanyi.baidu.com/gettts'
	data = requests.get(web,params=data).content
	if not os.path.exists(path):
		os.mkdir(path)
	name=path+'/'+str(i)+'.mp3'
	with open(name,'wb')as f:
		f.write(data)
	i+=1

