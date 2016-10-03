

def getData(fname):
	global strList
	fh=open(fname,'r')

	for line in fh:
		line=line.strip()
		temp=line.strip().split(':')
		if len(temp)>1:
			temp=line[9:]
			strList.append(temp)

fnames=["DSTC1.txt","DSTC2.txt","DSTC3.txt"]
strList=[]
for i in fnames:
	getData(i)

print len(strList)
		
