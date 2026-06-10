import codecs
import os
import sys

# --- 定義全局文件名，防止 NameError ---
filepath = 'reneeyu_canph2345ori.txt'   
fileout  = 'reneeyu_canph2345out.txt'   
filedup  = 'reneeyu_canph2345outdup.txt' 
keypath  = 'yus_candict_c.txt'          
dictpath = 'merge_ph2.txt'
ph2path  = 'merge_ph2.txt'       # <--- 新增：雙字詞專用頻率表
filefreqmerge = 'reneeyu_canph2345out_freqmerge.txt'
final_out = 'reneeyu_canph2345ori.txt'

# =====================================================================
# 第一階段：編碼轉換 (恢復原本邏輯，確保產生 ngomoo 等拼音碼)
# =====================================================================
# ------------------
mydict = {}
with codecs.open(keypath,'r','utf-16') as f:
    for line in f:
        
        if len(line) != 10:
          print(len(line))
          print(line)
          print(line[0])
          print(line[1])
          print(line[2])
          print(line[3])
          print(line[4])
          print(line[5])
          print(line[6])
          print(line[7])
          print(line[8])
#          print(line[9]) #endline
        key = line[7]
        val = line[0]+line[1]+line[2] #20221207 +line[3]
#        print(key)
#        print(val) 
#        if len(val) != 4:
#           print(len)
#           print(val) 
# prevent duplicate key dict
        valdict = mydict.get(key,'???')
        if valdict == '???':
           mydict[key] = val
f.close()

if os.path.exists(filedup):
    os.remove(filedup)
fd = open(filedup,'a+', encoding='utf-16') 
if os.path.exists(fileout):
    os.remove(fileout)
fo = open(fileout,'a+', encoding='utf-16') 
lineout = 'kungfu 功夫' 
with open(filepath,'r', encoding='utf-16') as fp:  
   line = fp.readline()
   cnt = 0
   cntout = 0
   cntout2 = 0
   cntout3 = 0
   cntout4 = 0 
   cntout5 = 0 
   cntout6 = 0 
   cntout7 = 0 
   cnterr2 = 0
   cnterr3 = 0
   cnterr4 = 0 
   cnterr5 = 0 
   cntdup2 = 0
   prevkey2 = '   '
   while line:
       if len(line) <= 1:
          print(line, " skipped")
          line = fp.readline()
          cnt += 1
          continue
       if len(line) > 15 or len(line) < 10:
          print('**line no.=', cnt)
          print(len(line))
          print(line)
          print('**len < 10 or > 15, 7key + 4,5,6,7(utf-16)char + 1endline')
          print("*** error and exit !!!")  
          sys.exit(1)                    # Exit with error
#        
# 7key + 2(utf-16)char + lf = 10
       
       if len(line) == 10:
          key1 = line[7]
          key2 = line[8]
#       print(key1)
          val1 = mydict.get(key1, 'xxx')      
          val2 = mydict.get(key2, 'xxx')
          if val1 == 'xxx' or val2 == 'xxx':
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(line)
             cnterr2 += 1
          val = val1.rstrip() + val2.rstrip()
          if len(val) > 6:
             val = val[0]+val[1]+val[2]+val[3]+val[4]+val[5]

#         if val1 == 'n  ':
#             print(key1)
#             print(val1)
#             print(key2)
#             print(val2)
#             print(line)
#             print(val)
#             print(len(val))
#
#20221207 n=no
          if len(val)==5:
             val = val + ' '
          if len(val)==4:
             val = val + '  '
          if len(val)==3:
             val = val + '   '
          if len(val)==2:
             val = val + '    '
          lineout = val + ' ' +key1+key2
          fo.write(lineout+'\n')
          if cntout2 == 0:
             print('**convering canph2...')
          cntout2 += 1
# output dupkey2 to fd
          if val == prevkey2:
             fd.write(line)
             cntdup2 += 1
          prevkey2 = val
