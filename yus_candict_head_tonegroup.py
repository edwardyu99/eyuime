import codecs
import os
import re

# Read the input file
input_file = 'yus_candict_head_tonefreqsort.txt'
output_file = 'yus_candict_head_tonegroup.txt'

with open(input_file, 'r', encoding='utf-16') as fin, open(output_file, 'w', encoding='utf-16') as fout:
    prev_key = ''
    prev_tone = 0
    tone = 1
    seq = 0
    
    for line in fin:
        line = line.strip() # 'cheung 1 9999 xx' #key0 tone1 freq ch
        elements = re.split(r'\s+', line)
        
        if len(elements) < 2 or not elements[1].isdigit():
            continue
        key0 = elements[0].ljust(6) # fill trailing spaces up to len=8
        tone1 = elements[1]
        freq = elements[2]
        ch = elements[3]
        
        # key = ' '.join(elements[:3])
        key = key0 + tone1
        
        if key != prev_key:
            tone = int(tone1) #1
            seq = 0
            prev_tone = 0
        
        if tone == prev_tone:
        	  tone += 1
        	  if tone > 6: 
        	  	tone = 1
           
        
        
        fout.write(line + ' ' + str(tone) + str(seq).zfill(2) + '\n')
        tone += 1
        if tone > 9:
        	tone = 9
        seq += 1
        
        prev_key = key
        prev_tone = int(tone1)
    

'''
# Read the lines from the input file
with open(input_file, 'r', encoding='utf-16') as f:
    lines = f.readlines()

# Group the lines by key
groups = {}
for line in lines:
    # key = line.split(' ')[0]
    key = re.split(r'\s+', line)[0]   # separated by 1 or more spaces
    if key in groups:
        groups[key].append(line)
    else:
        groups[key] = [line]

# Sort and output lines per group in a cycle of tones 1 to 6
output_file = 'yus_candict_head_tonegroup.txt'
with open(output_file, 'w', encoding='utf-16') as f:
    for key, group in groups.items():
        for tone in range(1, 7):  # Cycle of tones 1 to 6
            # tone_group = [line for line in group if int(line.split(' ')[1]) == tone]
            # tone_group = [line for line in group if line.split(' ')[1].isdigit() and int(line.split(' ')[1]) == tone]
            # tone_group = [line for line in group if len(re.split(r'\s+', line)) > 1 and int(re.split(r'\s+', line)[1]).isdigit() and int(re.split(r'\s+', line)[1]) == tone]
            tone_group = [line for line in group if len(re.split(r'\s+', line)) > 1 and re.split(r'\s+', line)[1].isdigit() and int(re.split(r'\s+', line)[1]) == tone]
            if len(tone_group) > 0:
                f.writelines(tone_group)
'''