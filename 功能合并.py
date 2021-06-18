import os,shutil,requests,time
from subprocess import call,PIPE

def request(web,data):
	while True:
		try:
			return requests.get(web,params=data).content
		except BaseException as e:
			print(e)
			time.sleep(0.5)



def get_mp3(path,name):
	with open(name,encoding='utf-8')as f:
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
		data = request(web,data)
		if not os.path.exists(path):
			os.mkdir(path)
		name=path+'/'+str(i)+'.mp3'
		with open(name,'wb')as f:
			f.write(data)
		i+=1



def splice():
	for root,dirs,file in os.walk('.'):
		if root =='.\\music':
			root=root.replace('.\\','')+'/'
			soundlist=[root+i for i in file]

	tempfile='new.mp3'
	cmd_part_1='D:\\ffmpeg-3.4.1\\ffmpeg '
	cmd_part_2=''
	for sound in soundlist:
		cmd_part_2+='-i {} '.format(sound)
	cmd_part_3='-filter_complex "[0:0] [1:0] concat=n={}:v=0:a=1 [a]" -map [a] {} '
	cmd_part_3 =cmd_part_3.format(str(len(soundlist)),tempfile)
	cmd=cmd_part_1+cmd_part_2+cmd_part_3
	with open('info.txt','w')as f:
		call(cmd,shell=True ,stdout=PIPE,stderr=f)



path='music'
name='1.txt'
get_mp3(path,name)
splice()


