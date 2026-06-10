import os
import re

# 檔案路徑設定
char_rank_file = "cuhk_ch_rank_7000.txt"
# phrase_file = "reneeyu_canph2345ori_extra_100000.txt"
phrase_file = "reranked_2char_phrases.txt"
output_file = "reranked_2char_phrases.txt"

# 1. 讀取單字排名數據（以 UTF-8 讀取）
char_ranks = {}
char_rank_lines = 0

if os.path.exists(char_rank_file):
    with open(char_rank_file, "r", encoding="utf-8") as f:
        # 讀取第一行（標頭）
        header = f.readline()
        if header:
            char_rank_lines += 1

        for line in f:
            char_rank_lines += 1
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) == 2:
                char = parts[0].strip()
                try:
                    char_ranks[char] = int(parts[1].strip())
                except ValueError:
                    continue
else:
    print(f"錯誤：找不到檔案 {char_rank_file}")

# 2. 處理並計算 2 字詞的權重（以 UTF-16 讀取）
reranked_phrases = []
phrase_total_lines = 0

if os.path.exists(phrase_file):
    with open(phrase_file, "r", encoding="utf-16") as f:
        for line in f:
            phrase_total_lines += 1
            line = line.strip()
            if not line:
                continue

            # 使用正則表達式切分欄位
            parts = re.split(r"\s+", line)
            if len(parts) >= 2:
                romaji = parts[0]
                phrase = parts[1]

                # 嚴格篩選僅處理 2 個中文字的詞彙
                if len(phrase) == 2:
                    char1, char2 = phrase[0], phrase[1]

                    # 計算新權重邏輯
                    if char1 in char_ranks and char2 in char_ranks:
                        ph2_rank = char_ranks[char1] + char_ranks[char2]
                    else:
                        ph2_rank = 999999

                    reranked_phrases.append(
                        {
                            "romaji": romaji,
                            "phrase": phrase,
                            "new_rank": ph2_rank,
                        }
                    )
else:
    print(f"錯誤：找不到檔案 {phrase_file}")

# 3. 根據 new_rank 進行排序（由小到大）
reranked_phrases.sort(key=lambda x: x["new_rank"])

# 4. 寫入輸出檔案（以 UTF-16 寫入，嚴格遵循原結構）
output_lines = 0
with open(output_file, "w", encoding="utf-16") as f:
    for item in reranked_phrases:
        # 將羅馬拼音固定為 6 碼（不足 6 碼則在右側補空格）
        romaji_fixed = item["romaji"].ljust(6)

        # 將新排名轉為 6 位數，不足 6 位數則在前方補零 (leading zero)
        rank_fixed = str(item["new_rank"]).zfill(6)

        # 按照您的格式組合：6位編碼 + 中文字詞 + " " + 6位權重
        f.write(f"{romaji_fixed} {item['phrase']} {rank_fixed}\n")
        output_lines += 1

print("處理完成！已成功將雙字詞轉為指定結構，並以 UTF-16 編碼儲存。")

# 5. 印出修正後的比對結果
print("\n" + "=" * 60)
print("【輸入/輸出檔案行數統計】")
print(f"1. 輸入檔 ({char_rank_file:<40}) : {char_rank_lines:,} 行 (含標頭)")
print(f"2. 輸入檔 ({phrase_file:<40}) : {phrase_total_lines:,} 行")
print("-" * 60)
print(f"3. 輸出檔 ({output_file:<40}) : {output_lines:,} 行 (純雙字詞)")
print("=" * 60)
