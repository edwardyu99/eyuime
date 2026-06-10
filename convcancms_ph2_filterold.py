import codecs
import os
import sys
import argparse  # <--- 新增：引入 argparse 模組處理命令列參數

# =====================================================================
# 參數解析設定
# =====================================================================
parser = argparse.ArgumentParser(description="處理余氏輸入法雙字詞編碼，並過濾低頻重碼詞")
parser.add_argument(
    '-r', '--rank-filter', 
    type=int, 
    default=100000, 
    help="設定雙字詞重碼過濾的詞頻閾值 (預設: 100000)。數值越小過濾越嚴格，重碼率越低。"
)
args = parser.parse_args()

RANK_FILTER = args.rank_filter  # 將輸入的參數賦值給變數

print(f"啟動程式：當前設定的重碼過濾閾值 RANK_FILTER = {RANK_FILTER}")
print("=" * 60)

import codecs
import os
import sys

# --- 定義全局文件名，防止 NameError ---
# filepath = 'reneeyu_canph2345or_aftcanph2.txt'
filepath = 'reneeyu_canph2345ori.txt'   
fileout  = 'reneeyu_canph2345out.txt'   
filedup  = 'reneeyu_canph2345outdup.txt' 
keypath  = 'yus_candict_c.txt'          
dictpath = 'merge_jieba.txt'
ph2path  = 'merge_ph2.txt'       # <--- 新增：雙字詞專用頻率表
filefreqmerge = 'reneeyu_canph2345out_freqmerge.txt'
final_out = 'reneeyu_canph2345ori_filtered.txt'

# =====================================================================
# 第一階段：編碼轉換 (恢復原本邏輯，確保產生 ngomoo 等拼音碼)
# =====================================================================
mydict = {}
with codecs.open(keypath, 'r', 'utf-16') as f:
    for line in f:
        if len(line) != 10: continue
        key = line[7]
        val = line[0:3]
        if mydict.get(key, '???') == '???':
            mydict[key] = val

if os.path.exists(fileout): os.remove(fileout)
fo = open(fileout, 'a+', encoding='utf-16') 

with open(filepath, 'r', encoding='utf-16') as fp:  
    line = fp.readline()
    cnt = cntout_total = 0
    while line:
        line_len = len(line)
        if line_len <= 1:
            line = fp.readline()
            continue
            
        if line_len == 10: # 2字 (恢復使用 key1, key2 尋找拼音碼)
            key1, key2 = line[7], line[8]
            val = (mydict.get(key1, 'xxx').rstrip() + mydict.get(key2, 'xxx').rstrip()).ljust(6)
            if mydict.get(key1, 'xxx') == 'xxx' or mydict.get(key2, 'xxx')  == 'xxx' :
                pass
            else:
                fo.write(f"{val} {key1}{key2}\n")
                
        elif line_len == 11: # 3字
            val = (mydict.get(line[7], 'x').rstrip() + mydict.get(line[8], 'x')[0] + mydict.get(line[9], 'x')[0]).ljust(6)
            fo.write(f"{val} {line[7:10]}\n")
            
        elif line_len >= 12: # 4字+
            temp_val = mydict.get(line[7], 'x').rstrip()
            for i in range(8, line_len - 1):
                temp_val += mydict.get(line[i], 'x')[0]
            val = temp_val[:6].ljust(6)
            fo.write(f"{val} {line[7:]}")
            
        cntout_total += 1
        line = fp.readline()
        cnt += 1
fo.close()
print(f"階段一完成：共處理 {cnt} 行，輸出 {cntout_total} 個詞組。")

# =====================================================================
# 第二階段：詞頻合併與排序 (在此處載入 merge_ph2.txt)
# =====================================================================
mergedict = {}

# 1. 讀取原本 merge_jieba.txt 的詞頻
if os.path.exists(dictpath):
    with codecs.open(dictpath, 'r', 'utf-16') as f:
        for line in f:
            if len(line) >= 9:
                mergedict[line[7:9]] = line[0:6].rstrip()

