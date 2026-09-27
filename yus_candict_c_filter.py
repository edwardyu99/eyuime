def filter_and_sort_file(input_path, output_path):
    parsed_records = []
    total_lines = 0
    
    # 讀取輸入檔 (UTF-16 編碼)
    with open(input_path, 'r', encoding='utf-16') as f_in:
        for line in f_in:
            total_lines += 1
            parts = line.split()
            
            # 確保欄位至少包含 code, char, tone (至少 3 個欄位)
            if len(parts) < 3:
                continue
            
            code = parts[0]
            char = parts[1]
            vowel = code[1:3]
            tone = int(parts[2])
            # 若包含 rank 欄位，轉換為整數以進行數值排序；若無則設為 9999
            rank = int(parts[3]) if len(parts) >= 4 else 9999
#符合條件行數: 37 行  rank<=300 
#比變第地定電代對九見口去展在最流了來裏命面平世手受四小水體頭同為會有又然用
#符合條件行數: 110 行  重碼：3951
#比丙秉並變背貝呈錢才財采材第豆鬥地定典電吊代對兌否九究久夠救景竟見叫具巨系口后喜豈亥去祭走展召在眾最契企喬瞿賴黎麗流劉里吏另了來弄雷累裏裡呂某眉未命名面免夢每皮平片世手受死四小兆宋水歲垂體頭亭田台同為慧韋永會有又然言堯用
            if code[0] not in ['n'] and tone > 1 \
		and rank >= 1 and rank <= 300 and vowel in \
['ei','oi','in','ai','au','iu','ui','ig','ug']:
#            if code[0] not in ['n'] and tone == 4 \
#and rank >= 1 and rank <= 3000 and vowel in \
#['ey','oy','yn','ay','aw','iw','uy','yg','wg','ae','oe','ow','ew','uh','ng','mg']:
                try:
                    parsed_records.append({
                        'code': code,
                        'char': char,
                        'tone': tone,
                        'rank': rank,
                        'raw_line': line
                    })
                except ValueError:
                    # 若 tone 或 rank 非整數數字則跳過
                    continue

    # 1. 依序按 code (英文字母), tone (數字升冪), rank (數字升冪) 進行排序
    parsed_records.sort(key=lambda x: (x['code'], x['tone'], x['rank']))

    # 2. 針對相同的 code，只擷取第一個符合 tone > 1 的行
    matching_lines = []
    matching_chars = ""
    # seen_codes = set()
    
    for record in parsed_records:
        code = record['code']
        char = record['char']
        tone = record['tone']
        
        if tone > 1: # and code not in seen_codes:
            # seen_codes.add(code)
            matching_lines.append(record['raw_line'])
            matching_chars += char


    # 將符合條件的資料寫入 result.txt (保持 UTF-16 編碼)
    with open(output_path, 'w', encoding='utf-16') as f_out:
        f_out.writelines(matching_lines)
        f_out.writelines(matching_chars)


    # 顯示檔名與行數統計資訊
    match_count = len(matching_lines)
    print("=" * 35)
    print(f"輸入檔名: {input_path}")
    print(f"輸出檔名: {output_path}")
    print(f"總讀取行數: {total_lines} 行")
    print(f"符合條件行數: {match_count} 行")
    print(matching_chars)
    print("=" * 35)

    return matching_lines

# 使用示範
if __name__ == '__main__':
    input_file = 'yus_candict_c_tone_rank.txt'
    output_file = 'result.txt'

    # 執行排序、篩選並輸出至檔案
    results = filter_and_sort_file(input_file, output_file)