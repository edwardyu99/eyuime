'''
請寫一個新的 PYTHON merge_ph1.py 合拼附上的cuhk_ch_rank.txt (utf-8 with header 和 ph1rank.txt，輸出 cuhk_ch_rank_merge.txt (格式同cuhk_ch_rank.txt )。消除重複的單字詞，以cuhk_ch_rank.txt為主
'''
import os

def merge_files():
    seen_chars = set()
    merged_chars = []
    
    cuhk_count = 0
    ph1_count = 0
    output_count = 0

    cuhk_filename = 'cuhk_ch_rank_7000.txt' # 根據你上傳的檔名
    ph1_filename = 'ph1rank.txt'
    output_filename = 'cuhk_ch_rank_merge.txt'

    # 1. 讀取並處理 cuhk_ch_rank_7000.txt (以這個為主)
    if os.path.exists(cuhk_filename):
        with open(cuhk_filename, 'r', encoding='utf-8') as f1:
            # 讀取第一行 header (ch,rank)
            header = f1.readline() 
            
            for line in f1:
                line = line.strip()
                if not line: continue
                
                parts = line.split(',')
                if len(parts) >= 1:
                    char = parts[0].strip()
                    # 確保是單字詞且尚未加入過
                    if len(char) == 1 and char not in seen_chars:
                        seen_chars.add(char)
                        merged_chars.append(char)
                        cuhk_count += 1

    # 2. 讀取並處理 ph1rank.txt
    if os.path.exists(ph1_filename):
        # 考慮到你之前提到 txt 可能為 UTF-16，這裡加入自動容錯處理
        try:
            f2 = open(ph1_filename, 'r', encoding='utf-16')
            f2.read(1) # 測試讀取
            f2.seek(0)
        except UnicodeError:
            f2 = open(ph1_filename, 'r', encoding='utf-8')
            
        with f2:
            for line in f2:
                parts = line.strip().split()
                if len(parts) >= 2:
                    char = parts[1].strip()
                    # 確保是單字詞且在 cuhk 中沒有出現過
                    if len(char) == 1 and char not in seen_chars:
                        seen_chars.add(char)
                        merged_chars.append(char)
                        ph1_count += 1

    # 3. 輸出至 cuhk_ch_rank_merge.txt (格式同 cuhk_ch_rank.txt)
    with open(output_filename, 'w', encoding='utf-8') as out_f:
        # 寫入 Header
        out_f.write("ch,rank\n")
        
        # 寫入合併後的單字，重新產生序號 (保持 4 位數格式，超過 9999 會自動延展)
        for i, char in enumerate(merged_chars, 1):
            out_f.write(f"{char},{i:04d}\n")
            output_count += 1

    # 顯示執行結果
    print(f"輸入檔: {cuhk_filename: <25} - 提取單字數: {cuhk_count}")
    print(f"輸入檔: {ph1_filename: <25} - 提取單字數: {ph1_count}")
    print(f"輸出檔: {output_filename: <25} - 寫入總行數: {output_count} (不含標題)")

if __name__ == '__main__':
    merge_files()