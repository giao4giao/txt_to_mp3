import os
os.environ['path']=os.environ.get('path')+';D:\\ffmpeg-3.4.1'
from pydub import AudioSegment


'''
#加载要合并的音频数据
inMP3_1=AudioSegment.from_mp3("a.mp3")
print(inMP3_1)
inMP3_2=AudioSegment.from_mp3("b.mp3")
 

#获取两个输入音频的音量与时长（以毫秒为单位）
inMP3_1db=inMP3_1.dBFS
print(inMP3_1db)
inMP3_2db=inMP3_2.dBFS
inMP3_1time=len(inMP3_1)
inMP3_2time=len(inMP3_2)
#调整两个音频的音量
db=inMP3_1db-inMP3_2db
print(db)
if db>0:
    inMP3_1+=abs(db)
elif db<0:
    inMP3_2+=abs(db)
#合并音频并保存
outMP3=inMP3_1+inMP3_2
outMP3.export("1.mp3",format='mp3')
outMP3.export("2.mp3",format="mp3",bitrate='192k')
 
print(len(inMP3_1),len(inMP3_2))
print(len(outMP3),outMP3.channels)

'''






