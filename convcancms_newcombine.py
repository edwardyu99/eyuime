import codecs
import os
import sys

freq_limit = 150000  # 100000
# --- 定義全局文件名 ---
filepath = 'reneeyu_canph2345ori.txt'   
fileout  = 'reneeyu_canph2345out.txt'   
filedup  = 'reneeyu_canph2345outdup.txt' 
keypath  = 'yus_candict_c.txt'          
dictpath = 'merge_jieba.txt'
filefreqmerge = 'reneeyu_canph2345out_freqmerge.txt'
final_out = 'reneeyu_canph2345ori.txt'
# 修改：輸出符合新規則的唯一碼表檔案名
final_unique_out = 'reneeyu_canph2345ori_unique.txt'

# =====================================================================
# 第一階段：編碼轉換 (維持不變)
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
        if line_len == 10: # 2字
            key1, key2 = line[7], line[8]
            val = (mydict.get(key1, 'xxx').rstrip() + mydict.get(key2, 'xxx').rstrip()).ljust(6)
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
# 第二階段：詞頻合併與排序 (維持不變)
# =====================================================================
mergedict = {}
with codecs.open(dictpath, 'r', 'utf-16') as f:
    for line in f:
        mergedict[line[7:9]] = line[0:6].rstrip()

with open(fileout, 'r', encoding='utf-16') as fp, \
     open(filefreqmerge, 'w', encoding='utf-16') as fom:
    for line in fp:
        word = line.strip().split()[-1]
        freq = mergedict.get(word[:2], '888888')
        prefix = f"{len(word):02d}"
        fom.write(f"{prefix}{line[0:6]}{freq}{line[7:]}")

with open(filefreqmerge, 'r+', encoding="utf-16") as f:
    lines = f.readlines()
    lines.sort()
    f.seek(0)
    f.truncate()
    f.write(''.join(lines))
print(f"階段二完成：詞頻合併與排序成功。")

# =====================================================================
# 第三階段：格式化與清理 (維持不變)
# =====================================================================
with open(filefreqmerge, 'r', encoding='utf-16') as fp, \
     open(final_out, 'w', encoding='utf-16') as fo:
    prev_line = ""
    for line in fp:
        if line == prev_line: continue
        fo.write(f"{line[2:8]} {line[14:]}")
        prev_line = line

for f in [fileout]:  # 保留 filefreqmerge 供後續 diff2 提取與過濾詞頻使用
    if os.path.exists(f): os.remove(f)
print(f"階段三完成：最終碼表已更新至 {final_out}，暫存檔已刪除。")

# =====================================================================
# 第四階段：雙字詞重碼分析 (維持不變)
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
    homonym_rate = (dup_codes_count / distinct_codes * 100) if distinct_codes > 0 else 0

    with open(filedup, 'w', encoding='utf-16') as fd:
        fd.write(f"【雙字詞重碼分析報告】\n")
        fd.write(f"1. 雙字詞總數：{total_2char_count}\n")
        fd.write(f"2. 使用的獨立編碼數：{distinct_codes}\n")
        fd.write(f"3. 不重碼的詞數：{unique_codes_count}\n")
        fd.write(f"4. 發生重碼的編碼數：{dup_codes_count}\n")
        fd.write(f"5. 雙字詞重碼率：{homonym_rate:.2f}%\n")
        print(f"1. 雙字詞總數：{total_2char_count}")
        print(f"2. 使用的獨立編碼數：{distinct_codes}")
        print(f"3. 不重碼的詞數：{unique_codes_count}")
        print(f"4. 發生重碼的編碼數：{dup_codes_count}")
        print(f"5. 雙字詞重碼率：{homonym_rate:.2f}%")
        fd.write("-" * 30 + "\n")
        for code in dup_codes_list:
            fd.write(f"{code} {' '.join(code_map[code])}\n")

    print(f"分析完成：詳細重碼清單已寫入：{filedup}")
    
    # =====================================================================
    # 第五階段：輸出 UNIQUE2.TXT (雙字詞去重，3字以上不變)
    # =====================================================================
    print(f"--- 正在生成唯一碼表 UNIQUE2.TXT (雙字詞去重，多字詞保留) ---")
    seen_2char_codes = set()
    
    with open(final_out, 'r', encoding='utf-16') as f_in, \
         open(final_unique_out, 'w', encoding='utf-16') as f_out:
        for line in f_in:
            parts = line.split()
            if not parts: continue
            code, word = parts[0], parts[1]
            
            if len(word) == 2:
                if code not in seen_2char_codes:
                    f_out.write(line)
                    seen_2char_codes.add(code)
            else:
                f_out.write(line)
                
    print(f"完成：新唯一碼表已寫入 {final_unique_out}")

else:
    print(f"錯誤：找不到最終碼表 {final_out}")


# =====================================================================
# 第六階段：diff2 處理 (過濾 詞頻 < 100000 且格式化為「編碼 詞組」)
# =====================================================================
# --- 定義輸入與輸出檔案名稱 ---
final_in = 'reneeyu_canph2345ori.txt'
final_unique_in = 'reneeyu_canph2345ori_unique.txt'
final_diff_out = 'reneeyu_canph2345ori_diff.txt'
final_diff88_out = 'reneeyu_canph2345ori_diff88.txt'


