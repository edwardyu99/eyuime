import jieba
import re
import requests
import os

# 檔案路徑設定
corpus_file = "hk_corpus_text.txt"
dict_file = "hk_dict.txt"
output_file = "HK_PH2.TXT"
TARGET_COUNT = 27100 #30000  # 設定目標行數

def load_user_dictionary():
    """如果用戶有自訂的 hk_dict.txt，則優先載入"""
    if os.path.exists(dict_file):
        print(f"【載入】偵測到自訂字典 {dict_file}，正在導入...")
        jieba.load_userdict(dict_file)
    else:
        print(f"【提示】未偵測到自訂字典 {dict_file}，將使用預設分詞。")

def is_valid_hk_word(word):
    """嚴格過濾函數：排除人名、地名、帶有姓氏的稱謂，並以獨創的【雙層編碼動態過濾器】100% 封殺任何簡體字"""
    # 1. 必須剛好是兩個字，且必須全為中文
    if len(word) != 2 or not re.match(r'^[\u4E00-\u9FA5]{2}$', word):
        return False
        
    # 【雙層編碼核心防禦機制】
    for char in word:
        try:
            # 第一層：嘗試用純標準繁體 (Big5) 編碼
            char.encode('big5')
            # 如果成功，說明是標準繁體字。但要排除少數在 Big5 中存在、但在現代常被當作簡體/俗字的特殊字外觀
            if char in "体双丰儿价广厂么叶":
                return False
        except UnicodeEncodeError:
            # 第二層：如果 Big5 編碼失敗，說明它不是標準繁體字
            # 它此時只可能是：(A) 真正的香港本土粵語/地名特有字，或 (B) 混在 HKSCS 裡的內地簡體字
            # 我們採用【香港特有字精準白名單】，不在名單內的非 Big5 字一律視為簡體字直接剔除！
            hk_vernacular = "哋嘢嚟埗邨攞揼咗㗎喺嗰啱瞓嘥噚喐𡃁嚦鰂氹冧搲擸糭躝噱"
            if char not in hk_vernacular:
                return False
                
    # 2. 專門消滅常見地名與行政區黑名單
    stop_places = {
        "尖沙", "銅鑼","台港"
        # "香港", "九龍", "新界", "澳門", "台灣", "臺灣", "中國", "北京", "上海", "廣州", "深圳", "廣東", 
        # "亞洲", "祖國", "全國", "中央", "內地", "中港", "港台", "歐美", "日本", "韓國", "英國", 
        # "美國", "中方", "美方", "警方", "官方", "院方", "校方", "地方", "各方", "雙方", "一帶", "一路",
        # "大埔", "沙田", "屯門", "荃灣", "元朗", "柴灣", "中環", "旺角", "西貢", "觀塘"
    }
    if word in stop_places:
        return False
        
    # 3. 專門消滅「姓氏+稱謂」（如：李總、黃父、陳生、張老、劉氏、曾大、謝長）
    surnames = "陳林黃吳李張王梁劉楊周鄭何郭曾鄧許馮謝蘇程曹袁田董潘杜姚鍾汪任姜範方石廖鄒熊金陸孔白崔康毛邱秦江史顧侯邵孟龍萬段雷錢湯尹黎易常喬賀賴龔柯蔣文武" #文武
    titles = "總生父哥姐媽伯叔太公婆兄弟師官員長導主代老少氏娘爺太姐嫌某寓姓"
    if word[0] in surnames and word[1] in titles:
        if word in ['文員','文官','武官','王爺','侯爺','易主','陸生','陸官']:
            return True
        print(f"delete {word}") 
        return False
        
    return True

def extract_words_from_local_corpus(word_set):
    """使用標準 jieba.cut 提煉真實書面語"""
    if not os.path.exists(corpus_file):
        print(f"找不到本地語料庫 {corpus_file}，請先執行 build_hk_corpus.py")
        return
        
    print(f"【處理】正在從本地語料庫 {corpus_file} 快打旋風提煉真實書面語...")
    with open(corpus_file, "r", encoding="utf-8") as f:
        for line in f:
            words = jieba.cut(line.strip())
            for word in words:
                if is_valid_hk_word(word):
                    word_set.add(word)

