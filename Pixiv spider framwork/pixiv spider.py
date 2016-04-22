import urllib2
import cookielib
import urllib
import re
import sys
import os

pixivurl = 'http://www.pixiv.net/'
posturl = 'https://www.pixiv.net/login.php'
markeduserurl = 'http://www.pixiv.net/bookmark.php?type=user&rest=show&p='
userpageurl = 'http://www.pixiv.net/member_illust.php?id='


print 'Welcome to pixiv crawler!------By Hantian Xiao(Hamame Yakoto)'
print 'My email: gakki@luv84.cn'
print 'Spam welcomed :P'

INPUT_id = raw_input('Your pixiv id:')
INPUT_pas = raw_input('Your password:')


##Creat cookie for login.
print 'Creating cookie...'
postdata = urllib.urlencode({'mode':'login', 'pixiv_id':INPUT_id,'pass':INPUT_pas,'skip':'1'}) ## Your pixiv id and password.
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





##Check the illusts already downloaded.
allfiles = os.listdir(os.getcwd())
duplicatelist = []
for everyfile in allfiles:
	try:
		duplicatelist.append(re.findall('id_(\d+)\.png',everyfile)[0])
	except(IndexError):
		continue

duplicatetxt = open('Illusts_already_downloaded.txt','w')
for temp in duplicatelist:
	duplicatetxt.write(temp+',')
duplicatetxt.close()



##Record all image id needs to download
print 'Creating illust id log...'
print 'This may take quite many hours...depands on how many pictures to download\n'
print 'Like me, I got 14 pages of marked artists(654 artists), it took me over 24 hours...(Yea, its like 30,000 pictures)\n'
print 'Also, a kindly remind, you should check you hard disk to see if theres enough room...(So 30,000 pictures is like 20GB)\n'
print 'Doing some works.....'
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
			if everyillust in duplicatelist:
				continue
			if everyillust not in duplicate_check:
				Marked_users_illust_id.write(everyillust+',')
				duplicate_check.append(everyillust)
Marked_users_illust_id.close()
del duplicatelist
del pages
del pagenum
del duplicate_check





##create a list of image id
Marked_users_illust_id = open('illust_id.txt','r')
illusts=Marked_users_illust_id.read()
illustlist=illusts.split(',')
Marked_users_illust_id.close()
illustlist.pop()






print 'Downloading...'
cookie84 = open('cookie.84','r').read()
device_token = re.findall('device_token\s+(.+)\n',cookie84)[0]
phpsessid = re.findall('PHPSESSID\s+(.+)\n',cookie84)[0]
module_orders_mypage = re.findall('module_orders_mypage\s+(.+)\n',cookie84)[0]
p_ab_id = re.findall('p_ab_id\s+(.+)\n',cookie84)[0]

for everyid in illustlist:
	illusturl='http://www.pixiv.net/member_illust.php?mode=medium&illust_id='+everyid
	request = urllib2.Request(illusturl)
	openimagepage = opener.open(illusturl)
	imagepage = openimagepage.read()
	imageurl = re.findall('data-src="(http://.+)" class="original-image"',imagepage)
	if len(imageurl) == 0:
		continue	
	hostnum = re.findall('(i\d\.pixiv\.net)',imageurl[0])
	referer = 'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=' + everyid
	data = {
	
			'Accept': 'image/webp,image/*,*/*;q=0.8',
			
			'Accept-Encoding':'gzip, deflate, sdch',
			
			'Accept-Language':'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
			
			'Connection':'keep-alive',
			
			'Cookie':'p_ab_id='+p_ab_id+'; device_token='+device_token+'; PHPSESSID='+phpsessid+'; module_orders_mypage='+module_orders_mypage+'; __utmb=235335808.19.10.1461180741; __utmc=235335808; __utmz=235335808.1460079625.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=235335808.|2=login%20ever=yes=1^3=plan=premium=1^5=gender=male=1^6=user_id=3271470=1',
			
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













