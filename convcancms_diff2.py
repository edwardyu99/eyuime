import os

# --- 定義輸入與輸出檔案名稱 ---
final_in = 'reneeyu_canph2345ori.txt'
final_unique_in = 'reneeyu_canph2345ori_unique2.txt'
final_diff_out = 'reneeyu_canph2345ori_diff2.txt'

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

def generate_diff():
    # 檢查輸入檔案是否存在
    if not os.path.exists(final_in):
        print(f"錯誤：找不到原始總表檔案 {final_in}")
        return
    if not os.path.exists(final_unique_in):
        print(f"錯誤：找不到唯一碼表檔案 {final_unique_in}")
        return

    print("--- 開始比對並提取雙字詞重碼字詞 (Diff2) ---")

    # 1. 將新唯一碼表 (UNIQUE2.TXT) 的每一行讀入集合中
    unique_lines = set()
    with open(final_unique_in, 'r', encoding='utf-16') as f_unique:
        for line in f_unique:
            cleaned = line.strip()
            if cleaned:
                unique_lines.add(cleaned)

    # 2. 讀取原始總表，比對並找出不在唯一碼表中的資料
    with open(final_in, 'r', encoding='utf-16') as f_in, \
         open(final_diff_out, 'w', encoding='utf-16') as f_diff:
        
        for line in f_in:
            cleaned = line.strip()
            if not cleaned:
                continue
            
            # 如果這一行「不在」唯一碼表裡，代表它是重碼組中被篩掉的字詞
            # 由於 UNIQUE2.TXT 只篩了雙字詞，這裡提取出來的必定只有被篩掉的雙字詞
            if cleaned not in unique_lines:
                f_diff.write(line)

    print("比對完成！\n")
    
    # 3. 計算並列出 Record Counts 與各項重碼率
    orig_cnt   = count_lines(final_in)
    unique_cnt = count_lines(final_unique_in)
    diff_cnt   = count_lines(final_diff_out)
    
    # 計算重碼率
    overall_dup_rate = (diff_cnt / orig_cnt * 100) if orig_cnt > 0 else 0.0
    char2_dup_rate = analyze_2char_homonym(final_in)
    
    print("=" * 50)
    print(" 【 數 據 核 對 報 告 2 (Record Counts) 】")
    print("=" * 50)
    print(f" 輸入 - 原始總表數 (A) : {orig_cnt:6d} 筆紀錄 ({final_in})")
    print(f" 輸入 - 唯一碼表數 (B) : {unique_cnt:6d} 筆紀錄 ({final_unique_in})")
    print("-" * 50)
    print(f" 輸出 - 差異重碼數 (C) : {diff_cnt:6d} 筆紀錄 ({final_diff_out})")
    print("-" * 50)
    print(" 【 重 碼 率 橫 向 對 比 】")
    print("-" * 50)
    print(f" 輸出 - 全體詞組重碼率 : {overall_dup_rate:.2f}% (C / A 佔比)")
    print(f" 輸出 - 雙字詞編碼重碼率: {char2_dup_rate:.2f}% (符合第四階段指標)")
    print("=" * 50)
    
    # 自動驗證
    if orig_cnt == (unique_cnt + diff_cnt):
        print(" 驗證結果: 成功！ (A = B + C) 數據完全吻合。")
    else:
        print(" 驗證結果: 警告！ 數據不吻合，請檢查檔案是否有手工修改或空白行問題。")
    print("=" * 50)

if __name__ == "__main__":
    generate_diff()