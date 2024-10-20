import codecs
import os
print('**yus_candict_c_tonefreq.py - add tonefreq to yus_candict_c.txt')
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
#------------------------------------------------------------
# 20230530 add tonedict -----------------------
import pandas as pd

# Read the input CSV file
input_file = 'cuhk_charfreq7000_粵拼_ori.csv' #'input.csv'
df = pd.read_csv(input_file, delimiter=',', index_col=False) # '\t')
print(df.columns)
print(df.head())
# Remove leading and trailing whitespace from the "jyutpi" column
df['jyutpi'] = df['jyutpi'].str.strip()
# Extract the last digit of the "jyutpi" column
df['tone'] = df['jyutpi'].str[-1]
print(df.columns)
print(df.head())
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
                print(f"Issue with line: {line}")
                continue

# Example of retrieving the tone value using a key
key_ch = '的'
tone_value = tone_dict.get(key_ch, 'x')
print(f"The tone value for '{key_ch}' is {tone_value}")
#--------------------------------------------
filepath = 'yus_candict_c_freq.txt' 
fileout  = 'yus_candict_c_tonefreq.txt'
if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
#linein = 'kug9999功' 
lineout = 'kug19999功' #key tone freq ch
with open(filepath,'r', encoding='utf-16') as fp:  
   line = fp.readline()
   cnt = 0
   cntout = 0
   
   while line:
     line = line.strip()
     #try:
     key_ch = line[7:9] #.encode('utf-16', 'surrogatepass').decode('utf-8')
     # tone = line.split(' ')[1]
     # tone_dict[key_ch] = tone
     #except (ValueError, IndexError):
     #  print(f"Issue with line: {line}")
     # key_ch = line[7:]
     tone_value = tone_dict.get(key_ch, 'x')
     # lineout = line[0:3] + '    ' + line[7:] 
     lineout = line[0:3] + tone_value + line[3:7] + line[7:9] + '\n'  #key tone freq ch
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
now yus_candict_c_tongfreq,txt :-   key(column 1-3)  tone(4) freq(5-8) ch(9-10)
ah 30542亞
ah 30675阿
ah 10800啊
ah 22657啞
ah 13110丫
ah 33310氬
how to sort in asc key+tone+freq+ch ?
'''
# Read the input file
input_file = 'yus_candict_c_tonefreq.txt'

# Sort the lines
sorted_lines = sorted(open(input_file, 'r', encoding='utf-16'), key=lambda x: (x[0:3], x[3], x[4:8], x[8:10]))

# Write the sorted lines to a new file
output_file = 'yus_candict_c_tonefreqsort.txt'
with open(output_file, 'w', encoding='utf-16') as f:
    f.writelines(sorted_lines)
print(input_file,' sorted in asc key+tone+freq+ch to ', output_file, ' OK')
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
'''

# Read the input file
input_file = 'yus_candict_c_tonefreqsort.txt'

# Read the lines from the input file
with open(input_file, 'r', encoding='utf-16') as f:
    lines = f.readlines()

# Group the lines by key
groups = {}
for line in lines:
    key = line.split(' ')[0]
    if key in groups:
        groups[key].append(line)
    else:
        groups[key] = [line]

# Sort and output lines per group in a cycle of tones 1 to 6
output_file = 'output_per_group.txt'
with open(output_file, 'w', encoding='utf-16') as f:
    for key, group in groups.items():
        for tone in range(1, 7):  # Cycle of tones 1 to 6
            tone_group = [line for line in group if int(line.split(' ')[1]) == tone]
            if len(tone_group) > 0:
                f.writelines(tone_group)
