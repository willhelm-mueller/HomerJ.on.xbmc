# -*- coding: utf-8 -*-
#!/usr/bin/python
import sys
import urllib, urllib2
import re
# encoding for the video urls
import base64

urlHost = "http://homerj.de"


def encodeString(inString):
	for old, new in (('&szlig;', 'ß'),( '&auml;','ä'),( '&Auml;','Ä'),( '&uuml;','ü'),( '&Uuml;','Ü'),( '&ouml;','ö'),( '&Ouml;','Ö')):
		inString = inString.replace(old, new)
	return inString

def getStreamUrl(url='http://homerj.de/index.php?show=vods&play=3688',res="720p"):
#720p 1080p ? 
	vod_decoded = 0
	url = url + "&res=" +res
	req = urllib2.Request(url)
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
#	match=re.compile("base64_decode\('(\w*)").findall(link)
	match=re.search("loadPlayer\('([\w\W]*)','fp",link)
	print match
#	print match
# urls are hided via a base64 decoding .... 
	if match:
		match = match.group(1)
		print match
		vod_decoded = base64.b64decode(match)
		print vod_decoded
		vod_decoded =  re.search('"stream":"([\w\W]*.mp4)"',vod_decoded).group(1)
		vod_decoded = vod_decoded.replace('\\','')
		print vod_decoded
	return vod_decoded
	
def index(category):
	
	req = urllib2.Request(category)
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link= link.split('<a name="overview">',1)[1]
#getting recently added vods 
	urls=re.compile('<a href="(index\.php\?show=vods&amp;play=\d*)"').findall(link)
#eliminate double urls 
	temp =[]
	for url in urls:
		if url not in temp:
			temp.append(url)
	urls =temp
	names = re.compile('<img class="b_1" style="position:absolute; z-index:1;".*alt="(.*)"' ).findall(link)
	images = re.compile('src="(http://homerj.de/files/vods/.*)" width' ).findall(link)
	for i  in range (len(urls)):
		urls[i] = urls[i].replace('&amp;','&')
		urls[i] = 'http://homerj.de/'+urls[i]
		url = getStreamUrl(urls[i],res='720p')
#fsk 18 links are only available from 22:00 to 6:00 (10pm to 6 am)
		names[i]=encodeString(names[i])
		if url:
#			addLink(name=names[i], url=url,iconimage=images[i])

## adding prev / next pages
	if re.compile('<a href="(.*)">vorherige Seite</a> ').findall(link):
		previousPageUrl = re.compile('<a href="(.*)">vorherige Seite</a> ').findall(link)[0]
		previousPageUrl =urlHost+'/' +previousPageUrl
		previousPageUrl = previousPageUrl.replace('&amp;','&')
#		addDir('Vorherige Seite',previousPageUrl,'1')
		
	if 	re.compile('<a href="(.*)">n&auml;chste Seite</a>').findall(link):
		nextPageUrl = re.compile('<a href="(.*)">n&auml;chste Seite</a>').findall(link)[0]
		nextPageUrl =urlHost+'/' +nextPageUrl
		nextPageUrl = nextPageUrl.replace('&amp;','&')
#		addDir('Naechste Seite',nextPageUrl,1)

def categories(categoryUrl="http://homerj.de/index.php?show=vods"):
	req = urllib2.Request(categoryUrl)
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()	
	categoryUrls=re.compile('<a href="(index\.php\?show=vods&amp;cat=\d*#overview)').findall(link)
	categoryNames = re.compile('<a href="index\.php\?show=vods&amp;cat=\d*#overview.*alt="(.*)" src').findall(link)
	categoryImages = re.compile('<a href="index\.php\?show=vods&amp;cat=\d*#overview.*alt=".*" src="(.*)">').findall(link)
#        print categoryImages
	for i in range(len(categoryUrls)):
		url = urlHost+'/'+ categoryUrls[i]
		url = url.replace('&amp;','&')
		imageUrl =  urlHost+'/'+categoryImages[i]
		categoryNames[i].encode("utf-8")
		categoryNames[i] = encodeString(categoryNames[i])
#		addDir(categoryNames[i],url, 1,imageUrl) 
## adding podcasts category	
#	podUrl = "http://www.homerj.de/index.php?show=podcast"
#	addDir("Podcasts",podUrl,1,"http://www.homerj.de/images/design/homerj_podcast_170x170.jpg")
# 	print "--- showContent ok"	
