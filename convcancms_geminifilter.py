import codecs
import os
import sys
import platform
import datetime
from datetime import date

# =====================================================================
# 核心實驗參數設定區 (置頂方便您隨時修改測試)
# =====================================================================
MAX_NCHAR_PER_CODE = 4    # 每碼最多保留的詞數 (含首選與備選)
RANK_THRESHOLD = 60000 #50000 #55000 #150000 #80000     # 【自訂門檻】超出此詞頻順位的罕用備選詞會被淘汰

print(datetime.datetime.now())
print(f"Python {sys.version}")
print("Name of the operating system:", platform.system(), os.name)
print("\n=====================================================================")
print(f"啟動實驗方案確認：")
print(f"  👉 MAX_NCHAR_PER_CODE = {MAX_NCHAR_PER_CODE}")
print(f"  👉 RANK_THRESHOLD     = {RANK_THRESHOLD}")
print("=====================================================================\n")

# --- 定義全局文件名，防止 NameError ---
filepath = 'reneeyu_canph2345ori.txt'   # 這是您最原始的備份檔
fileout  = 'reneeyu_canph2345out.txt'   
filedup  = 'reneeyu_canph2345outdup.txt' 
keypath  = 'yus_candict_c.txt'          
dictpath = 'merge_ph2.txt'
ph2path  = 'merge_ph2.txt'       # <--- 雙字詞專用頻率表
filefreqmerge = 'reneeyu_canph2345out_freqmerge.txt'

# 產出獨立的最終檔案與淘汰檔案，防止覆蓋原始碼表
final_out = 'reneeyu_canph2345ori_final.txt'  

# 【已修改】：動態將參數代入檔名中，例如：reneeyu_canph2345_discard-3-65000.txt
filediscard = f'reneeyu_canph2345_discard-{MAX_NCHAR_PER_CODE}-{RANK_THRESHOLD}.txt' 

filemissing = 'missing_in_dict.txt'  # 缺字報告輸出路徑

# =====================================================================
# 第一階段：編碼轉換 (恢復原本邏輯，確保產生 ngomoo 等拼音碼)
# =====================================================================
mydict = {}
with codecs.open(keypath,'r','utf-16') as f:
    for line in f:
        if len(line) != 10:
            print(len(line))
            print(line)
            print(line[0])
            print(line[1])
            print(line[2])
            print(line[3])
            print(line[4])
            print(line[5])
            print(line[6])
            print(line[7])
            print(line[8])
        key = line[7]
        val = line[0]+line[1]+line[2]
        valdict = mydict.get(key,'???')
        if valdict == '???':
            mydict[key] = val
f.close()

if os.path.exists(filedup):
    os.remove(filedup)
fd = open(filedup,'a+', encoding='utf-16') 
if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
lineout = 'kungfu 功夫' 

missing_chars = {}

