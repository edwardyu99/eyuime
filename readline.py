import codecs
filepath = 'reneeyu_ph2.txt'  

# -*- coding: gbk
# chardetect reneeyu_ph2.txt
for row in codecs.open(filepath,'r','utf-16').readlines():
   print(row)
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