import os

d=[]
for i in os.walk('.'):
	for l in i[2]:
		if os.path.splitext(l)[1]=='.mp3':
			d.append(l)

def ddd(d,n):
	l=[]
	for ii in d:
		new=''
		num,end=os.path.splitext(ii)
		num1="0123456789"
		num2=['零','一','二','三','四','五','六','七','八','九']
		if n==2:
			num2,num1=''.join(num2),list(num1)
			for i in num:
			    for j in num2:
			        print(i,j)
			        if i==j:
			        	new+=num1[int(j)]
			        	print(new)
			        	l.append(new+end)
		else:
			for i in num:
			    for j in num1:
			        if i==j:
			        	new+=num2[int(j)]	
			        	l.append(new+end)
	print(l)

n=2
print(d[0])
ddd(d[0],n)



#for i in range(0,len(l)):
	#os.rename(d[i],l[i])
#	os.rename(l[i],d[i])

