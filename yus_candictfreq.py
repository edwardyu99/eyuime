import codecs
import os
print('**yus_candictfreq.py - add freq to yus_candict_c.txt')
filepath = 'yus_candict_c.txt'  
#ang    鶯
fileout  = 'yus_candict_c_freq.txt'
#ang9999鶯
#keyyus    = 'can_faq_sorted7000.txt'
keyyus    = 'cuhk_charfreq7000utf16.txt'  
#0123456789012345678901234567890
#0001 489803 的   0002 166396 一
mydict = {}

with codecs.open(keyyus,'r','utf-16') as f:
    line = f.readline() #skip first line with BOM utf-16
    line = f.readline()
    while line: 
       key = line[11:13]  #utf16 char counted as 1, pre-space as key
       val = line[0:4]
       key2 = line[27:29] #utf16 char counted as 1, pre-space as key
       val2 = line[16:20]
       #if line[2]== ' ':
       #   val = line[0:2].rstrip()
       #else:
       #   val = line[0] + line[2]
       #print(key+val)
       #print(key2+val2)
# prevent duplicate key dict
       #valdict = mydict.get(key,'xxxx')
       #if valdict == 'xxxx':
       mydict[key] = val
       #valdict = mydict.get(key2,'xxxx')
       #if valdict == 'xxxx':
       mydict[key2] = val2
           
       line = f.readline()
f.close()
dictsize = len(mydict)
#print(mydict,dictsize)
print("bef dictsize = ",dictsize)

if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
lineout = 'ang9999鶯' 
with open(filepath,'r', encoding='utf-16') as fp:  
   line = fp.readline()
   cnt = 0
   cntout = 0
   
   while line:
#        
# 7key + 2(utf-16)char + lf = 10
       
        #print(line)
        key0 = line[0:3]
        key1 = line[6:8] #utf16 char counted as 1,pre-space as key
        key1nl = line[7:] 
        val1 = mydict.get(key1, 'xxxx')      
        if val1 == 'xxxx':
            dictsize += 1
            val1 = str(int(dictsize))  
            mydict[key1] = val1  #add new dict item
        lineout = key0 + val1 + key1nl
        #print(lineout)
#       fo.write(lineout+'\r\n')
        fo.write(lineout) # +'\n')
        if cntout == 0:
           print('**converting ' + filepath + '...')
        cntout += 1

        line = fp.readline()
        cnt += 1
fp.close()
fo.close()
print('cnt=', cnt, ',cntout=', cntout)
#------------------
csv_file = "cuhk_charfreq7000.csv"
csv_columns = ['ch','rank']
if os.path.exists(csv_file):
    os.remove(csv_file)
#fdict = open(filedict,'a+') #, encoding='utf-16') 
import csv
with open(csv_file, 'a+', encoding='utf-8') as f:
    f.write("%s,%s\n"%(csv_columns[0], csv_columns[1] ))
    for key in mydict.keys():
        f.write("%s,%s\n"%(key.lstrip(), mydict[key]))  # left strip space
print("aft dictsize = ",len(mydict))
#------------------
with open(fileout, 'r+',encoding="utf-16") as f:
    sorted_contents=''.join(sorted(f.readlines())) #, key = lambda x: int(x.split(' ')[0])))
    f.seek(0)
    f.truncate()
    f.write(sorted_contents)
print(fileout,' sorted OK')
#----------------------
import codecs
import os

# remove middle freqrank 9999 after sort
filepath = 'yus_candict_c_freq.txt' 
fileout  = 'yus_candict_c_freqsort.txt'
if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
#linein = 'kug9999功' 
lineout = 'kug    功' 
with open(filepath,'r', encoding='utf-16') as fp:  
   line = fp.readline()
   cnt = 0
   cntout = 0
   
   while line:
       lineout = line[0:3] + '    ' + line[7:] 
       fo.write(lineout)
       cntout += 1  
       line = fp.readline()
       cnt += 1
fp.close()
fo.close()

print('cnt=', cnt, ',cntout=', cntout)

print(filepath,' sorted by freqrank to ', fileout, ' OK')
