import codecs
import os
filepath = 'chisiusuet_more.txt'  
fileout  = 'chisiusuet_more_ph2.txt'
filedup  = 'chisiusuet_more_ph2dup.txt'
#filepath = 'reneeyu_canph234ori.txt'  
#fileout  = 'reneeyu_canph234out.txt'
#filedup  = 'reneeyu_canph234outdup.txt'
#keypath  = 'reneeyu_canph2key.txt'
keypath  = 'reneeyu_canph2key.txt'
#keypath  = 'reneeyu_canph2keych2c.txt'
# ---------------
# mydict12 = {}
# with codecs.open(keypath12,'r','utf-16') as f:
#    for line in f:
#       key = line[5]
#       val = line[0:2].rstrip()
#       print(key+val)
#       mydict12[key] = val
# f.close()

dictcnt = 0
mydict = {}
with codecs.open(keypath,'r','utf-16') as f:
    for line in f:
        if len(line) != 10:
          print(len(line))
          print(line)
        key = line[7]
        val = line[0:4]
# prevent duplicate key dict
        valdict = mydict.get(key,'????')
        if valdict == '????':
           mydict[key] = val
f.close()

if os.path.exists(filedup):
    os.remove(filedup)
fd = open(filedup,'a+', encoding='utf-16') 
if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
line    = '一個>999999'
lineout = '000001一個' 
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
   cntdup2 = 0
   prevkey2 = '  '
   while line:    
#        
# 2(utf-16)char + tab + ' 999999'   
       if line[2] == '\t':
          key1 = line[0:2]
#          key2 = line[1]
#       print(key1)
#          val1 = mydict.get(key1, 'xxxx')      
#          val2 = mydict.get(key2, 'xxxx')
#          if val1 == 'xxxx' or val2 == 'xxxx':
#             print(key1)
#             print(val1)
#             print(key2)
#             print(val2)
#             print(line)
#             cnterr2 += 1
#          val = val1.rstrip() + val2
#          if len(val) > 6:
#             val = val[0]+val[1]+val[2]+val[3]+val[4]+val[5]
#          print(val)
#          val = str(1000000 - int(line[3:9]))
#          val = str(100001 + cntout2)
          val = str(cntout2+1).zfill(6)
          freq = line[3:] 
          lineout = val + ' ' +key1 + ' ' + freq
          fo.write(lineout)
#          fo.write(lineout+'\n')
          if cntout2 == 0:
             print('**convering chisiusuetph2...')
          cntout2 += 1
# output dupkey2 to fd
          if key1 == prevkey2:
             fd.write(line)
             cntdup2 += 1
          prevkey2 = key1

#
       line = fp.readline()
       cnt += 1
       if cntout2 >= 100000:
          break
fp.close()
fo.close()
fd.close()
cntout = cntout2+cntout3+cntout4
print('cnt=', cnt, ',cntout=', cntout)
print('cntout2=', cntout2, ',cnterr2=', cnterr2, ' cntdup2=', cntdup2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