#
# 7key + 3(utf-16)char + lf = 11
# ==================== 【原三字詞處理區塊 - 已註解】 ====================
#       if len(line) == 11:
#          key1 = line[7]
#          key2 = line[8]
#          key3 = line[9]
#          val1 = mydict.get(key1, 'xxxx')      
#          val2 = mydict.get(key2, 'xxxx')
#          val3 = mydict.get(key3, 'xxxx')
#          if val1 == 'xxxx' or val2 == 'xxxx' or val3 == 'xxxx':
#             print(key1)
#             print(val1)
#             print(key2)
#             print(val2)
#             print(key3)
#             print(val3)
#             print(line)
#             cnterr3 += 1
#          val = val1.rstrip() + val2[0] + val3[0]
#          if len(val) > 6 or len(val) < 3:
#             print('**lenval not 4,5,6')
#             print(len(val))
#             print(val)
#             print(key1)
#             print(val1)
#             print(key2)
#             print(val2)
#             print(key3)
#             print(val3)
#             print(line)
#             print(line[99])
#          if len(val) == 5:
#             val = val + ' '
#          if len(val) == 4:
#             val = val + '  '
#          if len(val) == 3:
#             val = val + '   '
#          lineout = val + ' ' +key1+key2+key3
#          fo.write(lineout+'\n')
#          if cntout3 == 0:
#             print('**convering canph3...')         
#          cntout3 += 1

# ==================== 【新修正版 - 三字詞處理】 ====================
       if len(line) == 11:
          key1 = line[7]
          key2 = line[8]
          key3 = line[9]
          
          val1 = mydict.get(key1, 'xxxx')      
          val2 = mydict.get(key2, 'xxxx')
          val3 = mydict.get(key3, 'xxxx')
          
          if 'xxxx' in (val1, val2, val3):
             print(f"*** 三字詞缺少鍵碼: {key1}{key2}{key3} → {line.strip()}")
             cnterr3 += 1
             line = fp.readline()
             cnt += 1
             continue
          
          val = val1.rstrip() + val2[0] + val3[0]
          
          if len(val) > 6 or len(val) < 3:
             print(f'**三字詞長度異常: {len(val)} → {val}   {line.strip()}')
             cnterr3 += 1
             line = fp.readline()
             cnt += 1
             continue
          
          if len(val) == 5:
             val = val + ' '
          if len(val) == 4:
             val = val + '  '
          if len(val) == 3:
             val = val + '   '
          
          lineout = val + ' ' + key1 + key2 + key3
          fo.write(lineout + '\n')
          
          if cntout3 == 0:
             print('**convering canph3...')
          cntout3 += 1
#
# 7key + 4(utf-16)char + lf = 12
       
       if len(line) == 12:
          key1 = line[7]
          key2 = line[8]
          key3 = line[9]
          key4 = line[10]
#       print(key1)
          val1 = mydict.get(key1, 'xxxx')      
          val2 = mydict.get(key2, 'xxxx')
          val3 = mydict.get(key3, 'xxxx')
          val4 = mydict.get(key4, 'xxxx')
          if val1=='xxxx' or val2=='xxxx' or val3=='xxxx' or val4=='xxxx':
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(key3)
             print(val3)
             print(key4)
             print(val4)
             print(line)
             cnterr4 += 1
          val = val1.rstrip() + val2[0] + val3[0] + val4[0]
          if len(val) > 7 or len(val) < 4: #20221207  5:
             print('**lenval not 5,6,7')
             print(len(val))
             print(val)
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(key3)
             print(val3)
             print(line)
# abort by index
             print(line[99])
          if len(val) == 7:
             val = val[0]+val[1]+val[2]+val[3]+val[4]+val[5]
          if len(val) == 5:
             val = val + ' '
          if len(val) == 4:
             val = val + '  '

          lineout = val + ' ' +key1+key2+key3+key4
          fo.write(lineout+'\n')
          if cntout4 == 0:
             print('**convering canph4...')
          cntout4 += 1
#
#------------------
       if len(line) < 13:
          line = fp.readline()
          cnt += 1
          continue
# remaining lines are 5 or more chars phrases
                  
# 7key + 5(utf-16)char + lf = 13
       
       if len(line) >= 13:
          key1 = line[7]
          key2 = line[8]
          key3 = line[9]
          key4 = line[10]
          key5 = line[11]
#       print(key1)
          val1 = mydict.get(key1, 'xxxx')      
          val2 = mydict.get(key2, 'xxxx')
          val3 = mydict.get(key3, 'xxxx')
          val4 = mydict.get(key4, 'xxxx')
          val5 = mydict.get(key5, 'xxxx')
          if val1=='xxxx' or val2=='xxxx' or val3=='xxxx' or val4=='xxxx' or val5=='xxxx':
             print(key1)
             print(val1)
             print(key2)
             print(val2)
             print(key3)
             print(val3)
             print(key4)
             print(val4)
             print(key5)
             print(val5)
             print(line)
             cnterr5 += 1
          val = val1.rstrip() + val2[0] + val3[0] + val4[0] + val5[0]
          if len(val) > 8 or len(val) < 5: #20221207 6 :
             print('**lenval not 6,7,8')
