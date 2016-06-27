import urllib2
def findChar(s):
	for i in range(0,len(s)):
		if s[i]=='"':
			return i
	return 0

def replaceSpace(s):
	for i in range(0,len(s)):
		if s[i]==' ':
			p=s[0:i]
			q=s[i+1:]
			s=p + "%20" + q
	return s

def convertToName(s):
	for i in range(0,len(s)-3):
		if s[i:i+3]=='%20':
			p=s[0:i]
			q=s[i+3:]
			s=p + " " + q
	return s[:-1]

def giveResponse(url):
	u= urllib2.urlopen(url)
	inp=u.read()
	return inp

def download(url):
	u= urllib2.urlopen(url)
	file_name = url.split('/')[-1]
	file_name = file_name + '/'
	file_name = convertToName(file_name)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_name, file_size)
	file_size_dl = 0
	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break

	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print status,

	f.close()

def compare(str1,str2):
        if str1.lower()==str2.lower():
                return 1
        else :
                return 0


#initialization
url = "http://sv1.bia2dl.xyz/Series/"
listOfSeries=[]
inp = giveResponse(url)
for i in range(0,len(inp)-4):
	s=inp[i:i+4]
	if s=='href':
		temp = inp[i+6:]
		temp= temp[:findChar(temp)]
		if temp[-1:]=='/' and temp[-2:-1]!='.':
			#print(temp)
			listOfSeries = listOfSeries + [convertToName(temp),]

for j in range(0,len(listOfSeries),2):
        if j+1==len(listOfSeries):
                print(j, listOfSeries[j])
        else:
                print(j, listOfSeries[j],"             ", j+1, listOfSeries[j+1]) 

# number of times you wanna run the loop
for _ in range(0,10):
	try:
		print("Select the number of series from the list or Enter the name of Series to download")
		nameOfSeries= str(raw_input())
		val =0 
                for x in listOfSeries:
                        if compare(x,nameOfSeries)==1:
                                nameOfSeries=x
                                val=1
                                break
		if val==0 :
			nameOfSeries=listOfSeries[int(nameOfSeries)]


		nameOfSeries= replaceSpace(nameOfSeries)

		newurl = url + nameOfSeries + "/"

		inp = giveResponse(newurl)
		#print(inp)


		ar= []
		for i in range(0,len(inp)-4):
			s=inp[i:i+4]
			if s=='href':
				temp = inp[i+6:]
				temp= temp[:findChar(temp)]
				if temp[-1:]=='/' and temp[-2:-1]!='.':
					ar = ar + [temp,]

		newurl  = newurl + ar[-1]
		inp1=giveResponse(newurl)

		for i in range(0,len(inp1)-4):
			s=inp1[i:i+4]
			if s=='href':
				temp = inp1[i+6:]
				temp= temp[:findChar(temp)]
				ar = ar + [temp,]
		print(ar[-1])

		newurl  = newurl + ar[-1]
		print(newurl)
		download(newurl)
	except:
		print("Try Again")
