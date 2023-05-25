import codecs
import os
filepath = 'reneeyu_canph2345ori_20180616.txt'  
###filepath = 'canph2_from_jieba_merge.txt'  
fileout  = 'reneeyu_canph2345ori_freqjieba.txt'
file999999  = 'reneeyu_canph2345ori_999999jieba.txt'
filemergejieba   = 'merge_jieba.txt'
filejiebaextra = 'jieba_extra_twchi.txt'  
filebaidufixfreq='baidu_fixfreq.txt'
###keypathtwchi  = 'twchi_10000_ph234.txt'
keypathtwchi  = 'twchi_10000_ph2freq.txt'
###keypathjieba  = 'jieba_traddict.txt'
keypathjieba  = 'jieba_134000_ph2freq.txt'
keypathbaidu  = 'baiduchifu_ph2.txt'
keypathchiss  = 'chisiusuet_500000_ph2.txt'
if os.path.exists(filemergejieba):
    os.remove(filemergejieba)
fm = open(filemergejieba,'a+', encoding='utf-16') 
if os.path.exists(filejiebaextra):
    os.remove(filejiebaextra)
fje = open(filejiebaextra,'a+', encoding='utf-16') 
if os.path.exists(filebaidufixfreq):
    os.remove(filebaidufixfreq)
fbf = open(filebaidufixfreq,'a+', encoding='utf-16') 
cntbaidu = 0
cntbaiduextra = 0
mergecnt = 0
#-----------------------------
dictline = '018148 我們'
dictcnt = 0
mydictchiss = {}
with codecs.open(keypathtwchi,'r','utf-16') as f:
    for line in f:
       key = line[7:9]
       valdict = mydictchiss.get(key,'??????')
# prevent duplicate key dict
       if valdict == '??????':
          dictcnt += 1
##          val = str(dictcnt).zfill(6)
          val = str(18149 - int(line[1:6])).zfill(6)
          mydictchiss[key] = val
          lineout=val+' '+key
          fm.write(lineout+'\n')
          mergecnt += 1
f.close()
print('after twchi, merge dict cnt=',mergecnt)
#-------------

dictline = '083048 表示'
##dictcnt = 0 ## jieba dictcnt continued after chiss
with codecs.open(keypathjieba,'r','utf-16') as f:
    for line in f:
       key = line[7:9]
       valdict = mydictchiss.get(key,'??????')
# prevent duplicate key dict
       if valdict == '??????':
          dictcnt += 1
###          val = str(dictcnt).zfill(6)
# use prev twchi freq+100 as val
          
#          val = str(18149 - int(line[1:6])).zfill(6)
          val = str(int(prevtwchifreq) + 100).zfill(6)
          mydictchiss[key] = val
          lineout=val+' '+key
          fm.write(lineout+'\n')
          mergecnt += 1
          fje.write(lineout+'\n')
       else:
          prevtwchifreq = valdict
f.close()
print('after jieba, merge dict cnt=',mergecnt)
#-------------
## output baidu dict, freq=twichi+10 or jieba 
dictline = '4 公共'
dictcnt = 0 ## baidu dictcnt starts after jieba
##mydictbaidu = {}
with codecs.open(keypathbaidu,'r','utf-16') as f:
    for line in f:
       key = line[2:4]
       valdict = mydictchiss.get(key,'??????')
# prevent duplicate key dict
       if valdict == '??????':
          dictcnt += 1
###          val = str(dictcnt).zfill(6)
###          val = str(200000+dictcnt).zfill(6)
# use prev twchi freq+50 as val
          val = str(int(prevtwchifreq) + 10).zfill(6)

          mydictchiss[key] = val
          lineout=val+' '+key
          fm.write(lineout+'\n')
          mergecnt += 1
          fbf.write(lineout+'\n')
          cntbaidu += 1 
          cntbaiduextra += 1
       else:
          prevtwchifreq = valdict
          lineout=valdict+' '+key
          fbf.write(lineout+'\n')
          cntbaidu += 1 
          
f.close()
print('after baidu, merge dict cnt=',mergecnt)
#-----------------------------

dictline = '000001 一個 999999'
##dictcnt = 0
##mydictchiss = {}
with codecs.open(keypathchiss,'r','utf-16') as f:
    for line in f:
       key = line[7:9]
       valdict = mydictchiss.get(key,'??????')
# prevent duplicate key dict
       if valdict == '??????':
          dictcnt += 1
          val = str(dictcnt).zfill(6)
          mydictchiss[key] = val
## enough after mergecnt >= 150000
          if mergecnt < 150000:
             lineout=val+' '+key
             fm.write(lineout+'\n')
             mergecnt += 1
f.close()
fm.close()
print('after chisiusuet, merge dict cnt=',mergecnt)
# ---------------

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
          val1 = mydictchiss.get(key1, '999900') 
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
##          if int(val1)+dup999999cnt >= 999901: 
          if val1[0:4]=='9999':
             f9.write(lineout)
             cnterr2 += 1

          if cntout2 == 0:
             print('**converting canph2...') 
          cntout2 += 1           
#
# 7key + 3(utf-16)char + lf = 11
       
       if len(line) == 11:
          key1 = line[7:9]
          val1 = mydictchiss.get(key1, '888888') 
          lineout = '03' + line[0:6]+ val1 + line[7:]
          fo.write(lineout)
          if cntout3 == 0:
             print('**converting canph3...')
          cntout3 += 1
#
# 7key + 4(utf-16)char + lf = 12
       
       if len(line) >= 12:
          key1 = line[7:9]
          val1 = mydictchiss.get(key1, '888888') 
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
fm.close()
fje.close()
fbf.close()
print('cntbaidu=', cntbaidu, ',cntbaiduextra=',cntbaiduextra)
cntout = cntout2+cntout3+cntout4
print('cnt=', cnt, ',cntout=', cntout)
print('cntout2=', cntout2, ',cnterr2=', cnterr2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
