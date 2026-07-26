from collections import Counter

def count_chars(filename):
    # 依序嘗試的編碼清單
    encodings = ['utf-8', 'utf-16']
    for enc in encodings:
        try:
            counter = Counter()
            with open(filename, encoding=enc) as f:
                for line in f:
                    line = line.strip()
                    # 跳過摘要行（數字開頭）與分隔線
                    if not line or line[0].isdigit() or line.startswith('--'):
                        continue
                    parts = line.split()
                    if len(parts) < 2:
                        continue
                    # parts[0] 是編碼，後面是該編碼下的所有雙字詞
                    for word in parts[1:]:
                        if len(word) == 2:
                            counter[word[0]] += 1
                            counter[word[1]] += 1
            return counter  # 成功則回傳結果
        except UnicodeDecodeError:
            continue  # 失敗則試下一個編碼
    raise ValueError("無法解碼檔案，請檢查編碼格式")

# 執行統計
counter = count_chars('reneeyu_canph2345outdup.txt')

# 印出前 50 個最高頻漢字
for char, freq in counter.most_common(50):
    print(f'{char}: {freq}')