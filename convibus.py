import codecs
import os
filepath = 'reneeyu.txt'  
fileout  = 'reneeyu_ibusout.txt'

if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
lineout = 'kungfu>功夫>1' 
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
 
       wordlist = line.split()
#       print(wordlist[0])
# handled spc whitespace line
       if wordlist[0] == 'spc':
          lineout = 'spc\t' + '　' + '\t1'
       else:
#          print(wordlist[1]) 
          lineout = wordlist[0] + '\t' + wordlist[1] + '\t' + str(500000-cntout1)
       fo.write(lineout+'\n')
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
