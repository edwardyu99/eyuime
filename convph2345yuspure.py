import codecs
import os
print('**convph2345yuspure.py - conv from canori to phout using yus_quickdict_purequick')
### use canph2345 as ori.txt to gen quick ph2,3,4,5..7
filepath = 'reneeyu_canph2345ori.txt'  
###filepath = 'reneeyu_ph2345ori.txt'  
fileout  = 'reneeyu_ph2345out.txt'
filedup  = 'reneeyu_ph2345outdup.txt'
# keypath  = 'reneeyu_ph2key.txt'
##keypath12  = 'reneeyu_ph123key2.txt'
##keyyus    = 'yus_chardict.txt' 
##keyquick  = 'reneeyu_ph123key_oriquick.txt'
##keyyus    = 'yus_quickdict.txt' 
keyyus    = 'yus_quickdict_purequick.txt' 

mydict = {}
##with codecs.open(keypath12,'r','utf-16') as f:
##    for line in f:
##       key = line[5]
##       val = line[0:2].rstrip()

# prevent duplicate key dict
##       valdict = mydict.get(key,'??')
##       if valdict == '??':
##           mydict[key] = val
##f.close()

with codecs.open(keyyus,'r','utf-16') as f:
    for line in f:
       key = line[7]
       if line[2]== ' ':
          val = line[0:2].rstrip()
       else:
          val = line[0] + line[2]
#       print(key+val)
# prevent duplicate key dict
       valdict = mydict.get(key,'??')
       if valdict == '??':
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
   cntout5 = 0
   cntout6 = 0
   cntout7 = 0
   cnterr2 = 0
   cnterr3 = 0
   cnterr4 = 0 
   cnterr5 = 0
   cnterr6 = 0 
   cnterr7 = 0
   cntdup2 = 0
   prevkey2 = '    '
   while line:

       if len(line) > 15 or len(line) < 10:
          print(len(line))
          print(line)
          print('**len < 10 or > 15, 7key + 7(utf-16)char + 1endline')
#          abort by index 
#          print(line[99])
#        
# 7key + 2(utf-16)char + lf = 10
       
       if len(line) == 10:
          key1 = line[7]
          key2 = line[8]
#       print(key1)
          val1 = mydict.get(key1, 'xx')      
          val2 = mydict.get(key2, 'xx')
          if key1 != 'Ｘ' and (val1 == 'xx' or val2 == 'xx'):
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(line)
             cnterr2 += 1
          val = val1.rstrip() + val2.rstrip() 
          if len(val) < 2 or len(val) > 4:
             print('**lenval not 2,3,4')
#          abort by index 
             print(line[99])
          if len(val) == 3:
             val = val + ' '         
#             print(line)
          if len(val) == 2:
             val = val + 'z '  
          lineout = val + '   ' +key1+key2
#          fo.write(lineout+'\r\n')
          fo.write(lineout+'\n')
          if cntout2 == 0:
             print('**converting ph2...')
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
          val1 = mydict.get(key1, 'xx')      
          val2 = mydict.get(key2, 'xx')
          val3 = mydict.get(key3, 'xx')
          if val1 == 'xx' or val2 == 'xx' or val3 == 'xx':
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(key3)
             print(val3)
             print(line)
             cnterr3 += 1
          val = val1.rstrip() + val2[0] + val3[0] 
# 
          if len(val1.rstrip()) == 1:
             val = val1.rstrip() + val2[0] + val3 
          if len(val) < 3 or len(val) > 4:
             print('**lenval not 3,4')
#          abort by index 
             print(line[99])
          if len(val) == 3:
             val = val + ' '                   
          lineout = val + '   ' +key1+key2+key3
#          fo.write(lineout+'\r\n')
          fo.write(lineout+'\n')
          if cntout3 == 0:
             print('**converting ph3...')         
          cntout3 += 1
#
# 7key + 4(utf-16)char + lf = 12
       
       if len(line) == 12:
          key1 = line[7]
          key2 = line[8]
          key3 = line[9]
          key4 = line[10]