with open(filepath,'r', encoding='utf-16') as fp:  
    line = fp.readline()
    cnt = 0
    cntout2 = 0
    cntout3 = 0
    cntout4 = 0 
    cntout5 = 0 
    cntout6 = 0 
    cntout7 = 0 
    cnterr2 = 0
    cnterr3 = 0
    cnterr4 = 0 
    cnterr5 = 0 
    cntdup2 = 0
    prevkey2 = '    '
    while line:
        if len(line) <= 1:
            print(line, " skipped")
            line = fp.readline()
            cnt += 1
            continue
        if len(line) > 15 or len(line) < 10:
            print('**line no.=', cnt)
            print(len(line))
            print(line)
            print('**len < 10 or > 15, 7key + 4,5,6,7(utf-16)char + 1endline')
            print("*** error and exit !!!")  
            sys.exit(1)
       
        if len(line) == 10:
            key1 = line[7]
            key2 = line[8]
            val1 = mydict.get(key1, 'xxx')      
            val2 = mydict.get(key2, 'xxx')
          
            if val1 == 'xxx' or val2 == 'xxx':
                print(f"*** 雙字詞缺少鍵碼: {key1}{key2} → {line.strip()}")
                cnterr2 += 1
                word = line[7:].strip()
                for k, v in [(key1, val1), (key2, val2)]:
                    if v == 'xxx':
                        if k not in missing_chars:
                            missing_chars[k] = []
                        if word not in missing_chars[k]:
                            missing_chars[k].append(word)
                line = fp.readline()
                cnt += 1
                continue
             
            val = val1.rstrip() + val2.rstrip()
            if len(val) > 6:
                val = val[0]+val[1]+val[2]+val[3]+val[4]+val[5]

            if len(val)==5:
                val = val + ' '
            if len(val)==4:
                val = val + '  '
            if len(val)==3:
                val = val + '   '
            if len(val)==2:
                val = val + '    '
            lineout = val + ' ' +key1+key2
            fo.write(lineout+'\n')
            if cntout2 == 0:
                print('**convering canph2...')
            cntout2 += 1
            if val == prevkey2:
                fd.write(line)
                cntdup2 += 1
            prevkey2 = val

        if len(line) == 11:
            key1 = line[7]
            key2 = line[8]
            key3 = line[9]
            val1 = mydict.get(key1, 'xxxx')      
            val2 = mydict.get(key2, 'xxxx')
            val3 = mydict.get(key3, 'xxxx')
          
            if 'xxxx' in (val1, val2, val3):
                print(f"*** 三字詞缺少鍵碼: {key1}{key2}{key3} → {line.strip()}")
                cnterr3 += 1
                word = line[7:].strip()
                for k, v in [(key1, val1), (key2, val2), (key3, val3)]:
                    if v == 'xxxx':
                        if k not in missing_chars:
                            missing_chars[k] = []
                        if word not in missing_chars[k]:
                            missing_chars[k].append(word)
                line = fp.readline()
                cnt += 1
                continue
          
            val = val1.rstrip() + val2[0] + val3[0]
            if len(val) > 6 or len(val) < 3:
                print(f'**三字詞長度異常: {len(val)} → {val}   {line.strip()}')
                cnterr3 += 1
                line = fp.readline()
                cnt += 1
                continue
          
            if len(val) == 5:
                val = val + ' '
            if len(val) == 4:
                val = val + '  '
            if len(val) == 3:
                val = val + '   '
          
            lineout = val + ' ' + key1 + key2 + key3
            fo.write(lineout + '\n')
            if cntout3 == 0:
                print('**convering canph3...')
            cntout3 += 1
       
        if len(line) == 12:
            key1 = line[7]
            key2 = line[8]
            key3 = line[9]
            key4 = line[10]
            val1 = mydict.get(key1, 'xxxx')      
            val2 = mydict.get(key2, 'xxxx')
            val3 = mydict.get(key3, 'xxxx')
            val4 = mydict.get(key4, 'xxxx')
          
            if 'xxxx' in (val1, val2, val3, val4):
                print(f"*** 四字詞缺少鍵碼: {key1}{key2}{key3}{key4} → {line.strip()}")
                cnterr4 += 1
                word = line[7:].strip()
                for k, v in [(key1, val1), (key2, val2), (key3, val3), (key4, val4)]:
                    if v == 'xxxx':
                        if k not in missing_chars:
                            missing_chars[k] = []
                        if word not in missing_chars[k]:
                            missing_chars[k].append(word)
                line = fp.readline()
                cnt += 1
                continue
             
            val = val1.rstrip() + val2[0] + val3[0] + val4[0]
            if len(val) > 7 or len(val) < 4:
                print('**lenval not 5,6,7')
                print(line[99])
            if len(val) == 7:
                val = val[0]+val[1]+val[2]+val[3]+val[4]+val[5]
            if len(val) == 5:
                val = val + ' '
            if len(val) == 4:
                val = val + '  '

            lineout = val + ' ' +key1+key2+key3+key4
            fo.write(lineout+'\n')
            if cntout4 == 0:
                print('**convering canph4...')
            cntout4 += 1

        if len(line) < 13:
            line = fp.readline()
            cnt += 1
            continue
       
        if len(line) >= 13:
            key1 = line[7]
            key2 = line[8]
            key3 = line[9]
            key4 = line[10]
            key5 = line[11]
            val1 = mydict.get(key1, 'xxxx')      
            val2 = mydict.get(key2, 'xxxx')
            val3 = mydict.get(key3, 'xxxx')
            val4 = mydict.get(key4, 'xxxx')
            val5 = mydict.get(key5, 'xxxx')
          
            if 'xxxx' in (val1, val2, val3, val4, val5):
                print(f"*** 多字詞缺少鍵碼: {line[7:].strip()}")
                cnterr5 += 1
                word = line[7:].strip()
                for k, v in [(key1, val1), (key2, val2), (key3, val3), (key4, val4), (key5, val5)]:
                    if v == 'xxxx':
                        if k not in missing_chars:
                            missing_chars[k] = []
                        if word not in missing_chars[k]:
                            missing_chars[k].append(word)
                line = fp.readline()
                cnt += 1
                continue
             
            val = val1.rstrip() + val2[0] + val3[0] + val4[0] + val5[0]
            if len(val) > 8 or len(val) < 5:
                print(line[99])
            val = val[0:6]        
            lineout = val + ' ' + line[7:]
            fo.write(lineout)
            if cntout5 == 0:
                print('**converting canph5...')
            if len(line) == 13:
                cntout5 += 1
            else:
                if cntout6 == 0:
                    print('**converting canph6,7...')
                if len(line) == 14:
                    cntout6 += 1
                else:
                    cntout7 += 1

        line = fp.readline()
        cnt += 1
