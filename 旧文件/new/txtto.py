import requests,random,os,datetime
from requests_toolbelt.multipart.encoder import MultipartEncoder
from time import sleep


web='192.168.0.102:8088'
web='192.168.0.103:8088'
web='192.168.43.50:8088'
web='172.16.14.6:8088'

def State(web='192.168.0.100:8088'):
	# print(web)
	try:
		r=requests.get(url='http://'+web+'/',timeout=3)
		if r.status_code==200:
			return 1
		return 0
	except requests.exceptions.RequestException :
		return 0


#获取随机字符串
def Random():
	small=[chr(i)for i in range(97,123)]
	big=[chr(i)for i in range(65,91)]
	num=[chr(i)for i in range(48,58)]
	listing=num+small+big
	string=''
	string=string.join(listing)
	data=''
	for i in range(0,16):
		data = data + string[random.randint(0,61)]
	return data


class judge():
	def __init__(self):
		self.l=[]
		if not os.path.exists('download.txt'):
			with open ('download.txt','w')as f:
				print('已经创建download文件')

	def run(self):
		self.l=[]
		path=os.getcwd()
		for root,dirs,files in os.walk(path):
			for file in files:
				name,extension=os.path.splitext(file)
				if extension in ('.mp3','.lrc'):
					self.l.append(file)

		with open ('download.txt','r',encoding='utf-8')as f:
			for data in f:
				date=data.split('\n')[0].split(',time==')[0]
				if date in self.l and len(data)>6:
					self.l.remove(date)
		if not self.l==[]:
			return self.l[0]


	def add(self):
		if not self.l==[]:
			with open ('download.txt','a',encoding='utf-8')as f:
				f.write(self.l[0]+',time=='+str(datetime.datetime.now())+'\r\n')
			return {'code':0,'name':self.l[0]}
		return None



def upload(name,path,web='192.168.0.100:8088'):
	url='http://'+web+'/upload'
	headers ={
		'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31',
		'Referer': 'http://'+web+'/',
	}
	_name,file_extension=os.path.splitext(name)
	file_extension=file_extension.replace('.','')
	if file_extension=='mp3' or file_extension=='lrc':
		Content_Type='application/octet-stream'
	name_=name.encode('utf-8')
	multipart_encoder =MultipartEncoder(
		fields ={
			'name':'file',
			'filename':name_,
			'moduleid':'5',
			'path':('/'+path).encode('utf-8'),
			'data':(name_,open(name,'rb'),Content_Type)},
		boundary = '----'+'WebKitFormBoundary'+Random())
	headers['Content-Type']=multipart_encoder.content_type
	#headers['Content-Type']='audio/mp3'
	print('开始上传-|%s|-|%s|'%(_name,file_extension))
	try:
		r=requests.post(url,data=multipart_encoder,headers=headers)
		print(r.json())
		if not r.json().get('code'):
			print('上传完成-|%s|-|%s|'%(_name,file_extension))
			# return r.json().get('data').get('requestid')
			return r.json()
		print('上传失败-|%s|-|%s|'%(_name,file_extension))
		return None
	except requests.exceptions.RequestException :
		print('上传失败-|%s|-|%s|'%(_name,file_extension))
		return None

time=0
func = judge()
if State(web=web):
	print('连接成功')
	while True:
		name=func.run()
		if name:
			path='九星之主'
			requestid=upload(name=name,path=path,web=web)
			if not requestid:
				print('已经重新开始上传')
				if time>1:
					print('重试重试过多')
					exit()
				time+=1
			else:
				time=0
				func.add()
				print('继续上传----')
			sleep(.5)
		else:
			print('全部完成')
			break

else:
	print('连接失败')