#          abort by index 
             print(line[99])
#max 6chars           
          val = val[0:6]        
##          lineout = val + ' ' +key1+key2+key3+key4+key5
          lineout = val + ' ' + line[7:]
          fo.write(lineout)
#          fo.write(lineout+'\r\n')         
#          fo.write(lineout+'\n')
          if cntout5 == 0:
             print('**converting canph5...')
          if len(line) == 13:
             cntout5 += 1
          else:
             if cntout6 == 0:
                print('**converting canph6,7...')
             if len(line) == 14:
                cntout6 += 1
             else:
                cntout7 += 1

#------------------
       line = fp.readline()
       cnt += 1
fp.close()
fo.close()
fd.close()
cntout = cntout2+cntout3+cntout4+cntout5+cntout6+cntout7
print('cnt=', cnt, ',cntout=', cntout)
print('cntout2=', cntout2, ',cnterr2=', cnterr2, ' cntdup2=', cntdup2)
print('cntout3=', cntout3, ',cnterr3=', cnterr3)
print('cntout4=', cntout4, ',cnterr4=', cnterr4)
print('cntout5=', cntout5, ',cnterr5=', cnterr5)
print('cntout6=', cntout6)
print('cntout7=', cntout7)
print(filepath,'convert to', fileout, 'OK')
print(f"階段一完成：共處理 {cnt} 行，輸出 {cntout} 個詞組。")

#---------------------------------------------------------------------

# =====================================================================
# 第二階段：詞頻合併與排序 (在此處載入 merge_ph2.txt)
# =====================================================================
mergedict = {}

# 1. 讀取原本 merge_ph2.txt 的詞頻
#if os.path.exists(dictpath):
#    with codecs.open(dictpath, 'r', 'utf-16') as f:
#        for line in f:
#            if len(line) >= 9:
#                mergedict[line[7:9]] = line[0:6].rstrip()

# 2. 讀取 merge_ph2.txt 的雙字詞詞頻 (優先使用，會覆蓋上方的同名詞)
if os.path.exists(ph2path):
    with codecs.open(ph2path, 'r', 'utf-16') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                freq, word = parts[0], parts[1]
                mergedict[word] = freq.zfill(6) # 確保寫入是 000001 這樣的6碼

with open(fileout, 'r', encoding='utf-16') as fp, \
     open(filefreqmerge, 'w', encoding='utf-16') as fom:
    for line in fp:
        word = line.strip().split()[-1]
        freq = mergedict.get(word[:2], '888888')
        prefix = f"{len(word):02d}"
        # 此時 line[0:6] 為拼音碼(ngomoo)，freq 為從 merge_ph2 取到的頻率(000001)
        fom.write(f"{prefix}{' '}{line[0:6]}{' '}{freq}{line[7:]}")

with open(filefreqmerge, 'r+', encoding="utf-16") as f:
    lines = f.readlines()
    lines.sort()
    f.seek(0)
    f.truncate()
    f.write(''.join(lines))
print(f"階段二完成：詞頻合併與排序成功。")

# =====================================================================
# 第三階段：格式化與清理 - sort_remove_dup  filefreqmerge
# =====================================================================
with open(fileout, 'r', encoding='utf-16') as fp, \
     open(filefreqmerge, 'w', encoding='utf-16') as fom:
    prev_line = ""
    for line in fp:
        if line == prev_line: continue
        word = line.strip().split()[-1]
        prefix = f"{len(word):02d}"
        if prefix == "04":
            freq1 = mergedict.get(word[:2], '188888')   # 默认值改为 188888
            freq2 = mergedict.get(word[2:4], '188888')
            freq4 = int(freq1)+int(freq2)
            freq = f"{freq4:06d}"
        else:
            freq = mergedict.get(word[:2], '188888')   # 默认值改为 188888
        fom_line = f"{prefix} {line[0:6]} {freq} {line[7:]}"
        fom.write(fom_line)
        prev_line = line

# =====================================================================
# sort_remove_dup  filefreqmerge
# =====================================================================
file_path = filefreqmerge   # 'sample.txt'
# Read all lines
with open(file_path, 'r', encoding='utf-16') as f:
    lines = f.readlines()

input_count = len(lines)

# Track duplicates and keep first occurrence
seen = {}
duplicates = {}
unique_lines = []

