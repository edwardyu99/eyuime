import codecs
import sys
import os
from collections import Counter

def process_yucode(input_path):
    if not os.path.exists(input_path):
        print(f"錯誤：找不到檔案 {input_path}")
        return

    # 1. 建立聲調映射表 (從 jyutping.txt)
    tone_map = {}
    if os.path.exists('jyutping.txt'):
        with codecs.open('jyutping.txt', 'r', 'utf-8') as f:
            next(f)
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 6:
                    char, tone = parts[0], parts[5]
                    if char not in tone_map:
                        tone_map[char] = tone

    # 2. 建立排名映射表 (從 cuhk_ch_rank_7000i.txt)
    rank_map = {}
    if os.path.exists('cuhk_ch_rank_7000i.txt'):
        with codecs.open('cuhk_ch_rank_7000i.txt', 'r', 'utf-8') as f:
            next(f)
            for line in f:
                line = line.strip()
                if ',' in line:
                    char, rank = line.split(',')
                    rank_map[char] = rank.strip()

    # 定義 9 位聲調循環順序
    TONE_CYCLE = ["1", "2", "3", "4", "5", "6", "1", "2", "3"]

    def reorder_by_tone_cycle(pool, target_cycle):
        """
        在一個區塊（例如 9 個字）內按聲調循環排序
        """
        reordered = []
        temp_pool = list(pool)
        for target in target_cycle:
            if not temp_pool: break
            # 找尋該聲調中最常用的字
            match = next((x for x in temp_pool if x['tone'] == target), None)
            if match:
                reordered.append(match)
                temp_pool.remove(match)
            else:
                # 若無該聲調，補上剩餘中最常用的字
                match = temp_pool.pop(0)
                reordered.append(match)
        # 處理剩餘（理論上在此邏輯下 temp_pool 應為空，除非 pool > cycle 長度）
        if temp_pool:
            reordered.extend(temp_pool)
        return reordered

    # 3. 讀取輸入檔案
    raw_data = []
    codes_counter = Counter()

    with codecs.open(input_path, 'r', 'utf-16') as f_in:
        for line in f_in:
            line = line.strip()
            if not line: continue
            
            parts = line.split()
            if len(parts) >= 2:
                code, char = parts[0], parts[1]
                tone = tone_map.get(char, "9")
                rank = rank_map.get(char, "9999")
                
                raw_data.append({
                    'code': code,
                    'char': char,
                    'tone': tone,
                    'rank': int(rank)
                })
                codes_counter[code] += 1

    # 4. 執行分組循環排序邏輯 (每 9 個字一組)
    final_sorted_list = []
    unique_codes = sorted(codes_counter.keys())

    for c in unique_codes:
        # 該編碼所有字，先按字頻排序
        group = sorted([item for item in raw_data if item['code'] == c], key=lambda x: x['rank'])
        
        reordered_group = []
        # 以 9 為步長進行切片處理
        for i in range(0, len(group), 9):
            chunk = group[i : i + 9]
            # 對每一組（0-8, 9-17, 18-26...）分別套用循環邏輯
            reordered_chunk = reorder_by_tone_cycle(chunk, TONE_CYCLE[:len(chunk)])
            reordered_group.extend(reordered_chunk)
        
        final_sorted_list.extend(reordered_group)

    # 5. 輸出檔案
    base_name = os.path.splitext(input_path)[0]
    output_file = f"{base_name}_special.txt"
    output_file2 = f"{base_name}_special2.txt"

    with codecs.open(output_file, 'w', 'utf-16') as f_out, \
         codecs.open(output_file2, 'w', 'utf-16') as f_out2:
        for item in final_sorted_list:
            # special.txt: code(6位) + 1格 + 漢字 + 1格 + 聲調 + 1格 + 排名
            f_out.write(f"{item['code']:<6} {item['char']} {item['tone']} {item['rank']:04d}\n")
            # special2.txt: code(6位) + 1格 + 漢字
            f_out2.write(f"{item['code']:<6} {item['char']}\n")

    print(f"分組循環排序完成！")
    print(f"邏輯：每 9 個字為一組，內部獨立執行 (1,2,3,4,5,6,1,2,3) 聲調排序。")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法：python yus_sort_code_special.py yus_candict_c.txt")
    else:
        process_yucode(sys.argv[1])