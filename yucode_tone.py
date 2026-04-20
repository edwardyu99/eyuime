import codecs

# 1. 建立聲調映射表 (從 jyutping.txt)
tone_map = {}
with codecs.open('jyutping.txt', 'r', 'utf-8') as f:
    next(f)  # 跳過標題列
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >= 6:
            char = parts[0]
            tone = parts[5]
            if char not in tone_map:
                tone_map[char] = tone

# 2. 建立排名映射表 (從 cuhk_ch_rank_7000i.txt)
rank_map = {}
with codecs.open('cuhk_ch_rank_7000i.txt', 'r', 'utf-8') as f:
    next(f)  # 跳過標題列
    for line in f:
        line = line.strip()
        if ',' in line:
            char, rank = line.split(',')
            rank_map[char] = rank

# 3. 讀取原表並整合輸出
output_file = 'yus_candict_final.txt'
with codecs.open('yus_candict_c.txt', 'r', 'utf-16') as f_in, \
     codecs.open(output_file, 'w', 'utf-16') as f_out:
    
    for line in f_in:
        line = line.rstrip('\r\n')
        if not line:
            f_out.write('\n')
            continue
        
        parts = line.split()
        if len(parts) >= 2:
            code = parts[0]
            char = parts[1]
            
            tone = tone_map.get(char, "")
            rank = rank_map.get(char, "")
            
            # 以 Tab 分隔各列：編碼 漢字 聲調 排名
            f_out.write(f"{code}\t{char}\t{tone}\t{rank}\n")
        else:
            f_out.write(f"{line}\n")

print(f"處理完成，檔案已儲存為: {output_file}")