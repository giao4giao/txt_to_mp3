import os, shutil, requests, time, threading
from queue import Queue
from mutagen.mp3 import MP3
from prettytable import PrettyTable


def run_forever(func):
	def wrapper(obj):
		while obj.event:
			func(obj)

	return wrapper


class QiubaiSpider:
	def __init__(self, list, count=(1, 1)):
		self.event = True
		self.url = 'https://fanyi.baidu.com/gettts'
		self.path = os.path.splitext(list)[0]
		with open(list, encoding='utf-8')as f:
			deal = f.read().replace('一秒记住♂小?说☆网 ，更新快，，免费读！', '').replace('免费小说，无弹窗小说网，txt下载，请记住蚂蚁阅读网www.mayitxt.com',
																		 '')
		with open(list, 'w', encoding='utf8')as f:
			f.write(deal)
		with open(list, encoding='utf-8')as f:
			self.li_list = [i.strip() for i in f if i.strip() != '']
		self.all_num = len(self.li_list)
		self.now_num = 0
		self.count, self.now_time = count, 1
		# url 队列
		self.url_queue = Queue()
		# 响应队列
		self.page_queue = Queue()

	def add_url_to_queue(self):
		# 把URL添加url队列
		num = 0
		for text in self.li_list:
			num += 1
			dic = {
				'lan': 'zh',
				'spd': '7',
				'source': 'web',
				'text': text}
			self.url_queue.put((num, dic))

	@run_forever
	def add_page_to_queue(self):
		# 发送请求获取数据
		try:
			dic_all = self.url_queue.get()
			number, dic = dic_all
			response = requests.get(self.url, dic, timeout=3)
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
			if now > 0:
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
			num, data = data_all
			if not os.path.exists(self.path):
				os.mkdir(self.path)
			number = str(num).zfill(len(list(str(self.all_num))))
			_name = os.path.join(self.path, str(number) + '.mp3')
			with open(_name, 'wb')as f:
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
			print(self.now_num, self.all_num)
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


def get_lrc(path, name):
	with open(name, encoding='utf-8')as f:
		datalist = [i.strip() for i in f if i.strip() != '']
	for root, dirs, file in os.walk(path):
		soundlist = [os.path.join(root, i) for i in file if os.path.splitext(i)[1] == '.mp3']
	soundlist.sort()
	numlist = [MP3(i).info.length for i in soundlist]
	i, l = 0.00, []
	for num in numlist:
		# print(i)
		minute, sec = divmod(i, 60)
		minute, sec = str(round(minute)).zfill(2), format(round(sec, 2), '.2f')
		sec = [i[0].zfill(2) + '.' + i[-1].zfill(2) for i in (sec.split('.'),)][0]
		now = minute, sec
		l.append('[{}]'.format(':'.join(now)))
		i += num
	lastlist = [l[i] + datalist[i] for i in range(0, len(datalist))]
	return '\n'.join(lastlist)


def splice(path, name, num):
	if not os.path.exists(name):
		os.mkdir(name)
	lrcfile = os.path.join(name, str(num) + '.lrc')
	textfile = name.replace(os.path.basename(name), '') + str(num) + '.txt'
	data = get_lrc(os.path.splitext(textfile)[0], textfile)
	with open(lrcfile, 'w', encoding='utf-8')as f:
		f.write(data)
	#	'''
	for root, dirs, file in os.walk(path):
		# print(root)
		if root.find(str(num)) > 0:
			soundlist = [os.path.join(root, i) for i in file]
	tempfile = os.path.join(name, str(num) + '.mp3')
	data = None
	soundlist.sort()
	# print(soundlist)
	for sound in soundlist:
		with open(sound, 'rb')as f:
			if not data:
				data = f.read()
			else:
				data = data + f.read()
	with open(tempfile, 'wb')as f:
		f.write(data)
	time.sleep(.5)
	shutil.rmtree(os.path.join(path, num))


#	'''

def onput(num):
	while True:
		try:
			put = int(input('请输入编号:'))
			if num >= put > 0:
				break
			elif put <= 0:
				print('输入大于0的数')
			else:
				print('输入最大值为%s' % str(num))

		except ValueError:
			print('请输入数字，请重新输入')
	return put


def get_name(n=1):
	max = os.path.abspath(os.getcwd()).split(str(os.path.sep))
	if 'storage' in max and 'emulated' in max and '0' in max:
		print('检测到最大递归等级{}'.format(str(len(max) - 4)))
	else:
		print('检测到最大递归等级{}'.format(str(len(max) - 1)))
	_path = os.getcwd()
	print('递归等级:{}'.format(str(n)))
	for i in range(n):
		_path = os.path.abspath(os.path.join(_path, ".."))
	paths = []
	for root, dirs, files in os.walk(_path):
		for dir in dirs:
			if dir == '小说下载':
				paths.append(os.path.join(root, '小说下载'))
	names, dic = [], {}
	for pa in paths:
		for root, dirs, files in os.walk(pa):
			for dir in dirs:
				path_ = os.path.join(root, dir)
				dic[dir] = path_
				names = names + [dir, ]
			break
	if names == []:
		return
	#	names=list(set(names))
	x = PrettyTable(['编号', '名字'])
	n = 1
	for i in names:
		x.add_row([str(n), i])
		n += 1
	print(x)
	if len(names) == 1:
		return list(dic.items())[0]
	cname = names[onput(len(names)) - 1]
	return (cname, dic.get(cname))


def main(path='.'):
	count = 20
	first_path = 'music'

	# 删除一些可能引发问题的内容
	del_paths = [i for i in [os.path.join(path[0],i) for i in os.listdir(path[0])] if os.path.isdir(i) and os.path.split(i)[-1] not in (first_path,)]
	del_paths+=('book','cover.jpg')
	for i in del_paths:
		if os.path.exists(os.path.join(path[0], i)):
			if os.path.isfile(i):
				os.remove(os.path.join(path[0], i))
			else:
				shutil.rmtree(i)

	# '''
	# names = [(i.split('.')[0], os.path.join(path[0], i)) for i in [i[-1] for i in os.walk(path[0])][0]]
	# names.sort()
	# print(names)

	# 取出对应文件夹的文件列表
	paths = [i for i in [os.path.join(path[0],i) for i in os.listdir(path[0])] if not os.path.isdir(i)]
	# print(paths)
	# 数据进行格式化
	datas = [(os.path.splitext(os.path.split(i)[-1])[0],i) for i in paths]

	#建立了筛选的列表
	filter_datas = os.listdir(os.path.join(path[0],first_path))
	dic ={i[0]:0 for i in datas}
	for i in filter_datas:
		if os.path.splitext(i)[-1] in ('.lrc','.mp3'):
			dic[os.path.splitext(i)[0]]+=1
	last_names,filter_names=[],[]
	for k,v in dic.items():
		if v != 2:
			last_names+=[k,]
		else:
			filter_names+=[k,]
	if filter_names!=[]:
		print('检测到：',filter_names,'已经存在，已经自动去除')
	names = [(k,v) for k,v in datas if k in last_names]

	for num, name in names[:]:
		print('正在进行:', num)
		QiubaiSpider(name, (count, count)).run()
		print('开始合并')
		splice(path[0], os.path.join(path[0], first_path), num)


# '''


if __name__ == '__main__':
	data = get_name(2)
	if data:
		a, b = data
		path = b, a
		main(path)
	else:
		print('未检测到文件')

