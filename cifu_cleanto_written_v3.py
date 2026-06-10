import os
import re

def clean_cantonese_colloquial_v3(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"找不到檔案：{input_file}")
        return

    # 1. 單字級黑名單 (擴充版)
    spoken_chars = set(
        "唔係咁啲喺咗嗰咩俾畀㗎喇喎噃冇諗睇搵食瞓攞嚟企"
        "咪佬婆仔靚衰蠢叻梗掂掟揼𢯎𢱕㩒嘢𠱁氹呃嬲𢛴攰唞"
        "黎啱岩哩依" # 新增：黎, 啱, 岩(作為借字時), 哩, 依(依家/依度)
    )
    
    # 2. 雙字詞黑名單 (大規模擴充)
    spoken_words = {
        # 先前已有的
        "好似", "點解", "點知", "入面", "老豆", "而家", "即刻", "鍾意",
        "仲有", "一齊", "係咪", "咁樣", "出面", "上面", "下面", "左近",
        "返去", "落去", "上去", "過嚟", "點算", "傾偈", "幾多", "幾時",
        "求其", "是但", "拍拖", "返工", "放工", "屋企", "頭先", "阿哥",
        "阿媽", "阿爸", "阿心", "今日", "琴日", "聽日", "尋日", "點樣",
        "幾好", "多啲", "少啲", "好人", "死梗",
        
        # 新增：代詞/指示詞
        "依家", "依度", "依個", "哩個", "我地", "我同", "我個", "我將", "邊個", "佢地",
        
        # 新增：動詞/方向
        "返到", "出黎", "返黎", "同埋", "跟住", "入去", "出去", "響度", "落黎", "上黎",
        
        # 新增：程度/時間/語氣
        "一陣", "一路", "成日", "唯有", "少少", "啱啱", "岩岩", "好彩", "仲要", "不如",
        
        # 新增：親屬/稱呼 (疊字或加阿字)
        "家姐", "細妹", "老母", "哥哥", "弟弟", "妹妹", "姐姐",
        
        # 新增：網路/粗口
        "仆街", "哈哈", "呵呵", "喪屍", "多謝",
        
        # 新增：常見分詞碎片 (我X, 當X)
        "我講", "當我", "我話", "我知", "我望", "我見", "我要", "我問", "講呢", "左個", "左好",
        "一望", "一下", "一聲"
    }

    # 3. 豁免名單 (防止誤殺，例如「依然」不應被「依」字黑名單殺掉)
    whitelist = {
        "關係", "體系", "聯繫", "企業", "企劃", "企圖", "第一", "最後", "時間",
        "依然", "依賴", "依照", "岩石", "岩層", "黎明", "巴黎", "出面",
        "上面", "下面"
    }
    
    # 4. 正則表達式規則：過濾「阿X」或「小X」的人名
    name_pattern = re.compile(r'^(阿|小)[\u4e00-\u9fa5]$')

    clean_words = []

    print("開始進行第三代深度清洗...")
    with open(input_file, 'r', encoding='utf-16') as f_in:
        for line in f_in:
            parts = line.strip().split()
            if len(parts) == 2:
                word = parts[1]
                
                # 判斷邏輯
                if word in whitelist:
                    clean_words.append(word)
                elif word in spoken_words:
                    continue
                elif name_pattern.match(word):
                    # 命中人名模式，例如「阿政」、「小貞」
                    continue
                elif any(char in spoken_chars for char in word):
                    # 命中單字黑名單，但需確保不在豁免名單內 (上面已處理)
                    continue
                elif word.startswith("我") and len(word) == 2 and word not in {"我們", "我國", "我方", "我軍", "我校", "我省", "我市", "我區"}:
                    # 過濾過多的「我X」碎片 (如：我望、我講)，保留正規書面詞
                    continue
                else:
                    clean_words.append(word)

    print("正在重新排名並匯出...")
    with open(output_file, 'w', encoding='utf-16') as f_out:
        for i, word in enumerate(clean_words):
            rank = i + 1
            f_out.write(f"{rank:06d} {word}\n")

    print(f"✅ 清洗完成！")
    print(f"📄 V3 版純書面語檔案已匯出至：{output_file}")

if __name__ == "__main__":
    INPUT_FILE = 'cifu_pure_written_ph2rank.txt' # 讀取上一版的輸出
    OUTPUT_FILE = 'cifu_v3_written_ph2rank.txt'
    
    clean_cantonese_colloquial_v3(INPUT_FILE, OUTPUT_FILE)