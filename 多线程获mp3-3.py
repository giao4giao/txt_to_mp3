import os,shutil,requests,time,threading
from queue import Queue
from mutagen.mp3 import MP3

def run_forever(func):
	def wrapper(obj):
		while obj.event:
			func(obj)
	return wrapper


class QiubaiSpider:
	def __init__(self, list ,count=(1, 1)):
		self.event= True
		self.url='https://fanyi.baidu.com/gettts'
		self.path=os.path.splitext(list)[0]
		with open(list,encoding='utf-8')as f:
			self.li_list=[i.strip() for i in f if i.strip()!='']
		self.all_num=len(self.li_list)
		self.now_num = 0
		self.count,self.now_time= count, 1	
		# url 队列
		self.url_queue = Queue()
		# 响应队列
		self.page_queue = Queue()


	def add_url_to_queue(self):
		# 把URL添加url队列
		num=0
		for text in self.li_list:
			num+=1
			dic={
			'lan':'zh',
			'spd':'7',
			'source':'web',
			'text':text}
			self.url_queue.put((num,dic))

	@run_forever
	def add_page_to_queue(self):
		# 发送请求获取数据
		try:
			dic_all = self.url_queue.get()
			number,dic = dic_all
			response = requests.get(self.url,dic ,timeout=3)
			if response.status_code != 200:
				self.url_queue.put(dic_all)
			else:
				self.page_queue.put((number, response))
			time.sleep(1)
		# 完成当前URL任务

		except BaseException as e:
			# print(e)
			self.url_queue.put(dic_all)
			now = str(e).find('443')
			if now> 0:
				if self.now_time >= 5:
					print('网络连接超时')
					self.now_time = 1
				else:
					self.now_time += 1
			time.sleep(0.5)
		finally:
			self.url_queue.task_done()

	@run_forever
	def add_dz_to_queue(self):
		try:
			data_all = self.page_queue.get()
			num,data = data_all
			if not os.path.exists(self.path):
				os.mkdir(self.path)
			number=str(num).zfill(len(list(str(self.all_num))))
			_name=os.path.join(self.path,str(number)+'.mp3')
			with open(_name,'wb')as f:
				f.write(data.content)
			self.now_num += 1
			time.sleep(.5)	
		except BaseException as e:
			print(e)
			self.page_queue.put(data_all)
			time.sleep(0.5)
		finally:
			self.page_queue.task_done()



	def run_use_more_task(self, func, count=1):
		# 把func放到线程中执行,count:开启多少线程执行
		for i in range(0, count):
			t = threading.Thread(target=func)
			t.setDaemon(True)
			t.start()

	def verification_event(self):
		while True:
			print(self.now_num,self.all_num)
			if self.now_num == self.all_num:
				self.event = False
				break
			else:
				time.sleep(0.5)

	def run(self):
		# 开启线程执行上面的几个方法
		url_t = threading.Thread(target=self.add_url_to_queue)
		url_t.setDaemon(True)
		url_t.start()
		url_t.join()
		p = threading.Thread(target=self.verification_event)
		p.setDaemon(True)
		p.start()


		self.run_use_more_task(self.add_page_to_queue, self.count[0])
		self.run_use_more_task(self.add_dz_to_queue, self.count[1])


		self.url_queue.join()
		self.page_queue.join()



def get_lrc(path,name):
	with open(name,encoding='utf-8')as f:
		datalist=[i.strip() for i in f if i.strip()!='']
	for root,dirs,file in os.walk(path):
		soundlist=[os.path.join(root,i) for i in file if os.path.splitext(i)[1]=='.mp3']
	soundlist.sort()
	numlist=[MP3(i).info.length for i in soundlist]
	i,l=0.00,[]
	for num in numlist:
		#print(i)
		minute,sec=divmod(i,60)
		minute,sec =str(round(minute)).zfill(2),format(round(sec,2), '.2f')
		sec=[i[0].zfill(2)+'.'+i[-1].zfill(2) for i in (sec.split('.'),)][0]
		now=minute,sec
		l.append('[{}]'.format(':'.join(now)))
		i+=num
	lastlist=[l[i]+datalist[i] for i in range(0,len(datalist))]
	return '\n'.join(lastlist)


def splice(path,name,num):
	if not os.path.exists(name):
		os.mkdir(name)
	lrcfile=os.path.join(name,str(num)+'.lrc')
	textfile=name.replace(os.path.basename(name),'')+str(num)+'.txt'
	data=get_lrc(os.path.splitext(textfile)[0],textfile)
	with open(lrcfile,'w',encoding='utf-8')as f:
		f.write(data)
#	'''
	for root,dirs,file in os.walk(path):
		# print(root)
		if root.find(str(num))>0:
			soundlist=[os.path.join(root,i) for i in file]
	tempfile=os.path.join(name,str(num)+'.mp3')
	data=None
	soundlist.sort()
	#print(soundlist)
	for sound in soundlist:
		with open(sound,'rb')as f:
			if not data:
				data = f.read()
			else:
				data =data+f.read()
	with open(tempfile,'wb')as f:
		f.write(data)
	time.sleep(.5)
	shutil.rmtree(os.path.join(path,num))
#	'''





count=20
first_path='music'
path=[i[0].replace('.\\','') for i in os.walk('.') if i[0] !='.' and i[0].replace('.\\','').find('\\')<0]
print(path)
path=path[-1:]
print(path)
'''
names=[(i.split('.')[0],os.path.join(path[0],i)) for i in [i[-1] for i in os.walk(path[0])][0]]
names.sort()
for num,name in names:
	print('正在进行:',num)
	QiubaiSpider(name,(count,count)).run()
	print('开始合并')
	splice(path[0],os.path.join(path[0],first_path),num)
'''
