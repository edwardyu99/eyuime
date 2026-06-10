# -*- coding: utf-8 -*-
import codecs
import os
import sys
import argparse  
import shutil

# =====================================================================
# 參數解析設定
# =====================================================================
parser = argparse.ArgumentParser(description="處理余氏輸入法雙字詞編碼，並過濾低頻重碼詞")
parser.add_argument(
    '-r', '--rank-filter', 
    type=int, 
    default=55000, 
    help="設定雙字詞重碼過濾的詞頻閾值 (預設: 55000)。數值越小過濾越嚴格，重碼率越低。"
)
args = parser.parse_args()

RANK_FILTER = args.rank_filter

print(f"啟動程式：當前設定的重碼過濾閾值 RANK_FILTER = {RANK_FILTER}")
print("=" * 60)

# --- 定義全局文件名 ---
filepath  = 'reneeyu_canph2345ori.txt'   
fileout   = 'reneeyu_canph2345out.txt'   
filedup   = 'reneeyu_canph2345outdup.txt' 
filediscard  = 'reneeyu_canph2345ori_discard.txt'
keypath   = 'yus_candict_c.txt'          
dictpath  = 'merge_ph2.txt'
ph2path   = 'merge_ph2.txt'       
filefreqmerge = 'reneeyu_canph2345out_freqmerge.txt'
final_out = 'reneeyu_canph2345ori_filtered.txt'

# =====================================================================
# 記錄輸入/輸出檔案行數的字典
# =====================================================================
line_counts = {
    'input': {},
    'output': {}
}

# =====================================================================
# 第一階段：編碼轉換
# =====================================================================
mydict = {}
keypath_lines = 0
with codecs.open(keypath, 'r', 'utf-16') as f:
    for line in f:
        keypath_lines += 1
        if len(line) != 10: continue
        key = line[7]
        val = line[0:3]
        if mydict.get(key, '???') == '???':
            mydict[key] = val
line_counts['input'][keypath] = keypath_lines

if os.path.exists(fileout): os.remove(fileout)
fo = open(fileout, 'w', encoding='utf-16')

filepath_lines = 0
written_lines = 0

with open(filepath, 'r', encoding='utf-16') as fp:
    line = fp.readline()
    while line:
        filepath_lines += 1
        line_len = len(line)
        if line_len <= 1:
            line = fp.readline()
            continue
            
        if line_len == 10: 
            key1, key2 = line[7], line[8]
            val = (mydict.get(key1, 'xxx').rstrip() + mydict.get(key2, 'xxx').rstrip()).ljust(6)
            if mydict.get(key1, 'xxx') == 'xxx' or mydict.get(key2, 'xxx') == 'xxx':
                pass
            else:
                fo.write(f"{val} {key1}{key2}\n")
                written_lines += 1
                
        elif line_len == 11: 
            val = (mydict.get(line[7], 'x').rstrip() + mydict.get(line[8], 'x')[0] + mydict.get(line[9], 'x')[0]).ljust(6)
            fo.write(f"{val} {line[7:10]}\n")
            written_lines += 1
            
        elif line_len >= 12: 
            temp_val = mydict.get(line[7], 'x').rstrip()
            for i in range(8, line_len - 1):
                temp_val += mydict.get(line[i], 'x')[0]
            val = temp_val[:6].ljust(6)
            fo.write(f"{val} {line[7:]}")
            written_lines += 1
            
        line = fp.readline()
fo.close()

line_counts['input'][filepath] = filepath_lines
line_counts['output'][fileout] = written_lines
print(f"階段一完成：共讀取 {filepath_lines} 行，實際寫入 {written_lines} 個詞組。")

# =====================================================================
# 檢測重複（同一個詞視為重複，保留第一筆）
# =====================================================================
print("\n--- 開始檢測原始輸入檔重複行（同詞不同碼也視為重複） ---")
duplicate_lines = []
seen_words = {}

with open(filepath, 'r', encoding='utf-16') as f:
    for i, line in enumerate(f, 1):
        stripped = line.strip()
        if not stripped:
            continue
            
        # 分割出「詞」部分（空格後的內容）
        parts = stripped.split(maxsplit=1)
        if len(parts) >= 2:
            word = parts[1]          # 只取詞的部分
        else:
            word = stripped          # 異常行，整行比對
        
        if word in seen_words:
            duplicate_lines.append((i, stripped))
        else:
            seen_words[word] = True

