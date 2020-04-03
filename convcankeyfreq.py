import codecs
import os
filepath = 'reneeyu_canph2key.txt'  
fileout  = 'reneeyu_canph2keyfreq_aftcdup.txt'
keypath  = 'reneeyu_canph2keyfreq_befcdup.txt'

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
        val = line[0:4].rstrip()
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
lineout = 'kungfu9999 功夫' 
with open(filepath,'r', encoding='utf-16') as fp:  
   line = fp.readline()
   cnt = 0
   cntout = 0
   cntout1 = 0
   cntout2 = 0 
   cntout3 = 0
   cntout4 = 0 
   cnterr1 = 0
   cnterr2 = 0
   cnterr3 = 0
   cnterr4 = 0 
   while line:
#       print(len(line))
#       print(line)
# ignore blank lines and first 2 lines /S Aa b c ...
       if line[0] == ' ' or line[0] == '/':
          cnterr1 += 1
          line = fp.readline()
          cnt += 1
          continue   
       key1 = line[7]
       val1 = mydict.get(key1, '9999') 
       lineout = line[0:6] + str(10999-int(val1)) + ' ' + key1
       fo.write(lineout+'\n')
#       fo.write(lineout)
       cntout1 += 1

       line = fp.readline()
       cnt += 1
fp.close()
fo.close()
cntout = cntout1+cntout2+cntout3+cntout4
print('cnt=', cnt, ',cntout=', cntout)
print('cntout1=', cntout1, ',cnterr1=', cnterr1)
print('cntout2=', cntout2, ',cnterr2=', cnterr2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
