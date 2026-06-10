import os

def read_lines(filepath):
    if not os.path.exists(filepath):
        print(f"⚠️ 找不到檔案: {filepath}")
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f: return f.readlines()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='utf-16') as f: return f.readlines()

def parse_rank_file(lines):
    ranks = {}
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            try: ranks[parts[1]] = int(parts[0])
            except ValueError: continue
    return ranks

def parse_count_file(lines):
    counts = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            try: counts.append((int(parts[0]), parts[1]))
            except ValueError: continue
    counts.sort(key=lambda x: x[0], reverse=True)
    return {word: i + 1 for i, (count, word) in enumerate(counts)}

def main():
    # 1. 檔案路徑設定 (請確保這三個檔案都在同一個資料夾)
    FILE_HK = 'cifu_v3_written_ph2rank.txt' # 使用您剛洗好的 V3 版本
    FILE_TW = 'twchi_10000_ph2freq.txt'
    FILE_CN = 'zh-50k_ph2freq.txt'
    OUTPUT_FILE = 'HK_Standard_Written_PH2.txt' # 最終的完美詞庫

    print("讀取並解析三地詞庫中...")
    hk_ranks = parse_rank_file(read_lines(FILE_HK))
    cn_ranks = parse_rank_file(read_lines(FILE_CN))
    tw_ranks = parse_count_file(read_lines(FILE_TW)) 

    # 2. 黃金權重設定
    WEIGHT_TW = 1.0  # 繁體書面基底
    WEIGHT_HK = 0.8  # 香港在地書面語
    WEIGHT_CN = 0.4  # 通用現代名詞補充

    all_words = set(list(hk_ranks.keys()) + list(tw_ranks.keys()) + list(cn_ranks.keys()))
    word_scores = {}
    
    print("正在進行交叉驗證與 Zipf's Law 權重計算...")
    for word in all_words:
        score = 0.0
        # 頻率轉換分數 (Rank 越小，分數加越多)
        if word in tw_ranks: score += WEIGHT_TW * (100000.0 / tw_ranks[word])
        if word in hk_ranks: score += WEIGHT_HK * (100000.0 / hk_ranks[word])
        if word in cn_ranks: score += WEIGHT_CN * (100000.0 / cn_ranks[word])
            
        word_scores[word] = score

    # 依照總分由高到低排序
    sorted_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)

    print("正在匯出最終成果...")
    with open(OUTPUT_FILE, 'w', encoding='utf-16') as f:
        for i, (word, score) in enumerate(sorted_words):
            f.write(f"{i + 1:06d} {word}\n")

    print(f"✅ 大功告成！完美整合了 {len(sorted_words)} 個香港標準書面雙字詞。")
    print(f"📄 您的終極詞庫已匯出至：{OUTPUT_FILE}")

if __name__ == "__main__":
    main()