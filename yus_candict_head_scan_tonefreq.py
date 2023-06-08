import codecs
import os
#filepath = 'yus_candict_head_scan.txt'  
filepath = 'reneeyu_head.txt' 
print(f'** scan {filepath} for first tonefreq')
#cheung 張
fileout  = 'yus_candict_head_scan_freq.txt'
#cheung 19999張
#keyyus    = 'can_faq_sorted7000.txt'
keyyus    = 'cuhk_charfreq7000utf16.txt'  
#0123456789012345678901234567890
#0001 489803 的   0002 166396 一
mydict = {}

with codecs.open(keyyus,'r','utf-16') as f:
    line = f.readline() #skip first line with BOM utf-16
    line = f.readline()
    while line: 
       #line = line.strip()
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
#cheung 張
lineout = 'cheung 9999張' 
with open(filepath,'r', encoding='utf-16') as fp:  
   for i in range(13): #skip 13 lines
        fp.readline()
   line = fp.readline()
   cnt = 0
   cntout = 0
   
   while line:
#        
# 7key + 2(utf-16)char + lf = 10
       
        #print(line)
        #line = line.strip()
        key0 = line[0:6] #cheung [0:3]
        if key0 == 'ahr   ':	
          break 
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
''' just scan no sort
with open(fileout, 'r+',encoding="utf-16") as f:
    sorted_contents=''.join(sorted(f.readlines())) #, key = lambda x: int(x.split(' ')[0])))
    f.seek(0)
    f.truncate()
    f.write(sorted_contents)
print(fileout,' sorted OK')
'''
#----------------------
import codecs
import os

#------------------------------------------------------------
# 20230530 add tonedict -----------------------
import pandas as pd

# Read the input CSV file
input_file = 'cuhk_charfreq7000_粵拼_ori.csv' #'input.csv'
df = pd.read_csv(input_file, delimiter=',', index_col=False) # '\t')
# Remove leading and trailing whitespace from the "jyutpi" column
df['jyutpi'] = df['jyutpi'].str.strip()
# Extract the last digit of the "jyutpi" column
df['tone'] = df['jyutpi'].str[-1]
#print(df.columns)
#print(df.head())
# Write the output CSV file
output_file = 'cuhk_charfreq7000_粵拼_ori_output.csv'
df.to_csv(output_file, index=False)

# Read the output CSV file
# already from prev   output_file = 'cuhk_charfreq7000_粵拼_ori_output.csv'
df = pd.read_csv(output_file)

# Create a dictionary with 'ch' as keys and 'tone' as values
tone_dict = dict(zip(df['ch'], df['tone']))

# Save the dictionary as a UTF-16 encoded text file
dict_file = 'cuhk_charfreq7000_粵拼_ori_tones_dict.txt'
with open(dict_file, 'w', encoding='utf-16') as f:
	for ch, tone in tone_dict.items():
		# tab-sep f.write(f"{ch}\t{tone}\n")
		f.write(f"{ch} {tone}\n") # space-sep
				
# Read the tones_dict.txt file and recreate the tone_dict
# already from prev dict_file = 'tones_dict.txt'
#tone_dict = {}
'''
with open(dict_file, 'r', encoding='utf-16') as f:
  for line in f:
    ch, tone = line.strip().split(' ')
    tone_dict[ch] = tone
'''
# Read the tones_dict.txt file and recreate the tone_dict
tone_dict = {}
with open(dict_file, 'r', encoding='utf-16') as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                ch, tone = line.split(' ')
                tone_dict[ch] = tone
            except ValueError:
                print(f"{dict_file} Issue with line: {line}")
                continue