if duplicate_lines:
    print(f"發現 {len(duplicate_lines)} 處重複（同詞不同碼）：")
    for lineno, content in duplicate_lines:
        print(f"  第 {lineno} 行 → {content}")
else:
    print("未發現重複行。")

# =====================================================================
# 清理原始輸入檔（同詞只保留第一筆）
# =====================================================================
print("\n--- 開始清理原始輸入檔 ---")
backup_file = filepath + '.bak'
if os.path.exists(backup_file):
    os.remove(backup_file)

shutil.copy2(filepath, backup_file)

unique_lines = []
seen_words.clear()

with open(filepath, 'r', encoding='utf-16') as f:
    for line in f:
        stripped = line.strip()
        if not stripped:
            unique_lines.append(line)
            continue
            
        parts = stripped.split(maxsplit=1)
        if len(parts) >= 2:
            word = parts[1]
        else:
            word = stripped
        
        if word in seen_words:
            continue
        seen_words[word] = True
        unique_lines.append(line)

with open(filepath, 'w', encoding='utf-16') as f:
    f.writelines(unique_lines)

print(f"原始輸入檔清理完成：")
print(f"   原有 {filepath_lines} 行 → 清理後 {len(unique_lines)} 行")
print(f"   移除 {len(duplicate_lines)} 行重複（同詞）")
print(f"   原始檔已備份至：{backup_file}")

# =====================================================================
# 第二階段：詞頻合併與排序
# =====================================================================
mergedict = {}
dictpath_lines = 0
if os.path.exists(dictpath):
    with codecs.open(dictpath, 'r', 'utf-16') as f:
        for line in f:
            dictpath_lines += 1
            if len(line) >= 9:
                mergedict[line[7:9]] = line[0:6].rstrip()
    line_counts['input'][dictpath] = dictpath_lines

ph2path_lines = 0
if os.path.exists(ph2path):
    with codecs.open(ph2path, 'r', 'utf-16') as f:
        for line in f:
            ph2path_lines += 1
            parts = line.strip().split()
            if len(parts) >= 2:
                freq, word = parts[0], parts[1]
                mergedict[word] = freq.zfill(6) 
    line_counts['input'][ph2path] = ph2path_lines

freqmerge_lines = 0
seen = set()

with open(fileout, 'r', encoding='utf-16') as fp, \
     open(filefreqmerge, 'w', encoding='utf-16') as fom:
    
    for line in fp:
        if line in seen:
            continue
        seen.add(line)
        
        word = line.strip().split()[-1]
        freq = mergedict.get(word[:2], '108888') 
        prefix = f"{len(word):02d}"
        fom.write(f"{prefix}{line[0:6]}{freq}{line[7:]}")
        freqmerge_lines += 1

line_counts['output'][filefreqmerge] = freqmerge_lines

with open(filefreqmerge, 'r+', encoding="utf-16") as f:
    lines = f.readlines()
    lines.sort()
    f.seek(0)
    f.truncate()
    f.write(''.join(lines))

print(f"階段二完成：詞頻合併與排序成功，共 {freqmerge_lines} 行。")

# =====================================================================
# 第三階段
# =====================================================================
filtered_out_map = {}
final_out_lines = 0

with open(filefreqmerge, 'r', encoding='utf-16') as fp, \
     open(final_out, 'w', encoding='utf-16') as fo:
    
    code_count_map = {} 

    for line in fp:
        prefix = line[0:2]     
        code = line[2:8]       
        freq_str = line[8:14]  
        word_part = line[14:]  

        if prefix == '02':
            try:
                rank = int(freq_str)
            except ValueError:
                rank = 108888 

            if code not in code_count_map:
                fo.write(f"{code} {word_part}")
                final_out_lines += 1
                code_count_map[code] = 1
            else:
                if rank <= RANK_FILTER:
                    fo.write(f"{code} {word_part}")
                    final_out_lines += 1
                    code_count_map[code] += 1
                else:
                    clean_code = code.strip()
                    clean_word = word_part.strip()
                    if clean_code not in filtered_out_map:
                        filtered_out_map[clean_code] = []
                    filtered_out_map[clean_code].append(clean_word)
        else:
            fo.write(f"{code} {word_part}")
            final_out_lines += 1

line_counts['output'][final_out] = final_out_lines
print(f"階段三完成：最終碼表已更新至 {final_out}，低頻重碼詞已過濾。")