def count_lines(filename):
    """計算檔案的有效行數 (排除空白行)"""
    if not os.path.exists(filename):
        return 0
    count = 0
    with open(filename, 'r', encoding='utf-16') as f:
        for line in f:
            if line.strip():
                count += 1
    return count

def analyze_2char_homonym(filename):
    """即時統計總表中的雙字詞重碼率"""
    if not os.path.exists(filename):
        return 0.0
    
    code_map = {}
    with open(filename, 'r', encoding='utf-16') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2: continue
            code, word = parts[0], parts[1]
            if len(word) == 2:
                if code not in code_map: 
                    code_map[code] = []
                code_map[code].append(word)
                
    distinct_codes = len(code_map)
    dup_codes_count = sum(1 for w in code_map.values() if len(w) > 1)
    
    homonym_rate = (dup_codes_count / distinct_codes * 100) if distinct_codes > 0 else 0.0
    return homonym_rate

def generate_diff():
    if not os.path.exists(final_in):
        print(f"錯誤：找不到原始總表檔案 {final_in}")
        return
    if not os.path.exists(final_unique_in):
        print(f"錯誤：找不到唯一碼表檔案 {final_unique_in}")
        return
    if not os.path.exists(filefreqmerge):
        print(f"錯誤：找不到中間詞頻排序檔 {filefreqmerge}")
        return

    print(f"\n--- 開始提取雙字詞重碼字詞 (過濾詞頻 < {freq_limit} 且不帶詞頻) (Diff2) ---")

    # 1. 將新唯一碼表 (UNIQUE2.TXT) 的每行存入集合 (去除空白)
    unique_lines = set()
    with open(final_unique_in, 'r', encoding='utf-16') as f_unique:
        for line in f_unique:
            cleaned = line.strip()
            if cleaned:
                unique_lines.add(cleaned)

    # 2. 讀取原始總表與中間詞頻檔，精準比對並過濾詞頻
    # filefreqmerge 格式為: 02(字數)xxxxxx(編碼)123456(詞頻)詞組\n
    # 索引關係: line[2:8] 是編碼, line[8:14] 是詞頻, line[14:] 是詞組與換行
    with open(final_in, 'r', encoding='utf-16') as f_in, \
        open(filefreqmerge, 'r', encoding='utf-16') as f_fm, \
        open(final_diff_out, 'w', encoding='utf-16') as f_diff, \
        open(final_diff88_out, 'w', encoding='utf-16') as f_diff88:
        
        for line_in in f_in:
            line_fm = f_fm.readline()
            cleaned_in = line_in.strip()
            if not cleaned_in:
                continue
            
            # 如果這一行「不在」唯一碼表裡，代表它是被篩掉的雙字詞
            if cleaned_in not in unique_lines:
                try:
                    freq_val = int(line_fm[8:14].strip())
                except ValueError:
                    freq_val = 888888  # 若轉換失敗給予預設低頻值
                
                # 關鍵邏輯：只保留詞頻小於 100000 的詞組
                if freq_val < freq_limit: # 100000:
                    code = line_fm[2:8]
                    word = line_fm[14:].strip()
                    
                    # 輸出全新格式: 編碼 詞組 (不包含詞頻)
                    f_diff.write(f"{code} {word}\n")
                else:
                    # 輸出格式: 編碼 詞組 詞頻
                    code = line_fm[2:8]
                    word = line_fm[14:].strip()
                    f_diff88.write(f"{code} {word} {freq_val}\n")


    # 3. 提取工作完成後，清理留下來的中間詞頻暫存檔
    if os.path.exists(filefreqmerge):
        os.remove(filefreqmerge)
    print("比對與詞頻過濾完成，暫存檔已清除！\n")
    
    # 4. 計算並列出 Record Counts 與各項重碼率
    orig_cnt   = count_lines(final_in)
    unique_cnt = count_lines(final_unique_in)
    diff_cnt   = count_lines(final_diff_out)
    
    char2_dup_rate = analyze_2char_homonym(final_in)
    
    print("=" * 50)
    print(" 【 數 據 核 對 報 告 2 (Record Counts) 】")
    print("=" * 50)
    print(f" 輸入 - 原始總表數 (A) : {orig_cnt:6d} 筆紀錄 ({final_in})")
    print(f" 輸入 - 唯一碼表數 (B) : {unique_cnt:6d} 筆紀錄 ({final_unique_in})")
    print("-" * 50)
    print(f" 輸出 - 低頻差異重碼數 (C) : {diff_cnt:6d} 筆紀錄 ({final_diff_out}) (已過濾 詞頻 < {freq_limit})")
    print("-" * 50)
    print(" 【 重 碼 率 橫 向 對 比 】")
    print("-" * 50)
    print(f" 說明 - 由於輸出 (C) 已進行詞頻條件篩選，(A = B + C) 關係此處不適用。")
    print(f" 輸出 - 原始雙字詞編碼重碼率: {char2_dup_rate:.2f}% (符合第四階段指標)")
    print("=" * 50)

