import os

def clean_cantonese_colloquial_v2(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"找不到檔案：{input_file}")
        return

    # 1. 單字級黑名單 (過濾帶有專屬口語字的詞)
    spoken_chars = set(
        "唔係咁啲喺咗嗰咩俾畀㗎喇喎噃冇諗睇搵食瞓攞嚟企"
        "咪佬婆仔靚衰蠢叻梗掂掟揼𢯎𢱕㩒嘢𠱁氹呃嬲𢛴攰唞"
    )
    
    # 2. 雙字詞黑名單 (專殺「由標準漢字組成」的粵語口語詞)
    spoken_words = {
        "好似", "點解", "點知", "入面", "老豆", "而家", "即刻", "鍾意",
        "仲有", "一齊", "係咪", "咁樣", "出面", "上面", "下面", "左近",
        "返去", "落去", "上去", "過嚟", "點算", "傾偈", "幾多", "幾時",
        "求其", "是但", "拍拖", "返工", "放工", "屋企", "頭先", "阿哥",
        "阿媽", "阿爸", "阿心", "今日", "琴日", "聽日", "尋日", "點樣",
        "幾好", "多啲", "少啲", "好人", "死梗"
    }
    
    # 3. 豁免名單 (防止誤殺，有些字在口語和書面語都通用)
    whitelist = {"關係", "體系", "聯繫", "企業", "企劃", "企圖", "第一", "最後", "時間"}

    clean_words = []

    print("開始進行雙重清洗 (單字特徵 + 詞彙特徵)...")
    with open(input_file, 'r', encoding='utf-16') as f_in:
        for line in f_in:
            parts = line.strip().split()
            if len(parts) == 2:
                word = parts[1]
                
                # 判斷邏輯
                if word in whitelist:
                    clean_words.append(word)
                elif word in spoken_words:
                    # 命中「詞彙」黑名單 -> 丟棄
                    continue
                elif any(char in spoken_chars for char in word):
                    # 命中「單字」黑名單 -> 丟棄
                    continue
                else:
                    clean_words.append(word)

    print("正在重新排名並匯出...")
    with open(output_file, 'w', encoding='utf-16') as f_out:
        for i, word in enumerate(clean_words):
            rank = i + 1
            f_out.write(f"{rank:06d} {word}\n")

    print(f"✅ 清洗完成！")
    print(f"📄 升級版純書面語檔案已匯出至：{output_file}")

if __name__ == "__main__":
    # 讀取剛剛尚未完全乾淨的檔案
    INPUT_FILE = 'cifu_written_ph2rank.txt'
    OUTPUT_FILE = 'cifu_pure_written_ph2rank.txt'
    
    clean_cantonese_colloquial_v2(INPUT_FILE, OUTPUT_FILE)