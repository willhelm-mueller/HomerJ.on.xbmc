import xbmcplugin,xbmcgui
import sys
import urllib, urllib2
import re
import base64

urlHost = "http://homerj.de"
#testing and debugging :
#categoryUrl = "http://homerj.de/index.php?show=vods&cat=2#overview"
#streamUrl = "http://homerj.de/index.php?show=vods&play=3688&res=720p"
#categoryOverview= "http://homerj.de/index.php?show=vods"
# until here


def get_params():
	param=[]
	if len(sys.argv) > 1:
		paramstring=sys.argv[2]
		if len(paramstring)>=2:
			params=sys.argv[2]
			cleanedparams=params.replace('?','')
			if (params[len(params)-1]=='/'):
				params=params[0:len(params)-2]
				pairsofparams=cleanedparams.split('&')
				param={}
				for i in range(len(pairsofparams)):
					splitparams={}
					splitparams=pairsofparams[i].split('=')
					if (len(splitparams))==2:
						param[splitparams[0]]=splitparams[1]
                                
	return param


def addDir(name,url,mode,iconimage=''):
#	u = urllib.quote_plus(url)
	u=sys.argv[0]+"&url="+urllib.quote_plus(url)+"&mode="+str(mode)+"name="+urllib.quote_plus(name)
#	u=sys.argv[0]+urllib.quote_plus(url)
	liz=xbmcgui.ListItem(unicode(name), iconImage="DefaultFolder.png",thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name })
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
	return ok


def getStreamUrl(url='http://homerj.de/index.php?show=vods&play=3688',res="720p"):
#720p 1080p ? 
	url = url + "&res=" +res
	print url
	req = urllib2.Request(url)
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile("base64_decode\('(\w*)").findall(link)
	
# urls are hgided via a base64 decoding .... 
	vod_decoded = base64.b64decode(match[0])
	print vod_decoded
	return vod_decoded

def index(category):
	
	req = urllib2.Request(category)
#	print category, "hust hust hust \n"
	req.add_header('User-Agent', ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link= link.split('<a name="overview">',1)[1]
#getting recenttly added vods 
	urls=re.compile('<a href="(index\.php\?show=vods&amp;play=\d*)"').findall(link)
	#eliminate double urls 
	temp =[]
	for url in urls:
		if url not in temp:
			temp.append(url)
	urls =temp
	names = re.compile('<img class="b_1" style="position:absolute; z-index:1;".*alt="(.*)"' ).findall(link)
#	print names 

	for i  in range (len(urls)):
		urls[i] = urls[i].replace('&amp;','&')
		urls[i] = 'http://homerj.de/'+urls[i]
#		print urls[i]
		url = getStreamUrl(urls[i],res='720p')

		addLink(name=names[i], url=url,iconimage=' ')

## adding prev / next pages
	if re.compile('<a href="(.*)">vorherige Seite</a> ').findall(link):
		previousPageUrl = re.compile('<a href="(.*)">vorherige Seite</a> ').findall(link)[0]
		previousPageUrl =urlHost+'/' +previousPageUrl
		previousPageUrl = previousPageUrl.replace('&amp;','&')
		addDir('Vorherige Seite',previousPageUrl,'1')
		
	if 	re.compile('<a href="(.*)">n&auml;chste Seite</a>').findall(link):
		nextPageUrl = re.compile('<a href="(.*)">n&auml;chste Seite</a>').findall(link)[0]
		nextPageUrl =urlHost+'/' +nextPageUrl
		nextPageUrl = nextPageUrl.replace('&amp;','&')
		addDir('Naechste Seite',nextPageUrl,1)
#### getting next page

		 
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
#		print categoryNames[i],url

		addDir(categoryNames[i],url, 1) 
		
 	print "--- showContent ok"	
	
# ----- main -----

print "hello"              
params=get_params()
url=None
name=None
mode=None


#print params
print sys.argv

if  sys.argv[0] == 'plugin://plugin.video.homerj/':
	print "parsing categories"
	categories()
	xbmcplugin.endOfDirectory(handle=int(sys.argv[1])) 

 
#elif mode==1:
elif re.search('overview', sys.argv[0]) or re.search('start', sys.argv[0]) :
	url = sys.argv[0]
	print url
	url = url.split('&url=',1)[1]
	url = url.split('&mode=',1)[0]
	url = urllib.unquote_plus(url)
#	print "hase "+url
	index(category=url)
	xbmcplugin.endOfDirectory(handle=int(sys.argv[1])) 
'''
elif re.search('play', sys.argv[2]):
	print "yo plaing",sys.argv[2]
	url = url.split('&url=',1)[1]
	url = url.split('&mode=',1)[0]
	print url
	url = urllib.unquote_plus(url)
'''