#if __name__ == "__main__":
generate_diff()
#----- combine unique + diff --------------------------------------------------------
#import os

# --- 定義輸入與輸出檔案名稱 ---
final_in = 'reneeyu_canph2345ori.txt'
final_unique_in = 'reneeyu_canph2345ori_unique.txt'
final_diff_in = 'reneeyu_canph2345ori_diff.txt'
# 新增：合併輸出檔案名稱
final_combine_out = 'reneeyu_canph2345ori_combine.txt'

def count_lines(filename):
    """計算檔案的有效行數 (排除空白行)"""
    if not os.path.exists(filename):
        return 0
    count = 0
    with open(filename, 'r', encoding='utf-16') as f:
        for line in f:
            if line.strip():
                count += 1
    return count

def analyze_2char_homonym(filename):
    """即時統計總表中的雙字詞重碼率，邏輯與原程式第四階段完全一致"""
    if not os.path.exists(filename):
        return 0.0
    
    code_map = {}
    with open(filename, 'r', encoding='utf-16') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2: continue
            code, word = parts[0], parts[1]
            if len(word) == 2:
                if code not in code_map: 
                    code_map[code] = []
                code_map[code].append(word)
                
    distinct_codes = len(code_map)
    dup_codes_count = sum(1 for w in code_map.values() if len(w) > 1)
    
    # 計算雙字詞重碼率 (發生重碼的編碼數 / 獨立編碼數)
    homonym_rate = (dup_codes_count / distinct_codes * 100) if distinct_codes > 0 else 0.0
    return homonym_rate

def combine_unique_diff():
    # 檢查輸入檔案是否存在
    if not os.path.exists(final_in):
        print(f"錯誤：找不到原始總表檔案 {final_in}")
        return
    if not os.path.exists(final_diff_in):
        print(f"錯誤：找不到差異碼表檔案 {final_diff_in}")
        return
    if not os.path.exists(final_unique_in):
        print(f"錯誤：找不到唯一碼表檔案 {final_unique_in}")
        return

    # =====================================================================
    # 新增：依字數邏輯合併產生 combine.txt
    # =====================================================================
    print("--- 開始整合雙字詞並生成合併碼表 (Combine) ---")
    
    # 用來存放所有要寫入 combine.txt 的行，格式為 (字詞長度, 原始行內容)
    combine_records = []
    
    # (1) 讀取唯一碼表的所有內容
    with open(final_unique_in, 'r', encoding='utf-16') as f_unique:
        for line in f_unique:
            parts = line.strip().split()
            if len(parts) < 2: continue
            word = parts[1]
            combine_records.append((len(word), line))
            
    # (2) 讀取差異碼表，但「只拿雙字詞」放入
    with open(final_diff_out, 'r', encoding='utf-16') as f_diff:
        for line in f_diff:
            parts = line.strip().split()
            if len(parts) < 2: continue
            word = parts[1]
            if len(word) == 2:  # 嚴格限制：只要雙字詞
                combine_records.append((len(word), line))
                
    # (3) 依字詞長度進行穩定排序 (Python 的 sort 是穩定的，會維持原有的編碼/詞頻順序)
    combine_records.sort(key=lambda x: x[0])
    
    # (4) 寫入全新的 combine.txt 檔案
    with open(final_combine_out, 'w', encoding='utf-16') as f_combine:
        for length, line in combine_records:
            f_combine.write(line)
            
    print(f"完成：已將差異表中的雙字詞精準插入，新檔案已寫入 {final_combine_out}\n")
    
    # 3. 計算並列出 Record Counts 與各項重碼率
    orig_cnt    = count_lines(final_in)
    unique_cnt  = count_lines(final_unique_in)
    diff_cnt    = count_lines(final_diff_in)
    combine_cnt = count_lines(final_combine_out)
    
    # 計算重碼率
    
    print("=" * 50)
    print(" 【 數 據 核 對 報 告 (Record Counts) 】")
    print("=" * 50)
    print(f" 輸入 - 原始總表數 (A) : {orig_cnt:6d} 筆紀錄 ({final_in})")
    print(f" 輸入 - 唯一碼表數 (B) : {unique_cnt:6d} 筆紀錄 ({final_unique_in})")
    print("-" * 50)
    print(f" 輸出 - 差異重碼數 (C) : {diff_cnt:6d} 筆紀錄 ({final_diff_in})")
    print(f" 輸出 - 特製合併數 (D) : {combine_cnt:6d} 筆紀錄 ({final_combine_out})")
    
    # 自動驗證
    #if orig_cnt == (unique_cnt + diff_cnt):
    #    print(" 驗證結果: 成功！ (A = B + C) 數據完全吻合。")
    #else:
    #    print(" 驗證結果: 警告！ 數據不吻合，請檢查檔案是否有手工修改或空白行問題。")
    #print("=" * 50)

combine_unique_diff()
