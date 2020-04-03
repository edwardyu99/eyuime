import codecs
import os
filepath = 'yus_canchar_dict.txt'  
fileout  = 'yus_canchar_dict_freqyus.txt'
keypathcan  = 'reneeyu_canph2key.txt'
## yus_chardcit701 e.g. 'aa     間'
keypathyus  = 'yus_chardict701.txt'
keypathcuhk  = 'can_faq_sorted7000.txt'

dictcnt = 0
#-----------------------------

candict = {}
yusdict= {}
cuhkdict = {}

with codecs.open(keypathyus,'r','utf-16') as f:
    for line in f:
        if len(line) != 10:
          print(len(line))
          print(line)

        c0 = line[0]
        c1 = line[1]
        c01= line[0:2]
        if (c0=='c' or c0=='q' or c0=='r' or c0=='v' or c0=='x' or c0=='z' or \
           c0=='e') and c1!=' ': 
           continue
## extract single abcde 
## extract start or end with aeiou '?a' '?e' '?i' '?o' '?u' 
        if c1 != ' ' and c01 !='ah' and c01 !='ai' and c01 !='ak' and \
           c01 !='ap' and c01 !='au' and c01 !='oh' and c01 !='on' and \
           c01 !='in' and c01 !='uk' and \
           c1 !='a' and c1 !='e' and c1 !='i' and c1 !='o' and c1 !='u':
           continue        
           
        key = line[7]
        val = str(dictcnt+1).zfill(4)

# prevent duplicate key dict
        valdict = cuhkdict.get(key,'????')
        if valdict == '????':
           print('line from yusdict: ',line)
           cuhkdict[key] = val
           valyus = line[0:2]
           yusdict[key]= valyus
           dictcnt += 1

f.close()
#---------------------
prevcan6 = '      '
with codecs.open(keypathcan,'r','utf-16') as f:
    for line in f:
        if len(line) != 10:
          print(len(line))
          print(line)
##ignore 'z'
        if line[2]=='z':
           continue
##ignore aeiou already in yusdict
        key = line[7]
        valdict = yusdict.get(key,'??')
        if valdict == '??':
           continue
      
##ignore dup key
        if line[0:6] == prevcan6:
           continue
        else:
           prevcan6 = line[0:6]
## first break line always in dict
           key = line[7]
           valcnt = str(dictcnt+1).zfill(4) 
           val = line[0:6]+ ' ' + valcnt
           candict[key] = val
           cuhkdict[key] = valcnt
           dictcnt += 1
           continue

        key = line[7]
        valcnt = str(dictcnt+1).zfill(4) 
        val = line[0:6]+ ' ' + valcnt
        
# prevent duplicate key dict
# candict now can be used to check dup canchar 
# also the first candict freq will be put in front in cuhkdict
        valdict = candict.get(key,'??????')
        if valdict == '??????':
           candict[key] = val
           cuhkdict[key] = valcnt
           dictcnt += 1
f.close()
candictcnt = dictcnt

with codecs.open(keypathyus,'r','utf-16') as f:
    for line in f:
        if len(line) != 10:
          print(len(line))
          print(line)
        
        key = line[7]
        val = str(dictcnt+1).zfill(4)
##        print(key)
##        print(val) 
#        if len(val) != 4:
#           print(len)
#           print(val) 
# prevent duplicate key dict
        valdict = cuhkdict.get(key,'????')
        if valdict == '????':
##           print('line from yusdict: ',line)
           cuhkdict[key] = val
           valyus = line[0:2]
           yusdict[key]= valyus
           dictcnt += 1
##        else:
##           print('dup dict key ')
##           print(line)
##           print(line[99])
f.close()
yusdictcnt = dictcnt - candictcnt

with codecs.open(keypathcuhk,'r','utf-16') as f:
    for line in f:
        if len(line) != 17:
          print(len(line))
          print(line)

        key = line[12]
        val = line[1:5]
##        print(key)
##        print(val) 
#        if len(val) != 4:
#           print(len)
#           print(val) 
# prevent duplicate key dict
        valdict = cuhkdict.get(key,'????')
        if valdict == '????':
## cuhkdict val starts after yus_chardict701
           val = str(dictcnt+1).zfill(4)
           cuhkdict[key] = val
           dictcnt += 1
f.close()
cuhkdictcnt = dictcnt - candictcnt - yusdictcnt

#-----------------------------
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
       val1 = cuhkdict.get(key1, '9999')
##       valyus = yusdict.get(key1, '??') 
##       valcan = candict.get(key1, '??????')   
##       if line[2] !='z' and valcan != '???????' and line[0:6].rstrip() != valcan.rstrip():
##          print(line)
##          cnterr1 += 1 
       lineout = line[0:6] + val1 + ' ' + key1
       fo.write(lineout+'\n')
#       fo.write(lineout)
       cntout1 += 1

       line = fp.readline()
       cnt += 1
fp.close()
fo.close()
print('candict cnt=',candictcnt)
print('yusdict cnt=',yusdictcnt)
print('cuhkdict cnt=',cuhkdictcnt)

cntout = cntout1+cntout2+cntout3+cntout4
print('cnt=', cnt, ',cntout=', cntout)
print('cntout1=', cntout1, ',cnterr1=', cnterr1)
print('cntout2=', cntout2, ',cnterr2=', cnterr2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
