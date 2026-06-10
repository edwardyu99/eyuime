import codecs
import os
import sys
import platform
import shutil

# 顯示系統資訊
print(f"Python 版本: {sys.version}")
print(f"操作系統: {platform.system()}")
print('** 執行 convphyusms.py：將原始詞庫轉換為速成快速碼詞庫 **')

# =====================================================================
# 第一階段：速成編碼轉換 (Phrase to Quick Code Conversion)
# 目的：利用 yus_msquickdict.txt 將漢字詞組轉為 2-6 位的速成/快速碼
# =====================================================================

filepath = 'reneeyu_canph2345ori.txt'  # 輸入：原始詞組清單
fileout  = 'reneeyu_ph2345out.txt'     # 輸出：速成編碼初步結果
filedup  = 'reneeyu_ph2345outdup.txt'  # 輸出：記錄重複的編碼
keyyus   = 'yus_msquickdict.txt'       # 參考：速成快速碼單字字典

# 1. 載入速成快速碼字典
mydict = {}
with codecs.open(keyyus, 'r', 'utf-16') as f:
    for line in f:
        key = line[7] # 漢字
        # 邏輯：處理字典編碼位元（判斷第3位是否為空）
        if line[2] == ' ':
            val = line[0:2].rstrip()
        else:
            val = line[0] + line[2]
        
        # 防止字典重複，僅保留首個匹配
        if mydict.get(key, '??') == '??':
            mydict[key] = val

# 2. 初始化輸出文件
if os.path.exists(filedup): os.remove(filedup)
if os.path.exists(fileout): os.remove(fileout)
fd = open(filedup, 'a+', encoding='utf-16') 
fo = open(fileout, 'a+', encoding='utf-16') 

# 3. 處理並轉換詞組
with open(filepath, 'r', encoding='utf-16') as fp:  
    line = fp.readline()
    cnt = cntout2 = cntout3 = cntout4 = cntout5 = cntout6 = cntout7 = 0
    prevkey2 = '    '
    
    while line:
        line_len = len(line)
        if line_len < 10: 
            line = fp.readline()
            continue
            
        # 雙字詞處理 (10位)
        if line_len == 10:
            key1, key2 = line[7], line[8]
            val1, val2 = mydict.get(key1, 'xx'), mydict.get(key2, 'xx')
            val = (val1.rstrip() + val2.rstrip())
            
            # 格式化：補 z 或空格確保長度與對齊
            if len(val) == 3: val += ' '
            if len(val) == 2: val += 'z '
            
            lineout = f"{val}   {key1}{key2}\n"
            fo.write(lineout)
            if val == prevkey2: fd.write(line)
            prevkey2 = val
            cntout2 += 1

        # 三字詞處理 (11位)
        elif line_len == 11:
            key1, key2, key3 = line[7], line[8], line[9]
            val1, val2, val3 = mydict.get(key1, 'xx'), mydict.get(key2, 'xx'), mydict.get(key3, 'xx')
            # 邏輯：首字全碼(或首尾) + 後續字取首碼
            val = (val1.rstrip() + val2[0] + val3[0])
            if len(val) == 3: val += ' '
            fo.write(f"{val}   {key1}{key2}{key3}\n")
            cntout3 += 1

        # 四字及以上處理
        elif line_len >= 12:
            key1 = line[7]
            val1 = mydict.get(key1, 'xx')
            temp_val = val1.rstrip()
            for i in range(8, line_len - 1):
                temp_val += mydict.get(line[i], 'xx')[0]
            val = temp_val[:6].ljust(6) # 限制最長 6 位
            fo.write(f"{val}  {line[7:]}")
            cntout4 += 1

        line = fp.readline()
        cnt += 1

fo.close()
fd.close()
print(f"階段一完成：共處理 {cnt} 行，產出速成碼詞組。")

# =====================================================================
# 第二階段：詞頻注入與排序 (Frequency & Sorting)
# =====================================================================

dictpath = 'merge_ph2.txt'
filefreqmerge = 'reneeyu_ph2345out_freqmerge.txt'
mergedict = {}