#       print(key1)
          val1 = mydict.get(key1, 'xx')      
          val2 = mydict.get(key2, 'xx')
          val3 = mydict.get(key3, 'xx')
          val4 = mydict.get(key4, 'xx')
          if val1=='xx' or val2=='xx' or val3=='xx' or val4=='xx':
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
          if len(val) < 4 or len(val) > 5:
             print('**lenval not 4,5')
#          abort by index 
             print(line[99])
          if len(val) == 4:
             val = val + ' '         
          lineout = val + '  ' +key1+key2+key3+key4
#          fo.write(lineout+'\r\n')
          fo.write(lineout+'\n')
          if cntout4 == 0:
             print('**converting ph4...')
          cntout4 += 1
#------------------
       if len(line) < 13:
          line = fp.readline()
          cnt += 1
          continue
# remaining lines are 5 or more chars phrases         
#          
# 7key + 5(utf-16)char + lf = 13
       
       if len(line) == 13:
          key1 = line[7]
          key2 = line[8]
          key3 = line[9]
          key4 = line[10]
          key5 = line[11]
#       print(key1)
          val1 = mydict.get(key1, 'xx')      
          val2 = mydict.get(key2, 'xx')
          val3 = mydict.get(key3, 'xx')
          val4 = mydict.get(key4, 'xx')
          val5 = mydict.get(key5, 'xx')
          if val1=='xx' or val2=='xx' or val3=='xx' or val4=='xx' or val5=='xx':
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
          if len(val) < 5 or len(val) > 6:
             print('**lenval not 5,6')
#          abort by index 
             print(line[99])
          if len(val) == 5:
             val = val + ' '         
#          lineout = val + ' ' +key1+key2+key3+key4+key5
          lineout = val + ' ' +line[7:]
#          fo.write(lineout+'\n')
          fo.write(lineout)
          if cntout5 == 0:
             print('**converting ph5...')
##          if len(line)==13:
          cntout5 += 1
          

#------------------
# 7key + 6,7(utf-16)char + lf = 14,15
       
       if len(line) >= 14:
          key1 = line[7]
          key2 = line[8]
          key3 = line[9]
          key4 = line[10]
          key5 = line[11]
          key6 = line[12]
#       print(key1)
          val1 = mydict.get(key1, 'xx')      
          val2 = mydict.get(key2, 'xx')
          val3 = mydict.get(key3, 'xx')
          val4 = mydict.get(key4, 'xx')
          val5 = mydict.get(key5, 'xx')
          val6 = mydict.get(key6, 'xx')
          if val1=='xx' or val2=='xx' or val3=='xx' or val4=='xx' or val5=='xx' or val6=='xx':
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
             print(key6)
             print(val6)
             print(line)
             cnterr6 += 1
          val = val1.rstrip() +val2[0] +val3[0] +val4[0] +val5[0] +val6[0]
          val = val[0:6]
          if len(val) < 5 or len(val) > 6:
             print('**lenval not 5,6')
#          abort by index 
             print(line[99])
          if len(val) == 5:
             val = val + ' '         
#          lineout = val + ' ' +key1+key2+key3+key4+key5
          lineout = val + ' ' +line[7:]
#          fo.write(lineout+'\n')
          fo.write(lineout)
          if cntout6 == 0:
             print('**converting ph6,7...')
          if len(line)==14:
             cntout6 += 1
          if len(line)==15:
             cntout7 += 1

#------------------
       line = fp.readline()
       cnt += 1
fp.close()
fo.close()
fd.close()
cntout = cntout2+cntout3+cntout4+cntout5+cntout6+cntout7
print('cnt=', cnt, ',cntout=', cntout)
print('cntout2=', cntout2, ',cnterr2=', cnterr2, ' cntdup2=', cntdup2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
print('cntout5=', cntout5, ',cnterr5=', cnterr5)
print('cntout6=', cntout6, ',cnterr6=', cnterr6)
print('cntout7=', cntout7, ',cnterr7=', cnterr7)

# ----- 
