﻿import codecs
import os
# extract/ shift twchi.txt for ph2 only
filepath= 'twchi_10000_ph234.txt'  
fileout = 'twchi_10000_ph2freq.txt'  

if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
lineout = '999999 功夫' 
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
       if line[17]=='(':
          cntout2 += 1 
          wordlist=line.split() 
##          lineout = str(cntout2).zfill(6) + ' ' + line[15:17] 
          lineout = str(int(wordlist[2])).zfill(6) + ' ' + line[15:17] 
          fo.write(lineout+'\n')
           
       line = fp.readline()
       cnt += 1
fp.close()
fo.close()
cntout = cntout2+cntout3+cntout4
print('cnt=', cnt, ',cntout=', cntout)
print('cntout2=', cntout2, ',cnterr2=', cnterr2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
