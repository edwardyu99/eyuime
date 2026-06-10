'''
請寫一個 PYTHON merge_ph2.py 合拼附上的ph2rank.txt 和 merge_jieba.txt，輸出 merge_ph2.txt
000001 我們
000002 可以
000003 自己
消除重複的雙字詞，以ph2rank.txt為主
所有.TXT 皆為UTF-16
'''
import os
input_ph2 = 'jieba_1000.txt'      # 'ph2rank.txt'
input_jieba = 'merge_ph2old.txt'  # 'merge_jieba.txt'

def merge_files():
    seen_words = set()
    merged_words = []
    
    ph2_count = 0
    jieba_count = 0
    output_count = 0

    if os.path.exists(input_ph2):
        with open(input_ph2, 'r', encoding='utf-16') as f1:
            for line in f1:
                ph2_count += 1
                parts = line.strip().split()
                if len(parts) >= 2:
                    word = parts[1]
                    if len(word) == 2:  # 篩選雙字詞
                        if word not in seen_words:
                            seen_words.add(word)
                            merged_words.append(word)
                    else:
                        # 若非雙字詞也需保留但不去重，可在此處理。
                        # 依題意「消除重複的雙字詞」，此處預設僅提取並去重雙字詞
                        pass

    if os.path.exists(input_jieba):
        with open(input_jieba, 'r', encoding='utf-16') as f2:
            for line in f2:
                jieba_count += 1
                parts = line.strip().split()
                if len(parts) >= 2:
                    word = parts[1]
                    if len(word) == 2:  # 篩選雙字詞
                        if word not in seen_words:
                            seen_words.add(word)
                            merged_words.append(word)

    with open('merge_ph2.txt', 'w', encoding='utf-16') as out_f:
        for i, word in enumerate(merged_words, 1):
            out_f.write(f"{i:06d} {word}\n")
            output_count += 1

    print(f"輸入檔: {input_ph2}     - 讀取行數: {ph2_count}")
    print(f"輸入檔: {input_jieba}   - 讀取行數: {jieba_count}")
    print(f"輸出檔: merge_ph2.txt   - 寫入行數: {output_count}")

if __name__ == '__main__':
    merge_files()