def fetch_rime_cantonese_backup(word_set):
    """連線到香港 Rime 詞庫與 Jieba 官方大詞典（繁體版）補足差額，透過雙層過濾保證 100% 全繁體"""
    if len(word_set) >= TARGET_COUNT:
        return
        
    print(f"【補充】目前僅有 {len(word_set)} 個不重複詞。開始從線上下載高品質純繁體詞彙庫...")
    
    sources = [
#        {"name": "Rime 香港粵語詞組庫 (CDN)", "url": "https://cdn.jsdelivr.net/gh/rime/rime-cantonese@master/jyut6ping3.phrase.dict.yaml"},
#        {"name": "Rime 香港粵語詞組庫 (GitHub)", "url": "https://raw.githubusercontent.com/rime/rime-cantonese/master/jyut6ping3.phrase.dict.yaml"},

#        {"name": "Jieba 官方大詞典-繁體版 (CDN)", "url": 
# "https://cdn.jsdelivr.net/gh/fxsjy/jieba@master/extra_dict/dict.txt.big"},
#        {"name": "Jieba 官方大詞典-繁體版 (GitHub)", "url": #"https://raw.githubusercontent.com/fxsjy/jieba/master/extra_dict/dict.txt.big"}
    ]
    
    for src in sources:
        # if len(word_set) >= TARGET_COUNT:
        #    break
        try:
            print(f"  -> 正在下載並解析 {src['name']}...")
            response = requests.get(src['url'], headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
            response.raise_for_status()
            
            lines = response.text.split('\n')
            in_data_zone = False if "dict.yaml" in src['url'] else True 
            
            for line in lines:
                cleaned_line = line.strip()
                if not cleaned_line or cleaned_line.startswith('#'):
                    continue
                    
                if "dict.yaml" in src['url'] and cleaned_line.startswith("..."):
                    in_data_zone = True
                    continue
                    
                if not in_data_zone:
                    continue
                    
                parts = cleaned_line.split()
                if not parts:
                    continue
                word = parts[0]
                
                if is_valid_hk_word(word):
                    word_set.add(word)
                    
                if len(word_set) >= TARGET_COUNT:
                    break
            print(f"  -> 目前累積【純繁體】詞彙量已達到: {len(word_set)} 個")
        except Exception as e:
            print(f"  -> 該鏈接跳過: {e}")
            continue
    """        
    # 【終極離線安全網】萬一字數依舊不夠，才動用本地預設字典，但同樣接受雙層過濾器的超嚴格審查
    if len(word_set) < TARGET_COUNT:
        remaining = TARGET_COUNT - len(word_set)
        print(f"\n【備用方案啟動】字數仍不足，差額 {remaining} 個。正在從本地解鎖純繁體詞...")
        for word in jieba.dt.FREQ.keys():
            if is_valid_hk_word(word): 
                word_set.add(word)
                print(word)
            if len(word_set) >= TARGET_COUNT:
                break
    """
def main():
    word_set = set()
    
    # 1. 載入自訂詞典（如果有）
    load_user_dictionary()
    
    # 2. 瞬間榨乾本地語料庫
    extract_words_from_local_corpus(word_set)
    print(f"-> 本地語料庫共提煉出 {len(word_set)} 個符合條件的不重複雙字詞。")
    
    # 3. 補足安全網（直奔 80,000 大關）
    fetch_rime_cantonese_backup(word_set)
    
    # 4. 最終裁剪至目標數量
    final_words = list(word_set)[:TARGET_COUNT]
    print(f"【完成】成功集齊了 {len(final_words)} 個不重複的香港雙字詞！")
    
    # 5. 以 UTF-16 格式寫入 HK_PH2.TXT，並加上 6 位數流水號
    print(f"【導出】正在寫入 {output_file} (UTF-16 編碼)...")
    with open(output_file, "w", encoding="utf-16") as f:
        for i, word in enumerate(final_words, 1):
            f.write(f"{i:06d} {word}\n")
            
    print(f"✨ 恭喜！{output_file} 已成功生成。檔案包含 {len(final_words)} 行。")

if __name__ == "__main__":
    main()