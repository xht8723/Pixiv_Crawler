import urllib2
import cookielib
import urllib
import re

pixivurl = 'http://www.pixiv.net/'
posturl = 'https://www.pixiv.net/login.php'
markeduserurl = 'http://www.pixiv.net/bookmark.php?type=user'


postdata = urllib.urlencode({'mode':'login', 'pixiv_id':'wawa8723','pass':'09310501','skip':'1'})
cookies = cookielib.MozillaCookieJar('cookie.84')
handler = urllib2.HTTPCookieProcessor(cookies)
opener = urllib2.build_opener(handler)
response = opener.open(posturl,postdata)
cookies.save(ignore_discard=True, ignore_expires=True)


openMarkpage = opener.open(markeduserurl)
markpage=openMarkpage.read()
users=re.findall('member\.php\?id=(\d+)',markpage)


for everyuser in users:
	userpageurl = 'http://www.pixiv.net/member_illust.php?id='+everyuser
	openuserpage = opener.open(userpageurl)
	userpage=openuserpage.read()
	illustid=re.findall('member_illust.php\?mode=medium&illust_id=(\d+)',userpage)
	print illustid
	for everyillust in illustid:
		illusturl = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id='+everyillust
		openillustpage = opener.open(illusturl)
		illustpage=openillustpage.read()
		image=re.search('(http://i\d\.pixiv\.net/img-original/.+\.(jpg|png))',illustpage)
		print image










