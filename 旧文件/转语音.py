import requests
text='一'*10
text='后'
print(len(text))
data={
	'lan':'zh',
	'spd':'3',
	'source':'web',
	'text':text
}
# web='https://fanyi.baidu.com/gettts?lan=zh&spd=3&source=web&text={}'
web='https://fanyi.baidu.com/gettts'
r = requests.get(web,params=data)
data=r.content

#print(data)
# print(r.text)
with open('b.mp3','wb')as f:
	f.write(data)
#with open('a.tts','wb')as f:
#	f.write(data)


'''
with open('c.wav','w')as f:
	f.write(str(data))
'''

