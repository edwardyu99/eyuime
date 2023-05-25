import codecs
import os
filepath = 'reneeyu_canph234ori.txt'  
fileout  = 'reneeyu_canph234freq.txt'
keypath  = 'reneeyu_canph2keyfreq.txt'
# keypath  = 'reneeyu_ph123key_oriquick.txt'
# keypath12  = 'reneeyu_ph123key2.txt'
# ---------------
# mydict12 = {}
# with codecs.open(keypath12,'r','utf-16') as f:
#    for line in f:
#       key = line[5]
#       val = line[0:2].rstrip()
#       print(key+val)
#       mydict12[key] = val
# f.close()

mydict = {}
with codecs.open(keypath,'r','utf-16') as f:
    for line in f:
        if len(line) != 14:
          print(len(line))
          print(line)
          print(line[0])
          print(line[1])
          print(line[2])
          print(line[3])
          print(line[4])
          print(line[5])
          print(line[6])
          print(line[7])
          print(line[8])
          print(line[9])
          print(line[10])
          print(line[11])
          print(line[12])
#          print(line[13]) #endline
#          print(line[9]) #endline
        key = line[11]
        val = line[0:8].rstrip()
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

if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
lineout = '99998888kungfu 功夫' 
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
#       print("Line {}: {}".format(cnt, line.strip()))
#       if len(line) != 8:
#          print(len(line)) 
#       if len(line) == 6:
#          key1 = line[3]
#          key2 = line[4]
#          print(key1+key2)
#       else:
#          if len(line) == 7:
#             key1 = line[4]
#             key2 = line[5]
#             print(key1+key2)
#          else:
#             key1 = line[5]
#             key2 = line[6] 
#       print(len(line))
#       print(line)
       if len(line) > 12 or len(line) < 10:
#         print(line[0])
#         print(line[1])
#         print(line[2])
#         print(line[3])
#         print(line[4])
#         print(line[5])
#         print(line[6])
#         print(line[15]) #endline
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
          val1 = mydict.get(key1, '9999xxxx')      
          val2 = mydict.get(key2, '8888xxxx')
          if val1 == '9999xxxx' or val2 == '8888xxxx':
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(line)
             cnterr2 += 1
#          val = val1.rstrip() + val2
          val = str(10999-int(val1[0:4])) +str(10999-int(val2[0:4]))
          val=val+(val1[4:].rstrip()) + (val2[4:].rstrip()) 
          if len(val) > 14:
             val = val[0:14] 
          if len(val) == 13:
             val = val + ' '
          if len(val) == 12:
             val = val + '  '
          lineout = val + ' ' +key1+key2
          fo.write(lineout+'\n')
          if cntout2 == 0:
             print('**convering canph2...')
          cntout2 += 1
#
# 7key + 3(utf-16)char + lf = 11
       
       if len(line) == 11:
          key1 = line[7]
          key2 = line[8]
          key3 = line[9]
#       print(key1)
          val1 = mydict.get(key1, '9999xxxx')      
          val2 = mydict.get(key2, '8888xxxx')
          val3 = mydict.get(key3, '7777xxxx')
          if val1 == '9999xxxx' or val2 == '8888xxxx' or val3 == '7777xxxx':
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(key3)
             print(val3)
             print(line)
             cnterr3 += 1
          val = '9998'+str(10999-int(val1[0:4])) 
          val=val+(val1[4:].rstrip()) +val2[4]+val3[4] 
          if len(val) > 14:
             val = val[0:14] 
          if len(val) == 13:
             val = val + ' '
          if len(val) == 12:
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
          val1 = mydict.get(key1, '9999xxxx')      
          val2 = mydict.get(key2, '8888xxxx')
          val3 = mydict.get(key3, '7777xxxx')
          val4 = mydict.get(key4, '6666xxxx')
          if val1=='9999xxxx' or val2=='8888xxxx' or val3=='7777xxxx' or val4=='6666xxxx':
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
          val = '9999' + str(10999-int(val1[0:4]))
          val=val+(val1[4:].rstrip()) +val2[4]+val3[4]+val4[4] 
          if len(val) > 14:
             val = val[0:14] 
          if len(val) == 13:
             val = val + ' '
          if len(val) == 12:
             val = val + '  '
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
cntout = cntout2+cntout3+cntout4
print('cnt=', cnt, ',cntout=', cntout)
print('cntout2=', cntout2, ',cnterr2=', cnterr2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