# =====================================================================
# 第四階段：雙字詞重碼分析
# =====================================================================
print("\n--- 開始分析雙字詞重碼情況 ---")

code_map = {}
total_2char_count = 0

if os.path.exists(final_out):
    with open(final_out, 'r', encoding='utf-16') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2: continue
            code, word = parts[0], parts[1]
            if len(word) == 2:
                total_2char_count += 1
                if code not in code_map: code_map[code] = []
                code_map[code].append(word)

    distinct_codes = len(code_map)
    dup_codes_list = [c for c, w in code_map.items() if len(w) > 1]
    dup_codes_count = len(dup_codes_list)
    unique_codes_count = distinct_codes - dup_codes_count 
    if total_2char_count > 0:
        homonym_rate = (dup_codes_count / distinct_codes * 100) 
        dup_2char_count = total_2char_count - unique_codes_count
        dup_2char_rate = (dup_2char_count / total_2char_count * 100) 
    else:
        homonym_rate = 0
        dup_2char_count = 0
        dup_2char_rate = 0

    dup_lines = 0
    with open(filedup, 'w', encoding='utf-16') as fd:
        fd.write(f"【雙字詞重碼分析報告】\n")
        fd.write(f"過濾條件：重碼詞頻 RANK > {RANK_FILTER} 捨棄\n")
        fd.write("-" * 30 + "\n")
        fd.write(f"1. 雙字詞總數：{total_2char_count}\n")
        fd.write(f"2. 使用的獨立編碼數：{distinct_codes}\n")
        fd.write(f"3. 不重碼的雙字詞數：{unique_codes_count}\n")
        fd.write(f"4. 發生重碼的雙字詞數：{dup_2char_count}\n")
        fd.write(f"5. 雙字詞重碼率：{dup_2char_rate:.2f}%\n")
        fd.write(f"6. 雙字詞編碼數重碼率：{homonym_rate:.2f}%\n")
        fd.write("-" * 30 + "\n")
        dup_lines = 8
        
        for code in sorted(dup_codes_list):
            for w in code_map[code]:
                freq = mergedict.get(w, '108888')
                padded_code = code.ljust(6)
                fd.write(f"{padded_code} {freq} {w}\n")
                dup_lines += 1
    line_counts['output'][filedup] = dup_lines

    filtered_count = sum(len(words) for words in filtered_out_map.values())
    if filtered_count > 0:
        with open(filediscard, 'w', encoding='utf-8') as fdiscard:
            fdiscard.write(f"【被過濾捨棄的雙字詞清單】\n")
            fdiscard.write(f"過濾條件：重碼詞頻 RANK > {RANK_FILTER} 捨棄\n")
            fdiscard.write("-" * 30 + "\n")
            fdiscard.write(f"總計捨棄的雙字詞數量：{filtered_count}\n")
            fdiscard.write("-" * 30 + "\n")
            for code, words in sorted(filtered_out_map.items()):
                padded_code = code.ljust(6)
                for w in words:
                    freq = mergedict.get(w, '108888')
                    fdiscard.write(f"{padded_code} {freq} {w}\n")
        line_counts['output'][filediscard] = filtered_count + 5

    print(f"分析完成：")
    print(f"1. 雙字詞總數：{total_2char_count}")
    print(f"2. 使用的獨立編碼數：{distinct_codes}")
    print(f"3. 不重碼的雙字詞數：{unique_codes_count}")
    print(f"4. 發生重碼的雙字詞數：{dup_2char_count}")
    print(f"5. 雙字詞重碼率：{dup_2char_rate:.2f}%")
    print(f"6. 雙字詞編碼數重碼率：{homonym_rate:.2f}%")
    print(f"   保留的重碼清單已寫入：{filedup}")
    if filtered_count > 0:
        print(f"   被捨棄的過濾清單已寫入：{filediscard} (共 {filtered_count} 個詞彙)")

# =====================================================================
# 最終統計
# =====================================================================
print("\n" + "=" * 60)
print("【檔案行數統計】")
print("-" * 60)
print("輸入檔案：")
for fname, lines in line_counts['input'].items():
    print(f"  {fname} : {lines} 行")
print("輸出檔案：")
for fname, lines in line_counts['output'].items():
    print(f"  {fname} : {lines} 行")
print("=" * 60)