# 1. 載入詞頻
with codecs.open(dictpath, 'r', 'utf-16') as f:
    for line in f:
        mergedict[line[7:9]] = line[0:6].rstrip()

# 2. 注入排序標記
with open(fileout, 'r', encoding='utf-16') as fp, \
     open(filefreqmerge, 'w', encoding='utf-16') as fom:
    for line in fp:
        word = line.strip().split()[-1]
        freq = mergedict.get(word[:2], '188888')
        # 標籤格式：長度(02) + 編碼(6位) + 詞頻(6位)
        prefix = f"{len(word):02d}"
        fom.write(f"{prefix}{line[0:6]}{freq}{line[7:]}")

# 3. 排序文件
with open(filefreqmerge, 'r+', encoding="utf-16") as f:
    lines = f.readlines()
    lines.sort()
    f.seek(0)
    f.truncate()
    f.write(''.join(lines))

print(f"階段二完成：詞頻排序成功。")

# =====================================================================
# 第三階段：清理標籤與合併最終文件
# =====================================================================

file_final_ph = 'reneeyu_ph2345ori.txt'
filetxt = 'reneeyu.txt' # 最終合併大檔

# 1. 還原格式
with open(filefreqmerge, 'r', encoding='utf-16') as fp, \
     open(file_final_ph, 'w', encoding='utf-16') as fo:
    for line in fp:
        fo.write(f"{line[2:8]} {line[14:]}")

# 2. 合併所有詞庫 (頭部、粵拼、速成等)
filenames = ['reneeyu_head.txt', 'reneeyu_canph2345ori.txt', file_final_ph, 'reneeyu_ph2orixz.txt']
with open(filetxt, 'w', encoding='utf-16') as outfile:
    for fname in filenames:
        if os.path.exists(fname):
            with open(fname, 'r', encoding='utf-16') as infile:
                shutil.copyfileobj(infile, outfile)

# 清理暫存檔
for f in [fileout, filefreqmerge]:
    if os.path.exists(f): os.remove(f)

print(f"階段三完成：速成詞庫已更新，並合併至 {filetxt}。")

# =====================================================================
# 第四階段：雙字詞重碼分析 (Analysis)
# =====================================================================

print("\n--- 開始分析速成雙字詞重碼情況 ---")

code_map = {}
total_2char = 0

with open(file_final_ph, 'r', encoding='utf-16') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) < 2: continue
        code, word = parts[0], parts[1]
        if len(word) == 2:
            total_2char += 1
            if code not in code_map: code_map[code] = []
            code_map[code].append(word)

distinct_codes = len(code_map)
dup_codes_list = [c for c, w in code_map.items() if len(w) > 1]
dup_count = len(dup_codes_list)
unique_count = distinct_codes - dup_count
homonym_rate = (dup_count / distinct_codes * 100) if distinct_codes > 0 else 0

# 寫入重碼詳細清單
with open(filedup, 'w', encoding='utf-16') as fd:
    fd.write(f"【速成雙字詞重碼報告】\n1. 雙字詞總數：{total_2char}\n")
    fd.write(f"2. 使用獨立編碼數：{distinct_codes}\n")
    fd.write(f"3. 不重碼詞數：{unique_count}\n")
    fd.write(f"4. 發生重碼的編碼數：{dup_count}\n")
    fd.write(f"5. 速成重碼率：{homonym_rate:.2f}%\n" + "-"*30 + "\n")
    for c in dup_codes_list:
        fd.write(f"{c} {' '.join(code_map[c])}\n")

print(f"分析完成：")
print(f"1. 雙字詞總數：{total_2char}")
print(f"2. 使用的獨立編碼數：{distinct_codes}")
print(f"3. 不重碼的詞數：{unique_count}")
print(f"4. 發生重碼的編碼數：{dup_count}")
print(f"5. 雙字詞重碼率：{homonym_rate:.2f}%")
print(f"6. 詳細重碼清單已寫入：{filedup}")