# 2. 讀取 merge_ph2.txt 的雙字詞詞頻 (優先使用，會覆蓋上方的同名詞)
if os.path.exists(ph2path):
    with codecs.open(ph2path, 'r', 'utf-16') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                freq, word = parts[0], parts[1]
                mergedict[word] = freq.zfill(6) # 確保寫入是 000001 這樣的6碼

with open(fileout, 'r', encoding='utf-16') as fp, \
     open(filefreqmerge, 'w', encoding='utf-16') as fom:
    for line in fp:
        word = line.strip().split()[-1]
        freq = mergedict.get(word[:2], '888888')
        prefix = f"{len(word):02d}"
        # 此時 line[0:6] 為拼音碼(ngomoo)，freq 為從 merge_ph2 取到的頻率(000001)
        fom.write(f"{prefix}{line[0:6]}{freq}{line[7:]}")

with open(filefreqmerge, 'r+', encoding="utf-16") as f:
    lines = f.readlines()
    lines.sort()
    f.seek(0)
    f.truncate()
    f.write(''.join(lines))
print(f"階段二完成：詞頻合併與排序成功。")

# =====================================================================
# 加入不在mergedict的雙字詞 - 詞頻默認值為 050000
# =====================================================================
with open(fileout, 'r', encoding='utf-16') as fp, \
     open(filefreqmerge, 'w', encoding='utf-16') as fom:
    prev_line = ""
    for line in fp:
        if line == prev_line: continue
        word = line.strip().split()[-1]
        freq = mergedict.get(word[:2], '050000')   # 默认值为 050000
        prefix = f"{len(word):02d}"
        fom.write(f"{prefix}{line[0:6]}{freq}{line[7:]}")
        prev_line = line

# =====================================================================
# 第三階段：格式化與清理 (使用傳入的 RANK_FILTER)
# =====================================================================
with open(filefreqmerge, 'r', encoding='utf-16') as fp, \
     open(final_out, 'w', encoding='utf-16') as fo:
    
    prev_line = ""
    code_count_map = {} 

    for line in fp:
        if line == prev_line: continue 
        
        prefix = line[0:2]     
        code = line[2:8]       
        freq_str = line[8:14]  
        word_part = line[14:]  

        if prefix == '02':
            try:
                rank = int(freq_str)
            except ValueError:
                rank = 50000 # 888888

            if code not in code_count_map:
                # 該編碼的第一候選詞無條件保留
                fo.write(f"{code} {word_part}")
                code_count_map[code] = 1
            else:
                # 後續重碼詞，若 rank <= RANK_FILTER 則保留
                if rank <= RANK_FILTER:
                    fo.write(f"{code} {word_part}")
                    code_count_map[code] += 1
        else:
            # 3字以上的詞不受此限制
            fo.write(f"{code} {word_part}")

        prev_line = line

print(f"階段三完成：最終碼表已更新至 {final_out}，低頻重碼詞（RANK > {RANK_FILTER}）已過濾。")

# <--- 修改：註解掉這段以保留暫存檔 (Debug用) --->
# for f in [fileout, filefreqmerge]: 
#     if os.path.exists(f): os.remove(f)

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
        dup_2char_rate = ((dup_2char_count ) / total_2char_count * 100) 
    else:
        homonym_rate = 0
        dup_2char_count = 0
        dup_2char_rate = 0

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
        for code in dup_codes_list:
            fd.write(f"{code} {' '.join(code_map[code])}\n")

    print(f"分析完成：")
    print(f"1. 雙字詞總數：{total_2char_count}")
    print(f"2. 使用的獨立編碼數：{distinct_codes}")
    print(f"3. 不重碼的雙字詞數：{unique_codes_count}")
    print(f"4. 發生重碼的雙字詞數：{dup_2char_count}")
    print(f"5. 雙字詞重碼率：{dup_2char_rate:.2f}%")
    print(f"6. 雙字詞編碼數重碼率：{homonym_rate:.2f}%")

    print(f"   詳細重碼清單已寫入：{filedup}")
else:
    print(f"錯誤：找不到最終碼表 {final_out}")