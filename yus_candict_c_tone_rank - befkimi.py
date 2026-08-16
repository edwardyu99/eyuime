import codecs
import os
print('**yus_candict_c_tone.py - add tone rank to yus_candict_c.txt')
filein = 'yus_candict_c.txt'  
#yus_candict_c.txt :-   key(column 1-6) ' ' ch(8-9)
#cheung 張
fileout  = 'yus_candict_c_tone_rank.txt'
#yus_candict_c.txt :-   key(column 1-6) ' '  ch(8-9) ' ' tone(11) ' ' rank(13-16)
#cheung 張 1 7000

# 1. 建立聲調映射表 (從 jyutping.txt)
tone_map = {}
with codecs.open('jyutping.txt', 'r', 'utf-8') as f:
    next(f)  # 跳過標題列
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >= 6:
            char = parts[0]
            tone = parts[5]
            if char not in tone_map:
                tone_map[char] = tone

# 2. 建立排名映射表
#(從 cuhk_ch_rank_7000i.txt)
rank_file = 'cuhk_ch_rank_merge.txt'
rank_map = {}
with codecs.open(rank_file,'r', 'utf-8') as f:
    next(f)  # 跳過標題列
    for line in f:
        line = line.strip()
        if ',' in line:
            char, rank = line.split(',')
            rank_map[char] = rank

# 3. 讀取原表並整合輸出
with codecs.open(filein, 'r', 'utf-16') as f_in, \
     codecs.open(fileout, 'w', 'utf-16') as f_out:
    
    for line in f_in:
        line = line.rstrip('\r\n')
        if not line:
            f_out.write('\n')
            continue
        
        parts = line.split()
        if len(parts) >= 2:
            code = parts[0]
            char = parts[1]
            
            tone = tone_map.get(char, "")
            rank = rank_map.get(char, "")
            
            # 以 space 分隔各列：編碼 漢字 聲調 排名
            f_out.write(f"{code} {char} {tone} {rank}\n")
        else:
            f_out.write(f"{line}\n")

print(f"處理完成，檔案已儲存為: {fileout}")


