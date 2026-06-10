import os

def read_lines(filepath):
    """讀取檔案，自動兼容 UTF-8 或 UTF-16 編碼"""
    if not os.path.exists(filepath):
        print(f"⚠️ 找不到檔案: {filepath}")
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='utf-16') as f:
            return f.readlines()

def parse_rank_file(lines):
    """解析以 Rank 為主的檔案 (例如 Cifu, ZH-50k)"""
    ranks = {}
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            try:
                rank = int(parts[0])
                word = parts[1]
                ranks[word] = rank
            except ValueError:
                continue
    return ranks

def parse_count_file(lines):
    """解析以 Count (次數) 為主的檔案 (例如 TW-Chi)，並將其轉換為 Rank"""
    counts = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            try:
                count = int(parts[0])
                word = parts[1]
                counts.append((count, word))
            except ValueError:
                continue
    
    # 依照次數由大到小排序，重新賦予 Rank (1, 2, 3...)
    counts.sort(key=lambda x: x[0], reverse=True)
    ranks = {}
    for i, (count, word) in enumerate(counts):
        ranks[word] = i + 1
    return ranks

def main():
    # 1. 定義檔案名稱
    FILE_HK = 'cifu_ph2freq.txt'
    FILE_TW = 'twchi_10000_ph2freq.txt'
    FILE_CN = 'zh-50k_ph2freq.txt'
    OUTPUT_FILE = 'hk_combined_ph2rank.txt'

    # 2. 讀取並解析資料
    print("讀取檔案中...")
    hk_ranks = parse_rank_file(read_lines(FILE_HK))
    cn_ranks = parse_rank_file(read_lines(FILE_CN))
    tw_ranks = parse_count_file(read_lines(FILE_TW))  # twchi 數字為遞減的次數，需轉為 Rank

    # 3. 設定地區權重 (可依需求自行微調)
    WEIGHT_HK = 1.0  # 香港粵語口語 (最優先)
    WEIGHT_TW = 0.6  # 台灣書面語 (補充繁體書面用詞)
    WEIGHT_CN = 0.3  # 大陸通用語 (補足現代名詞，但降低陸方專屬詞的影響)

    # 4. 收集所有出現過的雙字詞
    all_words = set(list(hk_ranks.keys()) + list(tw_ranks.keys()) + list(cn_ranks.keys()))
    
    word_scores = {}
    
    print("正在計算綜合詞頻權重...")
    # 5. 計算總分 (利用 Zipf's Law 概念：頻率約等於 1 / Rank)
    # 常數 100000 是為了讓分數變成較好讀的整數，不影響排序
    for word in all_words:
        score = 0.0
        
        if word in hk_ranks:
            score += WEIGHT_HK * (100000.0 / hk_ranks[word])
            
        if word in tw_ranks:
            score += WEIGHT_TW * (100000.0 / tw_ranks[word])
            
        if word in cn_ranks:
            score += WEIGHT_CN * (100000.0 / cn_ranks[word])
            
        word_scores[word] = score

    # 6. 依照總分由高到低排序
    sorted_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)

    # 7. 寫入最終整合檔案 (UTF-16)
    print("正在匯出結果...")
    with open(OUTPUT_FILE, 'w', encoding='utf-16') as f:
        for i, (word, score) in enumerate(sorted_words):
            rank = i + 1
            # 輸出格式: 000001 詞彙
            f.write(f"{rank:06d} {word}\n")

    print(f"✅ 整合完成！共處理了 {len(sorted_words)} 個不重複的雙字詞。")
    print(f"📄 檔案已匯出至：{OUTPUT_FILE}")

if __name__ == "__main__":
    main()