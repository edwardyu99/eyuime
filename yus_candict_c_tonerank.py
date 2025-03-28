import codecs
import os
print('**yus_candict_c_tonerank.py - add tonerank to yus_candict_c.txt')
filepath = 'yus_candict_c.txt'  
#ang    鶯
fileout  = 'yus_candict_c_tonerankout.txt'
#ang9999鶯
#keyyus    = 'can_faq_sorted7000.txt'
#keyyus    = 'cuhk_charfreq7000utf16.txt'  
#0123456789012345678901234567890
#0001 489803 的   0002 166396 一
keyyus = 'yus_candict_c_rank.txt'
#0123456789012345678901234567890
#dik10001的
mydict = {}

with codecs.open(keyyus,'r','utf-16') as f:
#    line = f.readline() #skip first line with BOM utf-16
    line = f.readline()
    while line: 
       key = line[8:9]  #utf16 char counted as 1
       val = line[3:8]   #tone+rank
       #print(line, 'keyval=', key, val)
       mydict[key] = val
       line = f.readline()
f.close()
dictsize = len(mydict)
#print(mydict) #,dictsize)
print('dictsize=',dictsize)
#--------------------------------
if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
lineout = 'dik10001的' 
with open(filepath,'r', encoding='utf-16') as fp:  
#   line = fp.readline() #skip first line with BOM utf-16
   line = fp.readline()
   cnt = 0
   cntout = 0
   
   while line:      
        key0 = line[0:3]
        key1 = line[7:8] #utf16 char counted as 1
        line8 = line[7:]
        val1 = mydict.get(key1, 'xxxxx')      
        #print(line, 'keyval=', key1, val1)
        if val1 == 'xxxxx':
            dictsize += 1
            val1 = str(10000 + int(dictsize))  
            mydict[key1] = val1  #add new dict item
        lineout = key0 + val1 + line8
        #print(lineout)
#       fo.write(lineout+'\r\n')
        fo.write(lineout) # +'\n')
        if cntout == 0:
           print('**converting ' + filepath + ' to '  + fileout + '...')
        cntout += 1

        line = fp.readline()
        cnt += 1
fp.close()
fo.close()
print('cnt=', cnt, ',cntout=', cntout)
#------------------

'''
now yus_candict_c_tongfreq.txt :-   key(column 1-3)  tone(4) rank(5-8) ch(9-10)
ah 30542亞
ah 30675阿
ah 10800啊
ah 22657啞
ah 13110丫
ah 33310氬
how to sort in asc key+tone+freq+ch ?
'''
# Read the input file
input_file = 'yus_candict_c_tonerankout.txt'

# Sort the lines
sorted_lines = sorted(open(input_file, 'r', encoding='utf-16'), key=lambda x: (x[4:8], x[0:3], x[3], x[8:10]))

# Write the sorted lines to a new file
output_file = 'yus_candict_c_ranknew.txt'
with open(output_file, 'w', encoding='utf-16') as f:
    f.writelines(sorted_lines)
print(input_file,' sorted in asc rank+key+tone+ch to ', output_file, ' OK')
'''
ah 10800啊
ah 13110丫
ah 15140椏
ah 17079吖
ah 22657啞
ah 30542亞
ah 30675阿
ah 33310氬
ah 35413婭
ai 11413埃
ai 12231唉
ai 12312哎
ai 16623娭
ai 22077矮
ai 26721欸
ai 33025隘
ai 34066縊
ai 35036嗌
ai 36197翳
ai 40948危
ai 42090挨
ai 43057巍
ai 43736倪
ai 44287霓
ai 53684蟻
ai 60519藝
ai 61494魏
ai 61833毅
ai 61836偽
ai 63328羿
ai 64097詣
ai 64994睨
ai 65714囈

dik10001的
yet10002一
siz60003是
joi60004在
bet10005不
liu50006了
yau50007有
wo 40008和
yan40009人
je 50010這
jug10011中
di 60012大
wai40013為
she50014上
goh30015個
kwo30016國
ngo50017我
yi 50018以
yiu30019要
dei60020地
ta 10021他
sis40022時
loi40023來
yug60024用
mun40025們
sag10026生
dou30027到
jok30028作
cut10029出
jau60030就
fun10031分
yu 10032於
dui30033對
shi40034成
wui20035會
hor20036可
jua20037主
fat30038發
nin40039年
dug60040動
tug40041同
gug10042工
ya 50043也
nag40044能
ha 60045下
gwo30046過
chi20047子
sut30048說
can20049產
jug20050種
'''
