import collections
import os
import argparse

# 初始化雙向字典
code_to_chars = collections.defaultdict(list)
char_to_codes = collections.defaultdict(list)

# 設定余氏輸入法對照表檔案名稱
candict_filename = "yus_candict_c.txt"

# 讀取外部 UTF-16 對照表並解析數據
if os.path.exists(candict_filename):
    with open(candict_filename, "r", encoding="utf-16") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 2:
                code = parts[0].strip()
                char = parts[1].strip()
                
                # 建立雙向映射關係
                if char not in code_to_chars[code]:
                    code_to_chars[code].append(char)
                if code not in char_to_codes[char]:
                    char_to_codes[char].append(code)
else:
    print(f"錯誤：找不到編碼表檔案 {candict_filename}，請確保該檔案與腳本放在相同目錄。")

def encode_string(text):
    """
    將漢字字串精確轉換為余氏輸入法編碼。
    如果一個漢字對應多個編碼，會返回第一個編碼的列表。
    若未收錄，則返回 "xxx"。
    """
    result = []
    for char in text:
        if char in char_to_codes:
            # 僅獲取第一個編碼並封裝成列表
            first_code = char_to_codes[char][0]
            result.append((char, [first_code]))
        else:
            result.append((char, ["xxx"]))
    return result

# --- 主要處理邏輯：解析參數並進行轉換 ---
if __name__ == "__main__":
    # 設定命令列參數解析器
    parser = argparse.ArgumentParser(description="余氏輸入法編碼批次轉換工具")
    
    # 加入 input_file 參數，nargs="?" 代表選填，並設定 default="hk_word.txt"
    parser.add_argument(
        "input_file", 
        nargs="?", 
        default="hk_word.txt", 
        help="輸入的對照文字檔案路徑 (預設: hk_word.txt)"
    )
    
    # 解析參數
    args = parser.parse_args()
    input_file = args.input_file
    output_file = input_file + "_yucode.txt"
    
    if os.path.exists(input_file):
        print(f"開始處理檔案：{input_file}...")
        convert_count = 0
        
        # 以 UTF-16 編碼開啟輸入與輸出檔案
        with open(input_file, "r", encoding="utf-16") as fin, \
             open(output_file, "w", encoding="utf-16") as fout:
            
            for line in fin:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    # 獲取第二欄的漢字
                    char = parts[1].strip()
                    
                    # 查表轉換為余氏輸入法編碼（精確獲取第一個編碼）
                    encoded = encode_string(char)
                    yucode = encoded[0][1][0]
                    
                    # 依照要求排版格式輸出（第一欄固定為 6 碼寬度，靠左對齊）
                    fout.write(f"{yucode:<6} {char}\n")
                    convert_count += 1
                    
        print(f"處理完成！已成功將 {convert_count} 個字轉換並寫入至：{output_file}")
    else:
        print(f"錯誤：找不到輸入檔案 '{input_file}'，請確認檔案路徑是否正確。")