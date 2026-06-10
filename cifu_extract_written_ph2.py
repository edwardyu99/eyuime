import os

def extract_written_freq(input_filename, output_ph2):
    if not os.path.exists(input_filename):
        print(f"錯誤：找不到檔案 '{input_filename}'。")
        return

    word_freqs = []

    # 開啟 Cifu 格式化檔案
    with open(input_filename, 'r', encoding='utf-8') as f_in:
        # 1. 跳過第一行（標題列）
        f_in.readline()
        
        for line in f_in:
            line = line.strip()
            # 2. 跳過網格分隔線或空行
            if not line or line.startswith('-'):
                continue
            
            # 3. 使用 " | " 分割欄位
            parts = line.split('|')
            
            # 確保欄位數量足夠讀取到 Written 欄位 (index 7 是 Written per million)
            if len(parts) >= 8:
                word = parts[0].strip()
                
                # 4. 只提取「雙字詞」
                if len(word) == 2:
                    try:
                        # 提取第 8 個欄位：Written (per million tokens)
                        written_freq = float(parts[7].strip())
                        
                        # 5. 核心過濾：只保留在「書面語」語料中出現頻率大於 0 的詞
                        if written_freq > 0:
                            word_freqs.append((word, written_freq))
                    except ValueError:
                        continue

    # 6. 依照書面語頻率由大到小排序 (分數越高的排越前面)
    word_freqs.sort(key=lambda x: x[1], reverse=True)

    # 7. 將結果寫出為標準的 Rank 格式 (UTF-16)
    with open(output_ph2, 'w', encoding='utf-16') as f_out:
        for i, (word, freq) in enumerate(word_freqs):
            rank = i + 1
            f_out.write(f"{rank:06d} {word}\n")

    print(f"✅ 處理完成！共提取了 {len(word_freqs)} 個具備『書面語頻率』的雙字詞。")
    print(f"📄 專屬香港書面語的 Cifu 排名檔已匯出至 '{output_ph2}'。")

if __name__ == "__main__":
    INPUT_FILE = 'Cifu_formatted.txt'
    OUTPUT_PH2 = 'cifu_written_ph2rank.txt'
    
    extract_written_freq(INPUT_FILE, OUTPUT_PH2)