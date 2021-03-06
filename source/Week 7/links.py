import re
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup, SoupStrainer
import zipfile
import os
import shutil

baseURL= 'http://apps1.eere.energy.gov/buildings/energyplus/weatherdata_about.cfm'


countrylinks = []
regionlinks = []
files = []

website=urllib2.urlopen(baseURL)
html=website.read()

def getlinks(page,alist):
	soup = BeautifulSoup(page)
	for link in soup.findAll('a'):
		if link.has_key('href') and link['href'] not in alist:
			alist.append(link['href'])
mainlinks = []		
getlinks(html,mainlinks)		

for i in mainlinks:
	if i not in regionlinks and re.findall("/buildings/energyplus/cfm/weather_data2.cfm/region*", i ):
		regionlinks.append('http://apps1.eere.energy.gov/'+i)
"""
for i in regionlinks:
	print i
"""
for i in regionlinks:
	openingURL=urllib2.urlopen(i)
	response = openingURL.read()
	regionpagelinks=[]
	getlinks(response,regionpagelinks)
	
	
	for k in regionpagelinks:
		if k not in countrylinks and  re.findall("/buildings/energyplus/cfm/weather_data3.cfm/region*", k):
			countrylinks.append('http://apps1.eere.energy.gov/' + k)




					
	
l=[]
for i in countrylinks:
	request = urllib2.Request(i)

	response = urllib2.urlopen(request)

	t= []
	soup = BeautifulSoup(response)
	for link in soup.findAll('a'):
		if link.has_key('href') and link['href'] not in t:
			t.append(link['href'])


	for j in t:
		v= re.findall(".*\.zip", j)
		if v:
			l.append(v[0])

	for c in l:
		print c



for url in l: 
	myurl = 'http://apps1.eere.energy.gov/' + url 
	file_name = url.split('/')[-1]
	u = urllib2.urlopen(myurl)
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
	fh= open(file_name, 'rb')
	z= zipfile.ZipFile(fh)
	for name in z.namelist():
		if re.findall(".*\.epw",name):
			print "Extracting file " +  name
			z.extract(name)
	

	fh.close()
	print 'Deleting '+ file_name
	os.remove(file_name)



