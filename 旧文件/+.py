import subprocess


file_name,mp4_file='a.mp3','b.mp3'
outfile_name =file_name.split('.')[0]+'-new.mp3'
cmd ='D:\\ffmpeg-3.4.1\\ffmpeg -i {} -i {} -acodec copy -vcodec copy {}'
cmd =cmd.format(mp4_file,file_name,outfile_name)
print(cmd)
subprocess.call(cmd,shell=True)


