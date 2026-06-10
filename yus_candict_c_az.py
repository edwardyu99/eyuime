import codecs

def process_lang_files():
    # 1. 讀取聲調資料 (jyutping.txt) - 預設為 UTF-8
    tone_map = {}
    try:
        with open('jyutping.txt', 'r', encoding='utf-8') as f:
            next(f)
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 6:
                    char = parts[0]
                    tone = parts[5]
                    if char not in tone_map:
                        tone_map[char] = tone
    except FileNotFoundError:
        print("找不到 jyutping.txt")
        return

    # 2. 讀取排名資料 (cuhk_ch_rank_7000.txt)
    rank_map = {}
    try:
        with open('cuhk_ch_rank_7000.txt', 'r', encoding='utf-8') as f:
            next(f)
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    char = parts[0]
                    rank = parts[1].strip()
                    rank_map[char] = rank
    except FileNotFoundError:
        print("找不到 cuhk_ch_rank_7000.txt")
        return

    # 3. 處理主檔案
    entries = []
    try:
        with codecs.open('yus_candict_c.txt', 'r', encoding='utf-16') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    code = parts[0]
                    char = parts[1]
                    tone = tone_map.get(char, " ")
                    rank = rank_map.get(char, "9999")
                    entries.append((code, char, tone, rank))
    except FileNotFoundError:
        print("找不到 yus_candict_c.txt")
        return

    # 4. 排序：先按 code，再按 rank（轉成整數排序）
    entries.sort(key=lambda x: (x[0], int(x[3])))

    # 5. 格式化輸出
    output_lines = [f"{code.ljust(6)} {char} {tone} {rank}" for code, char, tone, rank in entries]

    # 6. 寫入結果檔案
    with codecs.open('yus_candict_c_az_out.txt', 'w', encoding='utf-16') as f:
        for ol in output_lines:
            f.write(ol + "\r\n")

    print("處理完成！輸出檔案：yus_candict_c_az_out.txt (UTF-16，已按 code 與 rank 排序)")

if __name__ == "__main__":
    process_lang_files()