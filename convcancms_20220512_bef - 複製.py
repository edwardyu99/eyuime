﻿import codecs
import os
### convcanph2345cms.py - c+merge+shift --> reneeyu_canph2345ori.txt 
### convcanph2345c.py - conv canph2345ori using yus_candict_c.txt
filepath = 'reneeyu_canph2345ori.txt' 
fileout  = 'reneeyu_canph2345out.txt'
filedup  = 'reneeyu_canph2345outdup.txt'
filefilter = 'reneeyu_canph2345outfilter.txt'
##keypath  = 'reneeyu_canph2key.txt'
keypath  = 'yus_candict_c.txt'
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
          print('**line no.=', cnt)
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
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(key3)
             print(val3)
             print(key4)
             print(val4)
             print(line)
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
#---------------------------------------------------------------------
import codecs
import os
### convcanph2345freqmerge.py -- add mergedict freq
filepath = 'reneeyu_canph2345out.txt'  
fileout  = 'reneeyu_canph2345out_freqmerge.txt'
file999999  = 'reneeyu_canph2345out_999999merge.txt'
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
##        if int(val1)+dup999999cnt >= 999901: 
          if val1[0:4]=='9999':
             lineout9 = str(int(val1)+dup999999cnt) + ' ' +line[7:]
             f9.write(lineout9)
             cnterr2 += 1

          if cntout2 == 0:
             print('**converting canph2...') 
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
             print('**converting canph3...')
          cntout3 += 1
#
# 7key + 4(utf-16)char + lf = 12
       
       if len(line) >= 12:
          key1 = line[7:9]
          val1 = mergedict.get(key1, '888888') 
          if val1 != '888888':
             val1 = str(int(val1)+400000).zfill(6)
          lineout = '0'+str(len(line)-12+4) + line[0:6]+ val1 + line[7:]
          fo.write(lineout)
          if cntout4 == 0:
             print('**converting canph4,5,6,7...')
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
# sort fo examples
#linux: sort shopping.txt -o shopping.txt 
#shopping = open('shopping.txt')
#lines = shopping.readlines()
#lines.sort()
#shopping.close()
#
#lines = sorted(shopping.readlines())
'''
fn = fileout # 'filename.txt'
sorted_fn = 'sorted_filename.txt'

with open(fn,'r') as first_file:
    rows = first_file.readlines()
    sorted_rows = sorted(rows) #, key=lambda x: int(x.split()[0]), reverse=False)
    with open(sorted_fn,'w') as second_file:
        for row in sorted_rows:
            second_file.write(row)
'''
with open(fileout, 'r+',encoding="utf-16") as f:
    sorted_contents=''.join(sorted(f.readlines())) #, key = lambda x: int(x.split(' ')[0])))
    f.seek(0)
    f.truncate()
    f.write(sorted_contents)
print(fileout,' sorted OK')
#------------------------------------------------------------------------------------
import codecs
import os
# convshiftcanph2345freqmerge.py
# remove left 2 columns and middle 6 columns freq after sort by ultraedit

filepath = 'reneeyu_canph2345out_freqmerge.txt'  
fileout  = 'reneeyu_canph2345ori.txt'
fileout9 = 'reneeyu_canph2345ori9.txt'  # 9999 only
fileouts = 'reneeyu_canph2345oris.txt'  # subtract 9999
if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 

if os.path.exists(fileout9):
    os.remove(fileout9)
f9 = open(fileout9,'a+', encoding='utf-16') 

if os.path.exists(fileouts):
    os.remove(fileouts)
fs = open(fileouts,'a+', encoding='utf-16') 
#linein = '02kungfu9999999功夫' 
lineout = 'kungfu 功夫' 
with open(filepath,'r', encoding='utf-16') as fp:  
   line = fp.readline()
   cnt = 0
   cntout = 0
   cntout2 = 0
   cntout9 = 0
   cntouts = 0
   cntout3 = 0
   cntout4 = 0 
   cnterr2 = 0
   cnterr3 = 0
   cnterr4 = 0 
   prevkey = '      '
   prevline = ' '
   while line:
       lineout = line[2:8] + ' ' + line[14:] 
       if line != prevline:
          fo.write(lineout)
          cntout2 += 1  
       # 
       if line[0:2] == '02' and line[8:12]=='9999' and line[2:8] == prevkey:
       	  f9.write(lineout)
       	  cntout9 += 1
       else:
       	  fs.write(lineout)
       	  cntouts += 1
       #
       prevline = line
       prevkey = line[2:8]
       line = fp.readline()
       cnt += 1
fp.close()
fo.close()
f9.close()
fs.close()
cntout = cntout2+cntout3+cntout4
print('cnt=', cnt, ',cntout=', cntout)
print('cntout2=', cntout2, ',cnterr2=', cnterr2)
#print('cntout3=', cntout3, ',cnterr3=', cnterr3)
#print('cntout4=', cntout4, ',cnterr4=', cnterr4)
print('cntout9=', cntout9)
print('cntouts=', cntouts)
print(filepath,' shifted to ', fileout, ' OK')
#------------------------------------------------------
# check oris dup cnt
print('*** check cntdup2 of oris.txt')
filepath = 'reneeyu_canph2345oris.txt' 
fileout  = 'reneeyu_canph2345outs.txt'
filedup  = 'reneeyu_canph2345outdups.txt'
filefilter = 'reneeyu_canph2345outfilters.txt'
##keypath  = 'reneeyu_canph2key.txt'
keypath  = 'yus_candict_c.txt'
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
             #print(key1)
             #print(val1)
             #print(key2)
             #print(val2)
             #print(key3)
             #print(val3)
             #print(key4)
             #print(val4)
             #print(line)
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
#---------------------------------------------------------------------