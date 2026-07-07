import os

# --- 設定 ---
input_file = '000001_ph2.txt'
output_file = '000001_ph2_ranked.txt'

#input_file = 'merge_ph2.txt'
#output_file = 'merge_ph2_ranked.txt'

#input_file = 'merge_jieba.txt'
#output_file = 'merge_jieba_ranked.txt'

# 若檔案編碼為 UTF-16，請保留 'utf-16'；若為 UTF-8 可改成 'utf-8'
file_encoding = 'utf-16'

def reassign_ranks():
    if not os.path.exists(input_file):
        print(f"錯誤：找不到輸入檔案 '{input_file}'")
        return

    print(f"正在讀取 '{input_file}'，重新編排序號並移除重複詞條……")

    seen_words = set()
    total_lines = 0
    unique_lines = 0

    with open(input_file, 'r', encoding=file_encoding) as f_in, \
         open(output_file, 'w', encoding=file_encoding) as f_out:

        for line in f_in:
            # 跳過空行
            if not line.strip():
                continue

            total_lines += 1

            # 原格式為 "000001 詞語"，保留第 6 個字元之後的內容（含空格）
            remaining_content = line[6:]   # 包含前面的空格
            word = remaining_content.strip()   # 取出純詞語

            # 若已出現過則跳過（移除重碼）
            if word in seen_words:
                continue
            seen_words.add(word)

            # 產生新的 6 位數流水號
            unique_lines += 1
            new_rank = f"{unique_lines:06d}"

            # 寫出更新後的行
            f_out.write(f"{new_rank}{remaining_content}")

    print(f"輸入檔案：   '{input_file}' -> 共 {total_lines} 行（含重複）")
    print(f"輸出檔案：   '{output_file}' -> 共 {unique_lines} 行（唯一值）")
    print(f"已移除重複詞條數量：{total_lines - unique_lines}")

if __name__ == "__main__":
    reassign_ranks()