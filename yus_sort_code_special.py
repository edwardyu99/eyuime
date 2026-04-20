import codecs
import sys
import os
from collections import Counter

def process_yucode(input_path):
    if not os.path.exists(input_path):
        print(f"錯誤：找不到檔案 {input_path}")
        return

    tone_file = 'jyutping.txt'
    rank_file = 'cuhk_ch_rank_7000i.txt'

    # 1. 建立聲調映射表
    tone_map = {}
    if os.path.exists(tone_file):
        with codecs.open(tone_file, 'r', 'utf-8') as f:
            next(f)
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 6:
                    char, tone = parts[0], parts[5]
                    if char not in tone_map:
                        tone_map[char] = tone

    # 2. 建立排名映射表
    rank_map = {}
    if os.path.exists(rank_file):
        with codecs.open(rank_file, 'r', 'utf-8') as f:
            next(f)
            for line in f:
                line = line.strip()
                if ',' in line:
                    char, rank = line.split(',')
                    rank_map[char] = rank.strip()

    # 定義 9 位聲調循環順序
    TONE_CYCLE = ["1", "2", "3", "4", "5", "6", "1", "2", "3"]

    def reorder_globally_by_cycle(all_items, target_cycle):
        reordered = []
        remaining_pool = list(all_items)
        
        while remaining_pool:
            current_cycle = target_cycle[:min(len(remaining_pool), 9)]
            for target_tone in current_cycle:
                match = next((x for x in remaining_pool if x['tone'] == target_tone), None)
                if match:
                    reordered.append(match)
                    remaining_pool.remove(match)
                elif remaining_pool:
                    fallback = remaining_pool.pop(0)
                    reordered.append(fallback)
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
                raw_data.append({'code': code, 'char': char, 'tone': tone, 'rank': int(rank)})
                codes_counter[code] += 1

    total_chars = len(raw_data)

    # 4. 執行排序
    final_sorted_list = []
    unique_codes = sorted(codes_counter.keys())

    for c in unique_codes:
        full_group = sorted([item for item in raw_data if item['code'] == c], key=lambda x: x['rank'])
        final_sorted_list.extend(reorder_globally_by_cycle(full_group, TONE_CYCLE))

    # 5. 輸出檔案
    base_name = os.path.splitext(input_path)[0]
    out_spec = f"{base_name}_special.txt"
    out_spec2 = f"{base_name}_special2.txt"

    with codecs.open(out_spec, 'w', 'utf-16') as f1, codecs.open(out_spec2, 'w', 'utf-16') as f2:
        for item in final_sorted_list:
            f1.write(f"{item['code']:<6} {item['char']} {item['tone']} {item['rank']:04d}\n")
            f2.write(f"{item['code']:<6} {item['char']}\n")

    # 輸出執行訊息
    print("-" * 50)
    print(f"TONE 表： {tone_file}")
    print(f"RANK 表： {rank_file}")
    print(f"輸入   (code char)                   : {input_path}  ({total_chars} 字)")
    print(f"輸出 1 (code char tone rank)：{out_spec}   ({len(final_sorted_list)} 字)")
    print(f"輸出 2 (簡潔版)：{out_spec2}")
    print(f"排序邏輯：全局跨組聲調掃描 (1,2,3,4,5,6,1,2,3) 循環")
    print("-" * 50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法：python yus_sort_code_special.py input.txt")
    else:
        process_yucode(sys.argv[1])