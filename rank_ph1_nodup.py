import os
import sys

def main():
    # 1. 檢查是否帶入輸入檔案參數
    if len(sys.argv) < 2:
        print("【使用說明】請在指令後方加上要處理的檔案名稱。")
        print("範例: python rank_ph1.py uh.txt")
        return

    input_file = sys.argv[1]
    
    # 自動動態生成輸出檔名 (例如: uh.txt -> uh_ranked.txt)
    file_name, file_ext = os.path.splitext(input_file)
    output_file = f"{file_name}_ranked{file_ext}"

    rank_dict = {}
    dict_file = 'cuhk_ch_rank_7000.txt'
    
    # 2. 讀取中文字排名字典 (UTF-8 編碼)
    try:
        with open(dict_file, 'r', encoding='utf-8') as f:
            header = f.readline() 
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) == 2:
                    char = parts[0].strip()
                    rank = int(parts[1].strip())
                    rank_dict[char] = rank
    except FileNotFoundError:
        print(f"錯誤：找不到字典檔案 {dict_file}")
        return

    # 3. 讀取輸入的資料檔案 (UTF-16 編碼)，記錄原始行數並過濾重複項
    lines = []
    seen_chars = set()
    raw_lines_count = 0  # 紀錄輸入檔案的原始總行數

    try:
        with open(input_file, 'r', encoding='utf-16') as f:
            for line in f:
                raw_lines_count += 1
                chinese_chars = line[6:].strip()
                if chinese_chars not in seen_chars:
                    seen_chars.add(chinese_chars)
                    lines.append(line)
    except FileNotFoundError:
        print(f"錯誤：找不到輸入檔案 {input_file}")
        return

    # 4. 定義排序規則
    def sort_key(line):
        code = line[:6]
        chinese_chars = line[6:].strip()
        char_ranks = [rank_dict.get(c, 999999) for c in chinese_chars]
        return (code, char_ranks)

    # 5. 執行排序
    sorted_lines = sorted(lines, key=sort_key)

    # 6. 輸出至新的檔案 (UTF-16 編碼)
    with open(output_file, 'w', encoding='utf-16') as f:
        f.writelines(sorted_lines)
        
    # 7. 統計與結果列印
    print("\n" + "="*30)
    print(" 檔案排序執行成功！")
    print("="*30)
    print(f" * 輸入檔案: {input_file:<15} | 原始總行數: {raw_lines_count}")
    print(f" * 輸出檔案: {output_file:<15} | 去重後總行數: {len(sorted_lines)}")
    print(f" * 已刪除重複行數: {raw_lines_count - len(sorted_lines)}")
    print("="*30 + "\n")

if __name__ == "__main__":
    main()