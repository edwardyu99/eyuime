import codecs
import os

print('**yus_candict_c_tone_rank.py - add tone rank to yus_candict_c.txt')

filein  = 'yus_candict_c.txt'
fileout = 'yus_candict_c_tone_rank.txt'

# 統計行數用的輔助函數
def count_lines(filepath, encoding='utf-8'):
    try:
        with codecs.open(filepath, 'r', encoding) as f:
            return sum(1 for _ in f)
    except Exception as e:
        return f"無法讀取 ({e})"

# 1. 建立聲調映射表 (從 jyutping.txt)
tone_file = 'jyutping.txt'
tone_map = {}
with codecs.open(tone_file, 'r', 'utf-8') as f:
    next(f)  # 跳過標題列
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >= 6:
            char = parts[0]
            tone = parts[5]
            if char not in tone_map:
                tone_map[char] = tone

# 2. 建立排名映射表 (從 cuhk_ch_rank_merge.txt)
rank_file = 'cuhk_ch_rank_merge.txt'
rank_map = {}
with codecs.open(rank_file, 'r', 'utf-8') as f:
    next(f)  # 跳過標題列
    for line in f:
        line = line.strip()
        if ',' in line:
            char, rank = line.split(',')
            rank_map[char] = rank

# 3. 讀取原表並整合輸出
out_lines = 0
with codecs.open(filein, 'r', 'utf-16') as f_in, \
     codecs.open(fileout, 'w', 'utf-16') as f_out:
    
    for line in f_in:
        line = line.rstrip('\r\n')
        if not line:
            f_out.write('\n')
            out_lines += 1
            continue
        
        parts = line.split()
        if len(parts) >= 2:
            code = parts[0]
            char = parts[1]
            tone = tone_map.get(char, "")
            rank = rank_map.get(char, "")
            # code 固定 6 字符寬度，左對齊，右邊補 trailing space
            f_out.write(f"{code:<6} {char} {tone} {rank}\n")
            out_lines += 1
        else:
            f_out.write(f"{line}\n")
            out_lines += 1

# 顯示檔名與行數統計
print("-" * 40)
print("檔案行數統計：")
print(f"  輸入 - {tone_file:<30} : {count_lines(tone_file, 'utf-8')} 行")
print(f"  輸入 - {rank_file:<30} : {count_lines(rank_file, 'utf-8')} 行")
print(f"  輸入 - {filein:<30} : {count_lines(filein, 'utf-16')} 行")
print(f"  輸出 - {fileout:<30} : {out_lines} 行")
print("-" * 40)
print(f"處理完成，檔案已儲存為: {fileout}")