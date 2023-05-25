import codecs
import os
filepath = 'reneeyu_canph234ori.txt'  
###filepath = 'reneeyu_canph234ori_aftshifttwchi.txt'  
fileout  = 'reneeyu_canph234ori_freqtwchi.txt'
file999999  = 'reneeyu_canph234ori_999999twchi.txt'
keypathtwchi  = 'twchi_10000_ph2freq.txt'
keypathbaidu  = 'baiduchifu_ph2.txt'
keypathchiss  = 'chisiusuet_500000_ph2.txt'

#-----------------------------
dictline = '000001 我們'
dictcnt = 0
mydictchiss = {}
with codecs.open(keypathtwchi,'r','utf-16') as f:
    for line in f:
       dictcnt += 1
       key = line[7:9]
       val = str(dictcnt).zfill(6)
#       print(key+val)
       valdict = mydictchiss.get(key,'??????')
# prevent duplicate key dict
       if valdict == '??????':
          mydictchiss[key] = val
f.close()
#-------------
dictline = '4 公共'
##dictcnt = 0 ## baidu dictcnt continued after chiss
##mydictbaidu = {}
with codecs.open(keypathbaidu,'r','utf-16') as f:
    for line in f:
       dictcnt += 1
       key = line[2:4]
       val = str(dictcnt).zfill(6)
#       print(key+val)
       valdict = mydictchiss.get(key,'??????')
# prevent duplicate key dict
       if valdict == '??????':
          mydictchiss[key] = val
f.close()

#-----------------------------
dictline = '000001 一個 999999'
##dictcnt = 0
##mydictchiss = {}
with codecs.open(keypathchiss,'r','utf-16') as f:
    for line in f:
       dictcnt += 1
       key = line[7:9]
       val = str(dictcnt).zfill(6)
#       print(key+val)
       valdict = mydictchiss.get(key,'??????')
# prevent duplicate key dict
       if valdict == '??????':
          mydictchiss[key] = val
f.close()
# ---------------

if os.path.exists(file999999):
    os.remove(file999999)
f9 = open(file999999,'a+', encoding='utf-16') 
if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
lineout = '02kungfu999999 功夫' 
prev999999key = '      '
dup999999cnt = 0
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
       if len(line) > 12 or len(line) < 10:
          print(len(line))
          print(line)
          print('**len < 10 or > 12, 7key + 4(utf-16)char + 1endline')
#          abort by index 
          print(line[99])
#        
# 7key + 2(utf-16)char + lf = 10

       if len(line) == 10:
          key1 = line[7:9]          
          val1 = mydictchiss.get(key1, '999900') 
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
             print('**converting canph2...') 
          cntout2 += 1           
#
# 7key + 3(utf-16)char + lf = 11
       
       if len(line) == 11:
          key1 = line[7:9]
          val1 = mydictchiss.get(key1, '999999') 
          lineout = '03' + line[0:6]+ val1 + line[7:]
          fo.write(lineout)
          if cntout3 == 0:
             print('**converting canph3...')
          cntout3 += 1
#
# 7key + 4(utf-16)char + lf = 12
       
       if len(line) == 12:
          key1 = line[7:9]
          val1 = mydictchiss.get(key1, '999999') 
          lineout = '04' + line[0:6]+ val1 + line[7:]
          fo.write(lineout)
          if cntout4 == 0:
             print('**converting canph4...')
          cntout4 += 1
#
       line = fp.readline()
       cnt += 1
fp.close()
fo.close()
cntout = cntout2+cntout3+cntout4
print('cnt=', cnt, ',cntout=', cntout)
print('cntout2=', cntout2, ',cnterr2=', cnterr2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
