import codecs
import os
# c=ch, s=sh, e=ei, ue=u 
filepath = 'reneeyu_canph2key.txt'  
fileout  = 'reneeyu_canph2key_short.txt'
if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
#linein = 'cheung 長' 
lineout = 'ceung  長' 
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
       lineout = line 
## keep cha che chi cho chu
##       if line[0:2] == 'ch' and line[3] != ' ':
## change all ch to c except chan陳 cheung張
       if line[0:2]=='ch' and line[7]!='陳' and line[7]!='張' and \
          line[7]!='周' and line[7]!='蔡' and line[7]!='曹' and line[7]!='趙':
          lineout = 'c' + line[2:7] + ' ' +line[7:]
## keep shun to sep from sun
       if line[0:2] == 'sh' and line[0:5] != 'shun ':
          lineout = 's' + line[2:7] + ' ' +line[7:]
       if line[1:4] == 'ei ':
          lineout = line[0:2] + line[3:7] + ' ' +line[7:] 
## only ju=jue
       if line[1:4] == 'ue ':
          lineout = line[0:2] + line[3:7] + ' ' +line[7:] 
       
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
