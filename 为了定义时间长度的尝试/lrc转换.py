import os,shutil,requests,time
from subprocess import call,PIPE
from mutagen.mp3 import MP3





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
	for text in data[0:10]:
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



def lrc_get(path,name):
	with open(name,encoding='utf-8')as f:
		datalist=[i.strip() for i in f if i.strip()!='']	
	for root,dirs,file in os.walk(path):
		soundlist=[os.path.join(root,i) for i in file]
	numlist=[MP3(i).info.length for i in soundlist]
	i,l=0.00,[]
	for num in numlist:
		minute,sec=divmod(i,60)
		minute,sec =str(round(minute)).zfill(2),format(round(sec,2), '.2f')
		sec=[i[0].zfill(2)+'.'+i[-1].zfill(2) for i in (sec.split('.'),)][0]
		now=minute,sec
		l.append('[{}] '.format(':'.join(now)))
		i+=num	
	lastlist=[l[i]+datalist[i] for i in range(0,len(l))]
	return '\n'.join(lastlist)



path='music'
name='1.txt'
#get_mp3(path,name)
#path=os.path.join(path,name)
print(lrc_get(path,name))

'''
first_path='music'
path=[i[0].replace('.\\','') for i in os.walk('.') if i[0] !='.' and i[0].replace('.\\','').find('\\')<0]
names=[(i.split('.')[0],os.path.join(path[0],i)) for i in [i[-1] for i in os.walk(path[0])][0]]
names.sort()
for num,name in names[0:1]:
	print('正在进行:',num)
	#get_mp3(os.path.join(path[0],num),name)
	print('开始合并')
	splice(path[0],os.path.join(path[0],first_path),num)
'''
