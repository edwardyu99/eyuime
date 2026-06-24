import os


def rank_and_sort_words(
    merge_file_path,
    hk_file_path,
    output_ranked_path,
    output_888888_path,
    encoding="utf-16",
):
    word_to_rank = {}
    merge_line_count = 0

    # 1. 讀取 merge_ph2.txt
    print("正在讀取 merge_ph2.txt...")
    with open(merge_file_path, "r", encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            merge_line_count += 1
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                rank_str, word = parts
                word_to_rank[word] = int(rank_str)

    ranked_entries = []
    not_found_entries = []
    hk_line_count = 0

    # 2. 讀取 HK_PH2_27000.TXT
    print("正在處理 HK_PH2_27000.TXT...")
    with open(hk_file_path, "r", encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            hk_line_count += 1
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                seq_str, word = parts
                if word in word_to_rank:
                    ranked_entries.append((word_to_rank[word], word))
                else:
                    not_found_entries.append((888888, word))

    # 3. 排序
    ranked_entries.sort(key=lambda x: x[0])

    # 4. 寫入 HK_PH2_27000_RANKED.TXT
    with open(output_ranked_path, "w", encoding=encoding) as f:
        for rank, word in ranked_entries:
            rank_str = str(rank).zfill(6)
            f.write(f"{rank_str} {word}\n")

    # 5. 寫入 HK_PH2_888888.TXT
    with open(output_888888_path, "w", encoding=encoding) as f:
        for rank, word in not_found_entries:
            f.write(f"{rank} {word}\n")

    # 報告精確行數
    print("\n" + "=" * 40)
    print("【檔案行數統計報告】")
    print("=" * 40)
    print(f"輸入檔案 1 ({merge_file_path}) 總行數: {merge_line_count} 行")
    print(f"輸入檔案 2 ({hk_file_path}) 總行數: {hk_line_count} 行")
    print("-" * 40)
    print(
        f"輸出檔案 1 ({output_ranked_path}) 總行數: {len(ranked_entries)} 行 (成功對照)"
    )
    print(
        f"輸出檔案 2 ({output_888888_path}) 總行數: {len(not_found_entries)} 行 (找不到對照)"
    )
    print("=" * 40)
    print("處理完成！")


# 執行設定
rank_and_sort_words(
    merge_file_path="merge_ph2.txt",
    hk_file_path="HK_PH2_27000.TXT",
    output_ranked_path="HK_PH2_27000_RANKED.TXT",
    output_888888_path="HK_PH2_888888.TXT",
    encoding="utf-16",
)