for line in lines:
    if line in seen:
        duplicates[line] = duplicates.get(line, 1) + 1
    else:
        seen[line] = True
        unique_lines.append(line)

# Sort the unique lines
unique_lines.sort()

output_count = len(unique_lines)

# Write back to file
with open(file_path, 'w', encoding='utf-16') as f:
    f.writelines(unique_lines)

# === Report ===
print(f"File         : {file_path}")
print(f"Input lines  : {input_count:,}")
print(f"Output lines : {output_count:,}")
print(f"Duplicates removed : {input_count - output_count:,}")

if duplicates:
    print(f"\nDuplicated lines found ({len(duplicates)} unique duplicated lines):")
    for line, count in duplicates.items():
        clean_line = line.strip()
        display = clean_line[:77] + "..." if len(clean_line) > 80 else clean_line
        print(f"  • {display}  (appeared {count + 1} times)")
#else:
#    print("\nNo duplicates found.")

#debug_cnt = 0
# remove left 2 columns and middle 6 columns freq after sort
with open(filefreqmerge, 'r', encoding='utf-16') as fp, \
     open(final_out, 'w', encoding='utf-16') as fom:
    for line in fp:
        # 此時 line[3:9] 為拼音碼(ngomoo)，remove prefix and freq in middle
        fom_line = f"{line[3:9]}{line[16:]}"
        fom.write(fom_line)
        #if debug_cnt < 3:
        #    print(fom_line)  #debug
        #    debug_cnt += 1

# <--- 修改：註解掉這段以保留暫存檔 (Debug用) --->
# for f in [fileout, filefreqmerge]: 
#     if os.path.exists(f): os.remove(f)
print(f"階段三完成：最終碼表已更新至 {final_out}，暫存檔已保留供 Debug 使用。")

# =====================================================================
# 第四階段：雙字詞重碼分析
# =====================================================================
print("\n--- 開始分析雙字詞重碼情況 ---")

code_map = {}
total_2char_count = 0

if os.path.exists(final_out):
    with open(final_out, 'r', encoding='utf-16') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2: continue
            code, word = parts[0], parts[1]
            #if total_2char_count < 10:  #debug
            #    print(line)
            #    print(parts)
            #    print(len(parts), code, word)
            if len(word) == 2:
                total_2char_count += 1
                if code not in code_map: code_map[code] = []
                code_map[code].append(word)

    distinct_codes = len(code_map)
    dup_codes_list = [c for c, w in code_map.items() if len(w) > 1]
    dup_codes_count = len(dup_codes_list)
    unique_codes_count = distinct_codes - dup_codes_count 
    if total_2char_count > 0:
        homonym_rate = (dup_codes_count / total_2char_count * 100)
        dup_2char_count = total_2char_count - unique_codes_count
        dup_2char_rate = ((dup_2char_count ) / total_2char_count * 100) 
    else:
        homonym_rate = 0
        dup_2char_count = 0
        dup_2char_rate = 0

    with open(filedup, 'w', encoding='utf-16') as fd:
        fd.write(f"【雙字詞重碼分析報告】\n")
        fd.write(f"1. 雙字詞總數：{total_2char_count}\n")
        fd.write(f"2. 使用的獨立編碼數：{distinct_codes}\n")
        fd.write(f"3. 不重碼的雙字詞數：{unique_codes_count}\n")
        fd.write(f"4. 發生重碼的雙字詞數：{dup_2char_count}\n")
        fd.write(f"5. 雙字詞重碼率：{dup_2char_rate:.2f}%\n")
        fd.write(f"6. 雙字詞編碼數重碼率：{homonym_rate:.2f}%\n")
        fd.write("-" * 30 + "\n")
        for code in dup_codes_list:
            fd.write(f"{code} {' '.join(code_map[code])}\n")

    print(f"分析完成：")
    print(f"1. 雙字詞總數：{total_2char_count}")
    print(f"2. 使用的獨立編碼數：{distinct_codes}")
    print(f"3. 不重碼的雙字詞數：{unique_codes_count}")
    print(f"4. 發生重碼的雙字詞數：{dup_2char_count}")
    print(f"5. 雙字詞重碼率：{dup_2char_rate:.2f}%")
    print(f"6. 雙字詞編碼數重碼率：{homonym_rate:.2f}%")

    print(f"   詳細重碼清單已寫入：{filedup}")
else:
    print(f"錯誤：找不到最終碼表 {final_out}")