import codecs
import os
filepath = 'fix6_txt_ori.txt'  
fileout  = 'fix6_txt_aftfix6.txt'

if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
lineout = 'kungfu 功夫' 
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
       wordlist = line.split()
#       print(wordlist[0])
       if len(wordlist) <= 1:
          print(len(line))
          print(line)
## ignore spc line
       cntout1 += 1
       if wordlist[0] == 'spc':
          fo.write(line)
       else: 
          lineout = wordlist[0].ljust(6) + ' ' + wordlist[1]  
          fo.write(lineout+'\n')
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
