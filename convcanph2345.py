import codecs
import os
### convcanph2345.py - conv canph2345ori using yus_candict.txt
filepath = 'reneeyu_canph2345ori.txt' 
fileout  = 'reneeyu_canph2345out.txt'
filedup  = 'reneeyu_canph2345outdup.txt'
filefilter = 'reneeyu_canph2345outfilter.txt'
##keypath  = 'reneeyu_canph2key.txt'
keypath  = 'yus_candict.txt'
# ------------------
mydict = {}
with codecs.open(keypath,'r','utf-16') as f:
    for line in f:
        if len(line) != 10:
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
#          print(line[9]) #endline
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

if os.path.exists(filefilter):
    os.remove(filefilter)
ff = open(filefilter,'a+', encoding='utf-16') 
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
   cntout5 = 0 
   cntout6 = 0 
   cntout7 = 0 
   cnterr2 = 0
   cnterr3 = 0
   cnterr4 = 0 
   cnterr5 = 0 
   cntdup2 = 0
   cntfilter=0
   prevkey2 = '    '
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
          key1 = line[7]
          key2 = line[8]
#       print(key1)
          val1 = mydict.get(key1, 'xxxx')      
          val2 = mydict.get(key2, 'xxxx')
          if val1 == 'xxxx' or val2 == 'xxxx':
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(line)
             cnterr2 += 1
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
          if val == prevkey2:
             fd.write(line)
             cntdup2 += 1
          prevkey2 = val
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
#------------------
       if len(line) < 13:
          line = fp.readline()
          cnt += 1
          continue
# remaining lines are 5 or more chars phrases
                  
# 7key + 5(utf-16)char + lf = 13
       
       if len(line) >= 13:
          key1 = line[7]
          key2 = line[8]
          key3 = line[9]
          key4 = line[10]
          key5 = line[11]
#       print(key1)
          val1 = mydict.get(key1, 'xxxx')      
          val2 = mydict.get(key2, 'xxxx')
          val3 = mydict.get(key3, 'xxxx')
          val4 = mydict.get(key4, 'xxxx')
          val5 = mydict.get(key5, 'xxxx')
          if val1=='xxxx' or val2=='xxxx' or val3=='xxxx' or val4=='xxxx' or val5=='xxxx':
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(key3)
             print(val3)
             print(key4)
             print(val4)
             print(key5)
             print(val5)
             print(line)
             cnterr5 += 1
          val = val1.rstrip() + val2[0] + val3[0] + val4[0] + val5[0]
          if len(val) < 6 or len(val) > 8:
             print('**lenval not 6,7,8')
#          abort by index 
             print(line[99])
#max 6chars           
          val = val[0:6]        
##          lineout = val + ' ' +key1+key2+key3+key4+key5
          lineout = val + ' ' + line[7:]
          fo.write(lineout)
#          fo.write(lineout+'\r\n')         
#          fo.write(lineout+'\n')
          if cntout5 == 0:
             print('**converting canph5...')
          if len(line) == 13:
             cntout5 += 1
          else:
             if cntout6 == 0:
                print('**converting canph6,7...')
             if len(line) == 14:
                cntout6 += 1
             else:
                cntout7 += 1

#------------------
       line = fp.readline()
       cnt += 1
fp.close()
fo.close()
fd.close()
ff.close()
cntout = cntout2+cntout3+cntout4+cntout5+cntout6+cntout7
print('cnt=', cnt, ',cntout=', cntout,' ,cntfilter= ',cntfilter)
print('cntout2=', cntout2, ',cnterr2=', cnterr2, ' cntdup2=', cntdup2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
print('cntout5=', cntout5, ',cnterr5=', cnterr5)
print('cntout6=', cntout6)
print('cntout7=', cntout7)
print(filepath,'convert to', fileout, 'OK')
