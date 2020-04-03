import codecs
filepath = 'reneeyu_ph2ori.txt'  
keypath  = 'reneeyu_ph2key.txt'

mydict = {}
with codecs.open(keypath,'r','utf-16') as f:
    for line in f:
       key = line[5:6]
       val = line[0] + line[2]
#       print(key+val)
       mydict[key] = val

print(u'脚', mydict.get(u'脚'))
print(u'本', mydict.get(u'本'))
print(u'分', mydict.get(u'分'))
print(u'享', mydict.get(u'享'))
print(u'一', mydict.get(u'一'))
# chardetect reneeyu_ph2.txt
#for row in codecs.open(keypath,'r','utf-16').readlines():
#    cstring = 
#    print(row.find(u'脚本分享网'))

#   print(row)
#   print(row.decode('utf8').encode('gbk'))
#   print(row.find(u'脚本分享网'))

# -*- coding: utf-8 -*-
# for row in open(filepath).readlines():
#  print(row)
#  print row.find(u'脚本分享网')


# with open(filepath) as fp:  
#   line = fp.readline()
#   cnt = 1
#   while line:
#       print("Line {}: {}".format(cnt, line.strip()))
#       line = fp.readline()
#       cnt += 1