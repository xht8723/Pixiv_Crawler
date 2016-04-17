import urllib2
import cookielib
import urllib
import re

pixivurl = 'http://www.pixiv.net/'
posturl = 'https://www.pixiv.net/login.php'
markeduserurl = 'http://www.pixiv.net/bookmark.php?type=user'

##Creat cookie for login.
postdata = urllib.urlencode({'mode':'login', 'pixiv_id':'********','pass':'********','skip':'1'}) ## Your pixiv id and password.
cookies = cookielib.MozillaCookieJar('cookie.84')
handler = urllib2.HTTPCookieProcessor(cookies)
opener = urllib2.build_opener(handler)
response = opener.open(posturl,postdata)
cookies.save(ignore_discard=True, ignore_expires=True)




##Open your mared user page and find all user id
openMarkpage = opener.open(markeduserurl)
markpage=openMarkpage.read()
users=re.findall('member\.php\?id=(\d+)', markpage)
marked_user_log = open('Marked_users.txt','w')
duplicate_check=[]
for everyuser in users:
	if everyuser not in duplicate_check:
		marked_user_log.write(everyuser+',')
		duplicate_check.append(everyuser)
marked_user_log.close()






##Record all image id needs to download
Marked_users_illust_id=open('illust_id.txt','w')
for everyuser in users:
	userpageurl = 'http://www.pixiv.net/member_illust.php?id=' + everyuser
	openuserpage = opener.open(userpageurl)
	userpage = openuserpage.read()
	illustid=re.findall('/member_illust\.php\?mode=medium&amp;illust_id=(\d+)',userpage)
	duplicate_check=[]
	for everyillust in illustid:
		if everyillust not in duplicate_check:
			Marked_users_illust_id.write(everyillust+',')
			duplicate_check.append(everyillust)
Marked_users_illust_id.close()


##create a list of image id
Marked_users_illust_id = open('illust_id.txt','r')
illusts=Marked_users_illust_id.read()
illustlist=illusts.split(',')
Marked_users_illust_id.close()
illustlist.pop()


##start downloading
for everyid in illustlist:
	illusturl='http://www.pixiv.net/member_illust.php?mode=medium&illust_id='+everyid
	openimagepage = opener.open(illusturl)
	imagepage = openimagepage.read()
	imageurl = re.findall('data-src="(http://.+)" class="original-image"',imagepage)	
	openfinal = opener.open(imageurl)
	filename='id_'+everyid+'.png'
	urllib.urlretrieve(imageurl[0],filename)














