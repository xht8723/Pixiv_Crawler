import urllib2
import cookielib
import urllib
import re
import sys

pixivurl = 'http://www.pixiv.net/'
posturl = 'https://www.pixiv.net/login.php'
markeduserurl = 'http://www.pixiv.net/bookmark.php?type=user&rest=show&p='
userpageurl = 'http://www.pixiv.net/member_illust.php?id='



##Creat cookie for login.
print 'Creating cookie...'
postdata = urllib.urlencode({'mode':'login', 'pixiv_id':'wawa8723','pass':'Chenyiming504','skip':'1'}) ## Your pixiv id and password.
cookies = cookielib.MozillaCookieJar('cookie.84')
handler = urllib2.HTTPCookieProcessor(cookies)
opener = urllib2.build_opener(handler)
response = opener.open(posturl,postdata)
cookies.save(ignore_discard=True, ignore_expires=True)






##Open your mared user page and find all user id
print 'Counting marked user page number...'
openMarkpage = opener.open(markeduserurl+'1')
markpage = openMarkpage.read()
pages = re.findall('bookmark\.php\?type=user&amp;rest=show&amp;p=(\d+)',markpage)
pagenum = []

for everypage in pages:
	if everypage not in pagenum:
		pagenum.append(everypage)
Maxpagenum = pagenum[len(pagenum)-1]

while(True):
	pagelen = len(pagenum)
	openMarkpage = opener.open(markeduserurl+Maxpagenum)
	markpage = openMarkpage.read()
	pages = pages = re.findall('bookmark\.php\?type=user&amp;rest=show&amp;p=(\d+)',markpage)
	
	for everypage in pages:
		if everypage not in pagenum:
			pagenum.append(everypage)
	
	Maxpagenum = pagenum[len(pagenum)-1]

	if pagelen == len(pagenum):
		break

print 'Creating marked user log...'
duplicate_check = []
marked_user_log = open('Marked_users.txt','w')
for everypage in pagenum:
	openMarkpage = opener.open(markeduserurl+everypage)
	markpage = openMarkpage.read()
	users = re.findall('member\.php\?id=(\d+)"', markpage)
	for everyuser in users:
		if everyuser not in duplicate_check:
			marked_user_log.write(everyuser+',')
			duplicate_check.append(everyuser)
marked_user_log.close()







##Create userslist
Marked_users = open('Marked_users.txt','r')
userslist = Marked_users.read().split(',')
Marked_users.close()
userslist.pop()






##Record all image id needs to download
print 'Creating illust id log...'
print 'This may take quite many hours...depands on how many pictures to download'
print 'Like me, I got 14 pages of marked artists(654 artists), it took me over 24 hours...(Yea, its like 50,000 pictures)'
print 'Also, a kindly remind, you should check you hard disk to see if theres enough room...(So 50,000 pictures is like 50GB)'
print '.....'
Marked_users_illust_id=open('illust_id.txt','w')
for everyuser in userslist:
	openuserpage = opener.open(userpageurl+everyuser)
	userpage = openuserpage.read()
	pages = re.findall('\?id=\d+&amp;type=all&amp;p=(\d+)',userpage)
	pagenum = []
	for everypage in pages:
		if everypage not in pagenum:
			pagenum.append(everypage)

	for everypage in pagenum:
		temppage = 'http://www.pixiv.net/member_illust.php?id='+everyuser+'&type=all&p='+everypage 
		openuserpage = opener.open(temppage)
		userpage = openuserpage.read()
		illustid = re.findall('/member_illust\.php\?mode=medium&amp;illust_id=(\d+)',userpage)
		duplicate_check = []
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
print 'Downloading...'
for everyid in illustlist:
	illusturl='http://www.pixiv.net/member_illust.php?mode=medium&illust_id='+everyid
	request = urllib2.Request(illusturl)
	openimagepage = opener.open(illusturl)
	imagepage = openimagepage.read()
	imageurl = re.findall('data-src="(http://.+)" class="original-image"',imagepage)
	if len(imageurl) == 0:
		continue	
	hostnum = re.findall('(i\d\.pixiv\.net)',imageurl[0])
	referer = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id='+ everyid
	data = {
	
			'Accept': 'image/webp,image/*,*/*;q=0.8',
			
			'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
			
			'Connection':'keep-alive',
			
			'Cookie':'p_ab_id=1; device_token=2e626a73bae4d1ab278b48b8fb2a2b18; PHPSESSID=3271470_bfc19558818bfe3737bc000e7ad071fa; module_orders_mypage=%5B%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; __utmt=1; __utma=235335808.542522510.1459631616.1461126162.1461137622.17; __utmb=235335808.2.10.1461137622; __utmc=235335808; __utmz=235335808.1460079625.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=235335808.|2=login%20ever=yes=1^3=plan=premium=1^5=gender=male=1^6=user_id=3271470=1',
			
			'Host': hostnum[0],
			
			'Referer': referer,
			
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
			
	}
	post = urllib.urlencode(data)
	req = urllib2.Request(imageurl[0],None,data)
	finalopen = opener.open(req)
	filename = 'id_'+everyid+'.png'
	f = open(filename,'wb')
	f.write(finalopen.read())
	f.close()













