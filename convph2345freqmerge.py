import codecs
import os
### convph2345freqmerge.py -- add mergedict freq
filepath = 'reneeyu_ph2345out.txt'  
fileout  = 'reneeyu_ph2345out_freqmerge.txt'
file999999  = 'reneeyu_ph2345out_999999merge.txt'
dictpath = 'merge_jieba.txt'
# ---------------
mergedict = {}
with codecs.open(dictpath,'r','utf-16') as f:
    for line in f:
       key = line[7:9]
       val = line[0:6].rstrip()
#       print(key+val)
       mergedict[key] = val
f.close()
# ------------------

if os.path.exists(file999999):
    os.remove(file999999)
f9 = open(file999999,'a+', encoding='utf-16') 
prev999999key = '      '
dup999999cnt = 0
#-----------------------------

if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
lineout = '02kungfu999999 功夫' 
with open(filepath,'r', encoding='utf-16') as fp:  
   line = fp.readline()
   cnt = 0
   cntout = 0
   cntout2 = 0
   cntout3 = 0
   cntout4 = 0 
   cnterr2 = 0
   cnterr3 = 0
   cnterr4 = 0 
   while line:
       if len(line) > 15 or len(line) < 10:
          print(len(line))
          print(line)
          print('**len < 10 or > 15, 7key + 4,5,6,7(utf-16)char + 1endline')
#          abort by index 
          print(line[99])
#        
# 7key + 2(utf-16)char + lf = 10
       
       if len(line) == 10:
          key1 = line[7:9]          
          val1 = mergedict.get(key1, '999900') 
          if val1 == '999900':
             if line[0:6] == prev999999key:
                dup999999cnt += 1
             else:
                dup999999cnt = 0
             prev999999key = line[0:6]
             lineout = '02'+line[0:6]+ str(int(val1)+dup999999cnt) + line[7:]
          else:
             lineout = '02' + line[0:6]+ val1 + line[7:]
          fo.write(lineout)
##  
          if int(val1)+dup999999cnt >= 999901: 
             f9.write(lineout)
             cnterr2 += 1

          if cntout2 == 0:
             print('**converting ph2...')
          cntout2 += 1

#
# 7key + 3(utf-16)char + lf = 11
       
       if len(line) == 11:
          key1 = line[7:9]
          val1 = mergedict.get(key1, '888888') 
          if val1 != '888888':
             val1 = str(int(val1)+300000).zfill(6)
          lineout = '03' + line[0:6]+ val1 + line[7:]
          fo.write(lineout)
          if cntout3 == 0:
             print('**converting ph3...')
          cntout3 += 1
#
# 7key + 4,5,6,7(utf-16)char + lf = 12,13,14,15
       
       if len(line) >= 12:
          key1 = line[7:9]
          val1 = mergedict.get(key1, '888888') 
          if val1 != '888888':
             val1 = str(int(val1)+400000).zfill(6)
          lineout = '0'+str(len(line)-12+4) + line[0:6]+ val1 + line[7:]
          fo.write(lineout)
          if cntout4 == 0:
             print('**converting ph4,5,6,7...')
          cntout4 += 1
#
       line = fp.readline()
       cnt += 1
fp.close()
fo.close()
f9.close()
cntout = cntout2+cntout3+cntout4
print('cnt=', cnt, ',cntout=', cntout)
print('cntout2=', cntout2, ',cnterr2=', cnterr2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
with open(fileout, 'r+',encoding="utf-16") as f:
    sorted_contents=''.join(sorted(f.readlines())) #, key = lambda x: int(x.split(' ')[0])))
    f.seek(0)
    f.truncate()
    f.write(sorted_contents)
print(fileout,' sorted OK')
