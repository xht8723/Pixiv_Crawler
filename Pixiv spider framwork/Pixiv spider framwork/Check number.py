f = open('Marked_users.txt','r')
temp = f.read()

temp2=temp.split(',')
temp2.pop()

print 'Marked users:',len(temp2)
f.close()

f = open('illust_id.txt','r')

temp = f.read()

temp2=temp.split(',')
temp2.pop()

print 'illusts:',len(temp2)