# Example of retrieving the tone value using a key
#key_ch = '的'
#tone_value = tone_dict.get(key_ch, 'x')
#print(f"The tone value for '{key_ch}' is {tone_value}")
#--------------------------------------------
filepath = 'yus_candict_head_scan_freq.txt' 
fileout  = 'yus_candict_head_scan_tonefreq.txt'
if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
#linein = 'cheung9999張' 
lineout = 'cheung 1 9999 張' #key tone freq ch
with open(filepath,'r', encoding='utf-16') as fp:  
   line = fp.readline()
   cnt = 0
   cntout = 0
   
   while line:
     line = line.strip()
     #try:
     key_ch = line[10:12] # line[7:9] #.encode('utf-16', 'surrogatepass').decode('utf-8')
     # tone = line.split(' ')[1]
     # tone_dict[key_ch] = tone
     #except (ValueError, IndexError):
     #  print(f"Issue with line: {line}")
     # key_ch = line[7:]
     tone_value = tone_dict.get(key_ch, 'x')
     if tone_value == 'x':
     	tone_value = '1' # default '6' for char not in dict
     	print(f"{filepath} key: {key_ch} not found, default tone = 6")
     # lineout = line[0:3] + '    ' + line[7:] 
     lineout = line[0:6] + ' ' + tone_value + ' ' + line[6:10] + ' ' + line[10:12] + '\n'  #key tone freq ch
     fo.write(lineout)
     cntout += 1  
     line = fp.readline()
     cnt += 1
fp.close()
fo.close()

print('cnt=', cnt, ',cntout=', cntout)

print(filepath,' add tone to ', fileout, ' OK')
#---------------------------------------
'''
now yus_candict_head_scan_tongfreq,txt :-   key(column 1-6)  tone(8) freq(10-13) ch(15-16)
1234567890123456
ah     3 0542 亞
ah     3 0675 阿
ah     1 0800 啊
ah     2 2657 啞
ah     1 3110 丫
ah     3 3310 氬
how to sort in asc key+tone+freq+ch ?
'''
# Read the input file
input_file = 'yus_candict_head_scan_tonefreq.txt'
''' just scan no need to sort
# Sort the lines - 
# sorted_lines = sorted(open(input_file, 'r', encoding='utf-16'), key=lambda x: (x[0:6], x[7], x[9:13], x[14:16]))

# Write the sorted lines to a new file
output_file = 'yus_candict_head_scan_tonefreqsort.txt'
with open(output_file, 'w', encoding='utf-16') as f:
    f.writelines(sorted_lines)
print(input_file,' sorted in asc key tone freq ch to ', output_file, ' OK')

ah     1 0800 啊
ah     1 0957 呀
ah     1 2140 鴉
ah     1 3110 丫
ah     1 5140 椏
ah     1 7073 吖
ah     2 2657 啞
ah     3 0542 亞
ah     3 0675 阿
ah     3 3310 氬
ah     3 5413 婭
ah     4 1401 牙
ah     4 1470 芽
ah     4 2652 衙
'''

import codecs
import os
import re

# Read the input file
#input_file = 'yus_candict_head_scan_tonefreqsort.txt'
output_file = 'yus_candict_head_scan_tonegroup.txt'
if os.path.exists(output_file):
    os.remove(output_file)
with open(input_file, 'r', encoding='utf-16') as fin, open(output_file, 'w', encoding='utf-16') as fout:
    prev_key = ''
    prev_tone = 0
    tone = 1
    seq = 0
    
    
    for line in fin:
        line = line.strip() # 'cheung 1 9999 xx' #key0 tone1 freq ch
        elements = re.split(r'\s+', line)
        
        if len(elements) < 2 or not elements[1].isdigit():
          print(f"{input_file} Issue with line: {line}")
          continue
        key0 = elements[0].ljust(6) # fill trailing spaces up to len=8
        tone1 = elements[1]
        freq = elements[2]
        ch = elements[3]
        
        # key = ' '.join(elements[:3])
        key = key0 + tone1
        
        if key != prev_key:
            tone = int(tone1) #1
            # prev_tone = 0
            seq = 0
            #if (tone > 1 and tone != prev_tone + 1):
            #	seq = 1
            prev_tone = 0
        
        '''if tone == prev_tone:
        	  tone += 1
        	  if tone > 6: 
        	  	tone = 1
        '''   
        
        fout.write(line + ' ' + str(tone) + str(seq).zfill(2) + '\n')
        tone += 1
        if tone > 9:
        	tone = 9
        seq += 1
        #if (tone > 3):
        #	seq += 1
        
        prev_key = key
        prev_tone = int(tone1)
    
