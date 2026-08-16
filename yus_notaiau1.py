import codecs

filein  = 'yus_candict_c_tone_rank.txt'
fileout = 'yus_candict_c_tone_rank_notaiau1.txt'

# 要保留的韻母（對應 code 的第 2-3 字母）
rhymes = ('ai','au','iu','ui','ei','in','oi','ak','ik','uk')

print(f'** 輸入: {filein}')
print(f'** 輸出: {fileout}')
print('** 條件:')
print('   1. 放棄 len(code)<3 的行')
print('   2. 假設韻母為 code[1:3]，不在保留列表則放棄')
print('   3. 每組 code 取第一行，若 tone=1 或 4 則整組放棄；否則只輸出第一行\n')

seen    = set()   # 已輸出的 code
skipped = set()   # 第一行 tone=1/4 而整組放棄的 code
out_lines = 0
dropped_short = 0
dropped_rhyme = 0

with codecs.open(filein, 'r', 'utf-16') as f_in, \
     codecs.open(fileout, 'w', 'utf-16') as f_out:

    for line in f_in:
        line = line.rstrip('\r\n')
        if not line:
            continue

        parts = line.split()
        if len(parts) < 3:
            continue

        code = parts[0]
        tone = parts[2]

        # 條件 1: 放棄 len(code) < 3 的行（無法取 code[1:3]）
        if len(code) < 3:
            dropped_short += 1
            continue

        # 條件 2: 直接取 code[1:3] 作為韻母判斷
        if code[1:3] not in rhymes:
            dropped_rhyme += 1
            continue

        # 此 code 已處理過（輸出或放棄），跳過後續同組行
        if code in seen or code in skipped:
            continue

        # 條件 3: 新 code 檢查第一行的 tone
        if tone in ('1', '4'):
            skipped.add(code)      # 整組放棄
        else:
            f_out.write(line + '\n')
            seen.add(code)
            out_lines += 1

print(f'放棄 len(code)<3 的行數: {dropped_short}')
print(f'放棄 code[1:3] 不符合的行數: {dropped_rhyme}')
print(f'共輸出 {out_lines} 行')
print(f'放棄 {len(skipped)} 組 (第一行 tone=1 或 4)')
print(f'檔案已儲存為: {fileout}')