import re

def find_duplicate_entries(input_file, output_file):
    """
    讀取碼表檔案，找出所有重碼的雙字詞條目，並輸出到指定檔案
    支援 UTF-16 編碼的輸入和輸出
    """
    # 用字典存儲每個輸入碼對應的詞語列表
    code_dict = {}
    
    # 使用 UTF-16 編碼讀取檔案
    with open(input_file, 'r', encoding='utf-16') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # 分割輸入碼和詞語（用空格或製表符分隔）
            parts = re.split(r'\s+', line)
            if len(parts) >= 2:
                code = parts[0]
                word = ' '.join(parts[1:])
                
                # 只處理雙字詞（長度為2的中文詞語）
                if len(word) == 2:
                    if code not in code_dict:
                        code_dict[code] = []
                    code_dict[code].append(word)
    
    # 找出重碼的條目（同一輸入碼對應多個雙字詞）
    duplicates = {}
    for code, words in code_dict.items():
        # 去除重複的詞語
        unique_words = list(set(words))
        if len(unique_words) > 1:
            duplicates[code] = unique_words
    
    # 使用 UTF-16 編碼輸出結果
    with open(output_file, 'w', encoding='utf-16') as f:
        # 寫入 BOM (Byte Order Mark)
        f.write('\ufeff')
        # 按輸入碼排序
        for code in sorted(duplicates.keys()):
            words = duplicates[code]
            # 將重碼的詞語放在同一行，以空格分隔
            line = f"{code}\t{' '.join(words)}"
            f.write(line + '\n')
    
    print(f"處理完成！")
    print(f"共找到 {len(duplicates)} 組重碼雙字詞")
    print(f"結果已輸出到 {output_file}")

# 主程式
input_file = 'reneeyu_canph2345ori.txt'
output_file = 'reneeyu_canphdup.txt'

find_duplicate_entries(input_file, output_file)