'''
ah     1 0800 啊 100
ah     1 0957 呀 201
ah     1 2140 鴉 302
ah     1 3110 丫 403
ah     1 5140 椏 504
ah     1 7073 吖 605
ah     2 2657 啞 200
ah     3 0542 亞 300
ah     3 0675 阿 401
ah     3 3310 氬 502
ah     3 5413 婭 603
ah     4 1401 牙 400
ah     4 1470 芽 501
ah     4 2652 衙 602
ah     5 1057 瓦 500
ah     5 1921 雅 601
ah     6 3195 訝 600
ah     6 6182 禡 701
ah     6 6517 迓 802
ai     1 1413 埃 100
ai     1 2231 唉 201
ai     1 2312 哎 302
ai     2 2077 矮 200
ai     2 2976 噯 301
ai     3 3025 隘 300
ai     3 4066 縊 401
ai     3 5036 嗌 502
ai     3 6197 翳 603
01234567890123456789
'''
# Read the input file
input_file = 'yus_candict_head_scan_tonegroup.txt'
''' just scan no need to sort
# Sort the lines
sorted_lines = sorted(open(input_file, 'r', encoding='utf-16'), key=lambda x: (x[0:6], x[17:19])) # x[17:20]))

# Write the sorted lines to a new file
output_file = 'yus_candict_head_scan_tonegroupsort.txt'
with open(output_file, 'w', encoding='utf-16') as f:
    f.writelines(sorted_lines)
print(input_file,' sorted in asc key tonecycleseq to ', output_file, ' OK')
#----------------------------------------------------
# remove extra fields after sort

filepath = 'yus_candict_head_scan_tonegroupsort.txt'
fileout  = 'yus_candict_head_scan_tonefinal.txt'
if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
#linein = 'kug9999功' 
#ai     3 6197 翳 603
#01234567890123456789
lineout = 'kug    功' 
with open(filepath,'r', encoding='utf-16') as fp:  
   line = fp.readline()
   cnt = 0
   cntout = 0
   
   while line:
       lineout = line[0:7] + line[14:15] + '\n'
       fo.write(lineout)
       cntout += 1  
       line = fp.readline()
       cnt += 1
fp.close()
fo.close()

print('cnt=', cnt, ',cntout=', cntout)

print(filepath,' remove tone freqrank to ', fileout, ' OK')
'''
#---20230605 - scan first line at key break
fileout  = 'yus_candict_head_scan_keybreak.txt'
scanout  = 'yus_candict_head_scan_except.txt'
if os.path.exists(fileout):
    os.remove(fileout)
if os.path.exists(scanout):
    os.remove(scanout)
fo = open(fileout,'a+', encoding='utf-16') 
fe = open(scanout,'a+', encoding='utf-16') 
#ai     3 6197 翳 603
#01234567890123456789
scanout = 'ai     3 6197 翳 603' 
with open(input_file,'r', encoding='utf-16') as fp:  
   line = fp.readline()
   cnt = 0
   cntout = 0
   scanout = 0
   prev_key = '      '
   while line:
     key = line[0:6]
     tone = line[7:8]
     freqrank = line[9:13]
     if line[0:6] != prev_key:
       prev_key = line[0:6]  
       # lineout = line[0:7] + line[14:15] + '\n'
       fo.write(line) # lineout
       cntout += 1  
       #if line[7] != '1' and int(line[9:13]) > 1500:
       #	 #print(line)
       #	 fe.write(line)
       if tone == '1' and freqrank > '1800':
       	 #print(line)
       	 fe.write(line)
       	 scanout += 1
     
     line = fp.readline()
     cnt += 1
fp.close()
fo.close()
fe.close()
print(f'cnt={cnt}, cntout={cntout}, scanout={scanout}')

print(input_file,' scan keybreak [0:6] to ', fileout, ' OK')