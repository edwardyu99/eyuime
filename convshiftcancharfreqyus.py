﻿import codecs
import os
# remove middle 4 columns freq after sort by ultraedit
filepath = 'yus_canchar_dict_freqyus.txt'  
fileout = 'yus_canchar_dict_aftshift.txt'  

if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
#linein = 'kungfu9999 功夫' 
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
   while line:
       lineout = line[0:6] + line[10:] 
       fo.write(lineout)
       cntout2 += 1  
       line = fp.readline()
       cnt += 1
fp.close()
fo.close()
cntout = cntout2+cntout3+cntout4
print('cnt=', cnt, ',cntout=', cntout)
print('cntout2=', cntout2, ',cnterr2=', cnterr2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