fp.close()
fo.close()
fd.close()

if os.path.exists(filemissing):
    os.remove(filemissing)
if missing_chars:
    with codecs.open(filemissing, 'w', 'utf-16') as fm:
        fm.write(f"【字頭字典缺字分析報告】\n")
        fm.write(f"共發現 {len(missing_chars)} 個未登錄於 {keypath} 的漢字：\n")
        fm.write("-" * 50 + "\n")
        for char, words in sorted(missing_chars.items()):
            fm.write(f"缺字：【{char}】\t→ 出現於詞組：{'、'.join(words)}\n")
    print(f"分析完成：詳細缺字清單已寫入：{filemissing}")

cntout = cntout2+cntout3+cntout4+cntout5+cntout6+cntout7
print('cnt=', cnt, ',cntout=', cntout)
print('cntout2=', cntout2, ',cnterr2=', cnterr2, ' cntdup2=', cntdup2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
print('cntout5=', cntout5, ',cnterr5=', cnterr5)
print('cntout6=', cntout6)
print('cntout7=', cntout7)
print(filepath,'convert to', fileout, 'OK')
print(f"階段一完成：共處理 {cnt} 行，輸出 {cntout} 個詞組。")

# =====================================================================
# 第二階段：詞頻合併與排序 (在此處載入 merge_ph2.txt)
# =====================================================================
mergedict = {}
if os.path.exists(ph2path):
    with codecs.open(ph2path, 'r', 'utf-16') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                freq, word = parts[0], parts[1]
                mergedict[word] = freq.zfill(6)

with open(fileout, 'r', encoding='utf-16') as fp, \
     open(filefreqmerge, 'w', encoding='utf-16') as fom:
    for line in fp:
        word = line.strip().split()[-1]
        freq = mergedict.get(word[:2], '108888')
        prefix = f"{len(word):02d}"
        fom.write(f"{prefix}{' '}{line[0:6]}{' '}{freq}{line[7:]}")

with open(filefreqmerge, 'r+', encoding="utf-16") as f:
    lines = f.readlines()
    lines.sort()
    f.seek(0)
    f.truncate()
    f.write(''.join(lines))
print(f"階段二完成：詞頻合併與排序成功。")

# =====================================================================
# 第三階段：格式化與清理 - sort_remove_dup  filefreqmerge
# =====================================================================
with open(fileout, 'r', encoding='utf-16') as fp, \
     open(filefreqmerge, 'w', encoding='utf-16') as fom:
    prev_line = ""
    for line in fp:
        if line == prev_line: continue
        word = line.strip().split()[-1]
        prefix = f"{len(word):02d}"
        if prefix == "04":
            freq1 = mergedict.get(word[:2], '108888')
            freq2 = mergedict.get(word[2:4], '108888')
            freq4 = int(freq1)+int(freq2)
            freq = f"{freq4:06d}"
        else:
            freq = mergedict.get(word[:2], '108888')
        fom_line = f"{prefix} {line[0:6]} {freq} {line[7:]}"
        fom.write(fom_line)
        prev_line = line

file_path = filefreqmerge
with open(file_path, 'r', encoding='utf-16') as f:
    lines = f.readlines()

input_count = len(lines)
seen = {}
duplicates = {}
unique_lines = []

for line in lines:
    if line in seen:
        duplicates[line] = duplicates.get(line, 1) + 1
    else:
        seen[line] = True
        unique_lines.append(line)

unique_lines.sort()
output_count = len(unique_lines)

with open(file_path, 'w', encoding='utf-16') as f:
    f.writelines(unique_lines)

print(f"File         : {file_path}")
print(f"Input lines  : {input_count:,}")
print(f"Output lines : {output_count:,}")
print(f"Duplicates removed : {input_count - output_count:,}")

# =====================================================================
# 修改重點：動態過濾罕用備選詞 (採用全新高彈性 N 碼防漏邏輯，並同步導出淘汰清單)
# =====================================================================
with open(filefreqmerge, 'r', encoding='utf-16') as fp, \
     open(final_out, 'w', encoding='utf-16') as fom, \
     open(filediscard, 'w', encoding='utf-16') as fdisc: 
    
    fdisc.write("【被淘汰的雙字詞對照清單】\n")
    fdisc.write(f"過濾參數：MAX_NCHAR_PER_CODE = {MAX_NCHAR_PER_CODE}, RANK_THRESHOLD = {RANK_THRESHOLD}\n")
    fdisc.write("-" * 65 + "\n")
    
    prev_code = ""
    code_count = 0
    
    for line in fp:
        parts = line.strip().split()
        if len(parts) < 4: 
            continue
            
        prefix = parts[0]         
        current_code = parts[1]   
        current_freq_str = parts[2] 
        
        try:
            current_freq = int(current_freq_str)
        except ValueError:
            current_freq = 108888
        
        if prefix == "02":
            if current_code == prev_code:
                code_count += 1
            else:
                prev_code = current_code
                code_count = 1
                
            # 條件 1：當重碼數大於 N，第 N+1 個詞以後無條件淘汰
            if code_count > MAX_NCHAR_PER_CODE:
                ## fdisc.write(f"{line[3:10]}{line[16:].strip()}\n")
                fdisc.write(f"{line[3:10]}{line[16:].strip()} \t# 原因: 超過最大同碼允許詞數 {MAX_NCHAR_PER_CODE} (同碼第 {code_count} 詞)\n")
                continue
                
            # 條件 2：如果是第 2 個詞（含）以後的備選詞，且詞頻順位大於門檻，淘汰
            if code_count >= 2 and current_freq > RANK_THRESHOLD:
                ## fdisc.write(f"{line[3:10]}{line[16:].strip()}\n")
                fdisc.write(f"{line[3:10]}{line[16:].strip()} \t# 原因: 詞頻順位 {current_freq} 超過門檻 {RANK_THRESHOLD} (同碼第 {code_count} 詞)\n")
                continue
        else:
            prev_code = ""
            code_count = 0
            
        fom_line = f"{line[3:9]}{line[16:]}"
        fom.write(fom_line)

print(f"階段三完成：最終碼表已動態過濾並更新至 {final_out}，被淘汰的雙字詞已輸出至 {filediscard}。")

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
        homonym_rate = (dup_codes_count / total_2char_count * 100)
        dup_2char_count = total_2char_count - unique_codes_count
        dup_2char_rate = ((dup_2char_count ) / total_2char_count * 100) 
    else:
        homonym_rate = 0
        dup_2char_count = 0
        dup_2char_rate = 0

    with open(filedup, 'w', encoding='utf-16') as fd:
        fd.write(f"【雙字詞重碼分析報告】\n")
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

# =====================================================================
# 第五階段：列出輸入與輸出的檔名和行數 (更新：加入動態行數更名)
# =====================================================================
print("\n=====================================================================")
print("執行總結：輸入與輸出檔案資訊")
print("=====================================================================")

def get_line_count(filename, default_encoding='utf-16'):
    if not os.path.exists(filename):
         return "N/A"
    try:
         with open(filename, 'r', encoding=default_encoding) as f:
              return sum(1 for _ in f)
    except Exception as e:
         return f"讀取錯誤"

# ---------------------------------------------------------------------
# 💡 【核心功能】自動將行數放入 final_out 檔名並進行 RENAME
# ---------------------------------------------------------------------
# 1. 先取得當前 final_out 的總行數
final_lines = get_line_count(final_out)

# 2. 確保有成功讀取到行數（非 N/A 或讀取錯誤）才進行更名
if isinstance(final_lines, int):
    # 動態產生帶有行數的新檔名 (例如: reneeyu_canph2345ori_final_128851.txt)
    final_renamed = f'reneeyu_canph2345ori_{MAX_NCHAR_PER_CODE}_{RANK_THRESHOLD}_final_{final_lines}.txt'
    
    try:
        # Windows 系統限制：如果新檔名已存在，rename 會報錯，所以先檢查並刪除舊檔
        if os.path.exists(final_renamed):
            os.remove(final_renamed)
            
        # 執行更名動作
        os.rename(final_out, final_renamed)
        
        # ⚡ 關鍵：將變數名稱指向新檔名，這樣下方印出的總結報告才會同步更新！
        final_out = final_renamed
        print(f"📢 成功將最終檔案更名為: {final_out}")
        
    except Exception as e:
        print(f"❌ 更名失敗，錯誤原因: {e}")
else:
    print("⚠️ 無法取得最終檔案行數，取消更名作業。")
# ---------------------------------------------------------------------


# --- 明確輸出當前執行時使用的實驗參數 ---
print("\n[當前執行參數設定]")
print(f"  ★ 最大同碼允許詞數 (MAX_NCHAR_PER_CODE) : {MAX_NCHAR_PER_CODE} 碼")
print(f"  ★ 罕用詞淘汰詞頻門檻 (RANK_THRESHOLD)   : {RANK_THRESHOLD} 名")
print("-" * 69)

print("[輸入檔案]")
print(f"  • {keypath:<30} : {get_line_count(keypath):>8} 行 (編碼字典)")
print(f"  • {ph2path:<30} : {get_line_count(ph2path):>8} 行 (雙字詞頻率表)")
print(f"  • {filepath:<30} : {cnt:>8} 行 (原始大碼表)")

print("\n[輸出檔案]")
# 這裡會因為上面 final_out 變數被更新了，自動印出帶數字的新檔名
print(f"  • {final_out:<30} : {get_line_count(final_out):>8} 行 (最終篩選碼表)") 
print(f"  • {filediscard:<30} : {get_line_count(filediscard):>8} 行 (已淘汰雙字詞清單)")
print(f"  • {filedup:<30} : {get_line_count(filedup):>8} 行 (重碼分析報告)")
if os.path.exists(filemissing):
    print(f"  • {filemissing:<30} : {get_line_count(filemissing):>8} 行 (缺字分析報告)")

print("\n[暫存檔案 (保留供 Debug)]")
print(f"  • {fileout:<30} : {get_line_count(fileout):>8} 行")
print(f"  • {filefreqmerge:<30} : {get_line_count(filefreqmerge):>8} 行")
print("=====================================================================\n")

