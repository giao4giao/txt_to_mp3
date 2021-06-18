import os,shutil
from subprocess import call,PIPE



def hcsound(soundlist,outfile):
	# print(soundlist)
	i=0
	if len(soundlist)==1:
		shutil.copy(soundlist[0],outfile)
	else:
		for sound in soundlist:
			i+=1
			if i==1:
				delfile(outfile)
				shutil.copy(sound,outfile)
			else:
				tempfile=outfile+'_t.mp3'
				cmd='D:\\ffmpeg-3.4.1\\ffmpeg -i {} -i {} -filter_complex "[0:0] [1:0] concat=n=2:v=0:a=1 [a]" -map [a] {} '
				cmd =cmd.format(outfile,sound,tempfile)
				call(cmd,shell=True ,stdout=PIPE,stderr=PIPE)
				shutil.move(tempfile,outfile)
			print(i)


# sound='a.mp3'
# outfile='b.mp3'
# tempfile='new.mp3'
# cmd='D:\\ffmpeg-3.4.1\\ffmpeg -i {} -i {} -filter_complex "[0:0] [1:0] concat=n=2:v=0:a=1 [a]" -map [a] {} '
# cmd =cmd.format(sound,outfile,tempfile)
# p=call(cmd,shell=True ,stdout=subprocess.PIPE,stderr=subprocess.PIPE)



for root,dirs,file in os.walk('.'):
	# print((root,dirs,file))
	if root =='.\\music':
		root=root.replace('.\\','')+'/'
		soundlist=[root+i for i in file]
# # print(soundlist)
# hcsound(soundlist,'new.mp3')

# import subprocess
# sound='music/1.mp3'
# outfile='music/2.mp3'
# firfile='music/3.mp3'
tempfile='new.mp3'
# cmd='D:\\ffmpeg-3.4.1\\ffmpeg -i {} -i {} -i {} -filter_complex "[0:0] [1:0] concat=n=3:v=0:a=1 [a]" -map [a] {} '
# cmd =cmd.format(sound,outfile,firfile,tempfile)
# call(cmd,shell=True ,stdout=subprocess.PIPE,stderr=subprocess.PIPE)


cmd_part_1='D:\\ffmpeg-3.4.1\\ffmpeg '
cmd_part_2=''
for sound in soundlist:
	cmd_part_2+='-i {} '.format(sound)
cmd_part_3='-filter_complex "[0:0] [1:0] concat=n={}:v=0:a=1 [a]" -map [a] {} '
cmd_part_3 =cmd_part_3.format(str(len(soundlist)),tempfile)
cmd=cmd_part_1+cmd_part_2+cmd_part_3
# call(cmd,shell=True ,stdout=PIPE,stderr=PIPE)
call(cmd)
