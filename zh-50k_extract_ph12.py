import opencc
import os

def process_file(input_filename, output_ph1, output_ph2):
    # 初始化 OpenCC 轉換器 (s2t.json：簡體轉繁體)
    converter = opencc.OpenCC('s2t.json')

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
        
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            
            # 使用空白分割字串，提取詞彙
            parts = line.split()
            if len(parts) >= 1:
                word = parts[0]
                
                # 判斷是否為單字或雙字詞
                if len(word) == 1 or len(word) == 2:
                    # 統一將簡體字轉換為繁體字
                    trad_word = converter.convert(word)
                    
                    # 若為單字詞，寫入 ph1rank.txt 並更新其 RANK
                    if len(word) == 1:
                        f_out1.write(f"{rank_ph1:06d} {trad_word}\n")
                        rank_ph1 += 1
                        
                    # 若為雙字詞，寫入 ph2rank.txt 並更新其 RANK
                    elif len(word) == 2:
                        f_out2.write(f"{rank_ph2:06d} {trad_word}\n")
                        rank_ph2 += 1

    print(f"✅ 處理完成！")
    print(f"📄 單字詞檔案已匯出至 '{output_ph1}' (共提取 {rank_ph1 - 1} 個，UTF-16 編碼)。")
    print(f"📄 雙字詞檔案已匯出至 '{output_ph2}' (共提取 {rank_ph2 - 1} 個，UTF-16 編碼)。")

if __name__ == "__main__":
    INPUT_FILE = 'zh-50k.txt'
    OUTPUT_PH1 = 'zh-50k_ph1freq.txt'
    OUTPUT_PH2 = 'zh-50k_ph2freq.txt'
    
    process_file(INPUT_FILE, OUTPUT_PH1, OUTPUT_PH2)