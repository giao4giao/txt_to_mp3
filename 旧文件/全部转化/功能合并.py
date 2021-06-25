import os,shutil,requests,time
from subprocess import call,PIPE
#print(os.getcwd())

ffmpeg_path='D:\\ffmpeg-3.4.1'
ffmpeg_path=''
#ffmpeg_path=os.getcwd()

def request(web,data):
	while True:
		try:
			return requests.get(web,params=data).content
		except BaseException as e:
			print(e)
			time.sleep(0.5)



def get_mp3(path,_name):
	with open(_name,encoding='utf-8')as f:
		data=[i.strip() for i in f if i.strip()!='']
	print('len(data):',len(data))
	i=1
	for text in data:
		print('len(text):',len(text),'num:',i)
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
		name=os.path.join(path,str(i)+'.mp3')
		with open(name,'wb')as f:
			f.write(data)
		i+=1



def splice(path,name,num):
	global ffmpeg_path
	for root,dirs,file in os.walk(path):
		# print(root)
		if root.find(str(num))>0:
			soundlist=[os.path.join(root,i) for i in file]
	if not os.path.exists(name):
		os.mkdir(name)
	tempfile=os.path.join(name,str(num)+'.mp3')
	cmd_part_1=os.path.join(ffmpeg_path,'ffmpeg ')
	cmd_part_2=''
	
	with open(soundlist[0],'rb')as f:
		a=f.read()
	with open(soundlist[1],'rb')as f:
		b=f.read()
	with open('new.mp3','wb')as f:
		f.write(a+b)
	
	
	'''
	for sound in soundlist:
		cmd_part_2+='-i {} '.format(sound)
	cmd_part_3='-filter_complex "[0:0] [1:0] concat=n={}:v=0:a=1 [a]" -map [a] {} '
	cmd_part_3 =cmd_part_3.format(str(len(soundlist)),tempfile)
	cmd=cmd_part_1+cmd_part_2+cmd_part_3
	with open('info.txt','w')as f:
		#call(cmd,shell=True ,stdout=PIPE,stderr=f)
		call(cmd)
	#shutil.rmtree(os.path.join(path,num))
'''


# path='music'
# name='1.txt'
# get_mp3(path,name)
# splice()

first_path='music'
path=[i[0].replace('.\\','') for i in os.walk('.') if i[0] !='.' and i[0].replace('.\\','').find('\\')<0]
names=[(i.split('.')[0],os.path.join(path[0],i)) for i in [i[-1] for i in os.walk(path[0])][0]]
names.sort()
for num,name in names[0:1]:
	print('正在进行:',num)
	#get_mp3(os.path.join(path[0],num),name)
	print('开始合并')
	splice(path[0],os.path.join(path[0],first_path),num)

