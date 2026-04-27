import codecs

def process_lang_files():
    # 1. 讀取聲調資料 (jyutping.txt) - 預設為 UTF-8
    # 格式: CH \t UCODE \t JP \t INIT \t FINL \t TONE ...
    tone_map = {}
    try:
        with open('jyutping.txt', 'r', encoding='utf-8') as f:
            next(f)  # 跳過標題
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 6:
                    char = parts[0]
                    tone = parts[5]
                    # 若同一個字有多個讀音，只取第一個
                    if char not in tone_map:
                        tone_map[char] = tone
    except FileNotFoundError:
        print("找不到 jyutping.txt")
        return

    # 2. 讀取排名資料 (cuhk_ch_rank_7000i.txt) - 預設為 UTF-8
    # 格式: 漢字,排名
    rank_map = {}
    try:
        with open('cuhk_ch_rank_7000i.txt', 'r', encoding='utf-8') as f:
            next(f)  # 跳過標題
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    char = parts[0]
                    rank = parts[1].strip()
                    rank_map[char] = rank
    except FileNotFoundError:
        print("找不到 cuhk_ch_rank_7000i.txt")
        return

    # 3. 處理主檔案並格式化輸出 (reneeyu_head_az.txt) - UTF-16
    output_lines = []
    try:
        with codecs.open('reneeyu_head_az.txt', 'r', encoding='utf-16') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    code = parts[0]
                    char = parts[1]
                    
                    tone = tone_map.get(char, " ") # 若無聲調則留空
                    rank = rank_map.get(char, "9999")
                    
                    # 格式調整：
                    # code.ljust(6) 確保 CODE 欄位左對齊並佔 6 格
                    # 之後各欄位以一個空格分隔
                    formatted_line = f"{code.ljust(6)} {char} {tone} {rank}"
                    output_lines.append(formatted_line)
    except FileNotFoundError:
        print("找不到 reneeyu_head_az.txt")
        return

    # 4. 寫入結果檔案 - UTF-16
    with codecs.open('reneeyu_head_az_out.txt', 'w', encoding='utf-16') as f:
        for ol in output_lines:
            f.write(ol + "\r\n")

    print("處理完成！輸出檔案：reneeyu_head_az_out.txt (UTF-16)")

if __name__ == "__main__":
    process_lang_files()