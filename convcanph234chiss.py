import codecs
import os
filepath = 'reneeyu_canph234ori.txt'  
fileout  = 'reneeyu_canph234chissout.txt'
filedup  = 'reneeyu_canph234chissdup.txt'
keypath  = 'reneeyu_canph2key.txt'
keypathchiss  = 'chisiusuet_500000_ph2.txt'
# ---------------
mydictchiss = {}
with codecs.open(keypathchiss,'r','utf-16') as f:
    for line in f:
       key = line[7:9]
       val = line[0:6]
#       print(key+val)
       mydictchiss[key] = val
f.close()

mydict = {}
with codecs.open(keypath,'r','utf-16') as f:
    for line in f:
        if len(line) != 10:
          print(len(line))
          print(line)
        key = line[7]
        val = line[0]+line[1]+line[2]+line[3]
#        print(key)
#        print(val) 
#        if len(val) != 4:
#           print(len)
#           print(val) 
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
lineout = 'kungfu 功夫' 
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
   prevkey2 = '    '
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
          key1 = line[7]
          key2 = line[8]
#       print(key1)
          val1 = mydict.get(key1, 'xxxx')      
          val2 = mydict.get(key2, 'xxxx')
          if val1 == 'xxxx' or val2 == 'xxxx':    
#             print(key1)
#             print(val1)
#             print(key2)
#             print(val2)
#             print(line)
             cnterr2 += 1
            
## ignore ph2 not found in mydict
             line = fp.readline()
             cnt += 1
             continue
## ignore ph2 not found in mydictchiss, out dup
          keychiss = key1 + key2
          valchiss = mydictchiss.get(keychiss,'000000')
          if valchiss == '000000':
             fd.write(line)
             cntdup2 += 1

             line = fp.readline()
             cnt += 1
             continue

          val = val1.rstrip() + val2
          if len(val) > 6:
             val = val[0]+val[1]+val[2]+val[3]+val[4]+val[5]
#          print(val)
          lineout = val + ' ' +key1+key2
          fo.write(lineout+'\n')
          if cntout2 == 0:
             print('**convering canph2...')
          cntout2 += 1
# output dupkey2 to fd
#          if val == prevkey2:
#             fd.write(line)
#             cntdup2 += 1
#          prevkey2 = val
#
# 7key + 3(utf-16)char + lf = 11
       
       if len(line) == 11:
          key1 = line[7]
          key2 = line[8]
          key3 = line[9]
#       print(key1)
          val1 = mydict.get(key1, 'xxxx')      
          val2 = mydict.get(key2, 'xxxx')
          val3 = mydict.get(key3, 'xxxx')
          if val1 == 'xxxx' or val2 == 'xxxx' or val3 == 'xxxx':
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(key3)
             print(val3)
             print(line)
             cnterr3 += 1
          val = val1.rstrip() + val2[0] + val3[0]
          
          if len(val) > 6 or len(val) < 4:
             print('**lenval not 4,5,6')
             print(len(val))
             print(val)
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(key3)
             print(val3)
             print(line)
# abort by index
             print(line[99])
          if len(val) == 5:
             val = val + ' '
          if len(val) == 4:
             val = val + '  '
          lineout = val + ' ' +key1+key2+key3
          fo.write(lineout+'\n')
          if cntout3 == 0:
             print('**convering canph3...')         
          cntout3 += 1
#
# 7key + 4(utf-16)char + lf = 12
       
       if len(line) == 12:
          key1 = line[7]
          key2 = line[8]
          key3 = line[9]
          key4 = line[10]
#       print(key1)
          val1 = mydict.get(key1, 'xxxx')      
          val2 = mydict.get(key2, 'xxxx')
          val3 = mydict.get(key3, 'xxxx')
          val4 = mydict.get(key4, 'xxxx')
          if val1=='xxxx' or val2=='xxxx' or val3=='xxxx' or val4=='xxxx':
#             print(key1)
#             print(val1)
#             print(key2)
#             print(val2)
#             print(key3)
#             print(val3)
#             print(key4)
#             print(val4)
#             print(line)
             cnterr4 += 1
          val = val1.rstrip() + val2[0] + val3[0] + val4[0]
          if len(val) > 7 or len(val) < 5:
             print('**lenval not 5,6,7')
             print(len(val))
             print(val)
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(key3)
             print(val3)
             print(line)
# abort by index
             print(line[99])
          if len(val) == 7:
             val = val[0]+val[1]+val[2]+val[3]+val[4]+val[5]
          if len(val) == 5:
             val = val + ' '

          lineout = val + ' ' +key1+key2+key3+key4
          fo.write(lineout+'\n')
          if cntout4 == 0:
             print('**convering canph4...')
          cntout4 += 1
#
       line = fp.readline()
       cnt += 1
fp.close()
fo.close()
fd.close()
cntout = cntout2+cntout3+cntout4
print('cnt=', cnt, ',cntout=', cntout)
print('cntout2=', cntout2, ',cnterr2=', cnterr2, ' cntdup2=', cntdup2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
