import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

def getData(fname,c):
	global systemList
	global userList
	global testData	
	fh=open(fname,'r')
	count=0
	
	
	tempList=[]
		
	for line in fh:
		line=line.strip()
							
		temp=line.strip().split(':')
		if count<=c:		
			if len(temp)>1:
				temp=line[9:]	
				if line.startswith("System"):
					systemList.append(temp)
				else:
					userList.append(temp)
		else:		
			temp=line[9:]
			if line.startswith("----"):
				if len(tempList)>2:				
					testData.append(tempList)
				tempList=[]
			else:
				tempList.append(temp)
		if line.startswith("----"):
			count=count+1
					
#fnames=["DSTC1.txt","DSTC2.txt","DSTC3.txt"]
fnames = ["DSTC2.txt"]
systemList=[]
userList=[]
testData=[]

c=[2000]
#c=[900,2000,2200]
for i in range(len(fnames)):
	getData(fnames[i],c[i])
print len(systemList),len(userList)

	
	
vectorizer_system = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
vec_system=vectorizer_system.fit(systemList)
vectorized_system=vec_system.transform(systemList)

vectorizer_user = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
vec_user=vectorizer_user.fit(userList)
vectorized_user=vec_user.transform(userList)

km_system = KMeans(n_clusters=10, init='k-means++', max_iter=100, n_init=1)
km_system.fit(vectorized_system)

km_user = KMeans(n_clusters=10, init='k-means++', max_iter=100, n_init=1)
km_user.fit(vectorized_user)

#labels = km.predict(train_data_features)
#print len(labels)

#data structures for getiing cluster transition frequencies

clusterDict={}

#tracks freqent sentences in each cluster sorted in descending order
#cluster names s1 for cluster 1 in system model, u1 for cluster 1 in user model
sentenceDict={}

for i in range(len(testData)):
	print "\n\n******************************"
	curList=testData[i]
	curList=curList[1:-1]
	userConv=curList[1::2]
	systemConv=curList[0: :2]

	print systemConv
	print
	print userConv
	print 

	#test_data_features = vec.transform(curList)
	#labels = km.predict(test_data_features)




	system_features=vec_system.transform(systemConv)
	system_labels=km_system.predict(system_features)
	print system_labels

	
	user_features=vec_user.transform(userConv)
	user_labels=km_user.predict(user_features)
	print user_labels
	j=0
	k=0
	while j<len(system_labels) and k<len(user_labels):
		print system_labels[j],user_labels[k],
		

		#populate cluster dictionary
		if "s_"+str(system_labels[j]) in clusterDict:
			currentDict=clusterDict["s_"+str(system_labels[j])]
			if "u_"+str(user_labels[k]) in currentDict:
				currentDict["u_"+str(user_labels[k])]=currentDict["u_"+str(user_labels[k])]+1
			else:
				currentDict["u_"+str(user_labels[k])] = 1
			clusterDict["s_"+str(system_labels[j])]=currentDict
		else:
			temp={}
			temp["u_"+str(user_labels[k])]=1
			clusterDict["s_"+str(system_labels[j])] = temp		
		
		if (j+1)<len(system_labels):
			if "u_"+str(user_labels[k]) in clusterDict:
				currentDict=clusterDict["u_"+str(user_labels[k])]
				if "s_"+str(system_labels[j+1]) in currentDict:
					currentDict["s_"+str(system_labels[j+1])]=currentDict["s_"+str(system_labels[j+1])]+1
				else:
					currentDict["s_"+str(system_labels[j+1])] = 1
				clusterDict["u_"+str(user_labels[k])]=currentDict
			else:
				temp={}
				temp["s_"+str(system_labels[j+1])]=1
				clusterDict["u_"+str(user_labels[k])] = temp		
							
		#populate sentence dictionary
		if "s_"+str(system_labels[j]) in sentenceDict:
			currentDict=sentenceDict["s_"+str(system_labels[j])]
			if systemConv[j] in currentDict:
				currentDict[systemConv[j]]=currentDict[systemConv[j]]+1
			else:
				currentDict[systemConv[j]] = 1
			sentenceDict["s_"+str(system_labels[j])]=currentDict
		else:
			temp={}
			temp[systemConv[j]]=1
			sentenceDict["s_"+str(system_labels[j])] = temp		
		
		if "u_"+str(user_labels[k]) in sentenceDict:
			currentDict=sentenceDict["u_"+str(user_labels[k])]
			if userConv[k] in currentDict:
				currentDict[userConv[k]]=currentDict[userConv[k]]+1
			else:
				currentDict[userConv[k]] = 1
			sentenceDict["u_"+str(user_labels[k])]=currentDict
		else:
			temp={}
			temp[userConv[k]]=1
			sentenceDict["u_"+str(user_labels[k])] = temp		
		


		j=j+1
		k=k+1

#print sentenceDicit
print
print clusterDict
print
f1 = open('sentenceDict.pkl', 'wb')
f2 = open('clusterDict.pkl', 'wb')
# Pickle dictionary using protocol 0.
pickle.dump(sentenceDict, f1)
pickle.dump(clusterDict, f2)
f1.close()
f2.close()

pkl_file = open('clusterDict.pkl', 'rb')

data1 = pickle.load(pkl_file)
print data1
pkl_file.close()
	#if j<len(system_labels):
	# 	print system_labels[j],
	#print 
	
	
	
