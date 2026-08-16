import codecs

filein  = 'yus_candict_c_tone_rank.txt'
fileout = 'yus_candict_c_tone_rank_not1.txt'

print(f'** 輸入: {filein}')
print(f'** 輸出: {fileout}')
print('** 條件:')
print('   1. 放棄 len(code)<3 的行')
print('   2. 放棄 code 第 3 字母為 "a c e h w y z" 或 第2字母="m n" 的行')
print('   3. 每組 code 取第一行，若 tone=1或4 則整組放棄；若 tone≠1,4 則只輸出第一行\n')

seen    = set()   # 已輸出的 code
skipped = set()   # 第一行 tone=1 而整組放棄的 code
out_lines = 0
dropped_short = 0
dropped_hz = 0

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

        # 條件 1: 放棄 len(code) < 3 的行
        if len(code) < 3:
            dropped_short += 1
            continue

        # 條件 2: 放棄 code 第 3 字母 (index 2) 為 "a c e h m w y z" 的行
               #  或第 2 字母 為 'n', 'm'
        if code[2] in ('a', 'c', 'e', 'h', 'm', 'w', 'y', 'z') or code[1] in ('m', 'n', 'w', 'y'):
            dropped_hz += 1
            continue

        # 此 code 已處理過（輸出或放棄），跳過後續同組行
        if code in seen or code in skipped:
            continue

        # 條件 3: 新 code 檢查第一行的 tone
        if tone in ['1', '4'] :
            skipped.add(code)      # 整組放棄
        else:
            f_out.write(line + '\n')
            seen.add(code)
            out_lines += 1

print(f'放棄 len(code)<3 的行數: {dropped_short}')
print(f'放棄 code[2]="a c e h m w y z" 或 code[1]="m n w y" 的行數: {dropped_hz}')
print(f'共輸出 {out_lines} 行')
print(f'放棄 {len(skipped)} 組 (第一行 tone=1, 4)')
print(f'檔案已儲存為: {fileout}')