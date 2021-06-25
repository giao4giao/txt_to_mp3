import os,shutil
from subprocess import call,PIPE


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

