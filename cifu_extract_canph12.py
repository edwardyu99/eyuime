import os

def process_file(input_filename, output_ph1, output_ph2):
    # 確認輸入檔案是否存在
    if not os.path.exists(input_filename):
        print(f"錯誤：找不到檔案 '{input_filename}'。")
        return

    # 分別為單字詞與雙字詞設定獨立的 RANK 計數器
    rank_ph1 = 1
    rank_ph2 = 1

    # 同時開啟原始檔（讀取）與兩個輸出檔（寫入，指定為 UTF-16 編碼）
    with open(input_filename, 'r', encoding='utf-8') as f_in, \
         open(output_ph1, 'w', encoding='utf-16') as f_out1, \
         open(output_ph2, 'w', encoding='utf-16') as f_out2:
        
        # 1. 讀取並跳過第一行（標題列：Word | JyutPing | ...）
        f_in.readline()
        
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            
            # 2. 跳過第二行的網格分隔線（由減號 ------- 組成的行）
            if line.startswith('-'):
                continue
            
            # 3. 使用 " | " 分割欄位，提取第一個欄位（Word）
            parts = line.split('|')
            if len(parts) >= 1:
                # 使用 .strip() 清除字詞前後可能殘留的空白
                word = parts[0].strip()
                
                # 判斷是否為單字或雙字詞
                if len(word) == 1:
                    f_out1.write(f"{rank_ph1:06d} {word}\n")
                    rank_ph1 += 1
                    
                elif len(word) == 2:
                    f_out2.write(f"{rank_ph2:06d} {word}\n")
                    rank_ph2 += 1

    print(f"✅ 處理完成！")
    print(f"📄 粵語單字詞已匯出至 '{output_ph1}' (共提取 {rank_ph1 - 1} 個，UTF-16 編碼)。")
    print(f"📄 粵語雙字詞已匯出至 '{output_ph2}' (共提取 {rank_ph2 - 1} 個，UTF-16 編碼)。")

if __name__ == "__main__":
    INPUT_FILE = 'Cifu_formatted.txt'
    OUTPUT_PH1 = 'cifu_ph1freq.txt'
    OUTPUT_PH2 = 'cifu_ph2freq.txt'
    
    process_file(INPUT_FILE, OUTPUT_PH1, OUTPUT_PH2)