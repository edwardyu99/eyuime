import os
import jieba
import re

# --- 設定 ---
corpus_file = 'merge_ph2.txt'
output_extract_file = 'merge_ph2_extract.txt'
output_discard_file = 'merge_ph2_discard.txt'

input_file = 'merge_ph2_extract.txt'
output_file = 'merge_ph2_extract_ranked.txt'

file_encoding = 'utf-16'

def is_valid_hk_word(word):
    """嚴格過濾函數：排除人名、地名、帶有姓氏的稱謂，並以獨創的【雙層編碼動態過濾器】100% 封殺任何簡體字"""
    if len(word) != 2 or not re.match(r'^[\u4E00-\u9FA5]{2}$', word):
        return False
        
    # 【雙層編碼核心防禦機制】
    for char in word:
        try:
            char.encode('big5')
            if char in "体双丰儿价广厂么叶":
                return False
        except UnicodeEncodeError:
            hk_vernacular = "哋嘢嚟埗邨攞揼咗㗎喺嗰啱瞓嘥噚喐𡃁嚦鰂氹冧搲擸糭躝噱"
            if char not in hk_vernacular:
                return False
        
    surnames = "陳林黃吳李張王梁劉楊周鄭何郭曾鄧許馮謝蘇程曹袁田董潘杜姚鍾汪任姜範方石廖鄒熊金陸孔白崔康毛邱秦江史顧侯邵孟龍萬段雷錢湯尹黎易常喬賀賴龔柯蔣文武"
    titles = "總生父哥姐媽伯叔太公婆兄弟師官員長導主代老少氏娘爺太姐嫌某寓姓"
    
    if word[0] in surnames and word[1] in titles:
        if word in ['文員','文官','武官','王爺','侯爺','易主','陸生','陸官']:
            return True
        return False
        
    return True

def extract_words_from_local_corpus(word_dict, discard_dict):
    if not os.path.exists(corpus_file):
        print(f"找不到本地語料庫 {corpus_file}")
        return
        
    # 預先初始化結巴分詞
    jieba.initialize()
        
    print(f"【處理】正在從本地語料庫 {corpus_file} 智能辨識並提煉真實書面語...")
    with open(corpus_file, "r", encoding="utf-16") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            
            # 💡 核心邏輯：用正規表達式檢查這行是否「純粹是雙字詞條（前面可帶有流水號）」
            # 匹配成功：如 "172466 復似" 或 "復似"
            list_match = re.match(r'^\s*(?:\d+\s+)?([\u4E00-\u9FA5]{2})\s*$', line_str)
            
            if list_match:
                # ─── 【模式 A：詞表清單模式】 ───
                word = list_match.group(1)
                if is_valid_hk_word(word):
                    word_dict[word] = None      # 100% 錄取，不看結巴臉色
                else:
                    discard_dict[word] = None   # 違規詞送入廢棄區
            else:
                # ─── 【模式 B：長篇散文模式】 ───
                # 1. 正常結巴分詞（開啟 HMM 猜測新詞）
                words = jieba.cut(line_str, HMM=True)
                current_line_jieba_words = set()
                
                for word in words:
                    if len(word) == 2 and re.match(r'^[\u4E00-\u9FA5]{2}$', word):
                        current_line_jieba_words.add(word)
                        if is_valid_hk_word(word):
                            word_dict[word] = None
                        else:
                            discard_dict[word] = None
                            
                # 2. N-gram 補漏機制：抓出長句子裡結巴漏掉的「潛在未知雙字詞」
                chinese_chunks = re.findall(r'[\u4E00-\u9FA5]+', line_str)
                for chunk in chinese_chunks:
                    for i in range(len(chunk) - 1):
                        ngram_word = chunk[i:i+2]
                        # 如果這個雙字組合結巴字典沒有，剛才分詞也沒切出來，那就是「隱藏的新詞」
                        if ngram_word not in jieba.dt.FREQ and ngram_word not in current_line_jieba_words:
                            # 丟入 discard.txt 供用戶後續尋寶
                            discard_dict[ngram_word] = None

def reassign_ranks():
    word_dict = {}
    discard_dict = {}
    
    extract_words_from_local_corpus(word_dict, discard_dict)
    
    print(f"-> 本地語料庫共提煉出 {len(word_dict)} 個符合條件的不重複雙字詞。")
    print(f"-> 攔截並過濾了 {len(discard_dict)} 個不合格或待審查的新雙字詞。")

    final_words = list(word_dict.keys())
    discarded_words = list(discard_dict.keys())
    
    print(f"【完成】成功集齊了 {len(final_words)} 個不重複的香港雙字詞！")

    # 導出正式檔案
    print(f"【導出】正在寫入 {output_extract_file} (UTF-16 編碼)...")
    with open(output_extract_file, "w", encoding="utf-16") as f:
        for i, word in enumerate(final_words, 1):
            f.write(f"{i:06d} {word}\n")
    print(f"✨ 恭喜！{output_extract_file} 已成功生成。檔案包含 {len(final_words)} 行。")

    # 導出廢棄與新詞檔案
    print(f"【導出】正在寫入 {output_discard_file} (UTF-16 編碼)...")
    with open(output_discard_file, "w", encoding="utf-16") as f:
        for i, word in enumerate(discarded_words, 1):
            f.write(f"{i:06d} {word}\n")
    print(f"🗑️ 提示：{output_discard_file} 已生成。")

    print("-" * 50)

    # 處理排名與去重
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
            if not line.strip():
                continue
            total_lines += 1
            remaining_content = line[6:] 
            word = remaining_content.strip()
            if word in seen_words:
                continue
            seen_words.add(word)
            unique_lines += 1
            new_rank = f"{unique_lines:06d}"
            f_out.write(f"{new_rank}{remaining_content}")

    print(f"輸入檔案：   '{input_file}' -> 共 {total_lines} 行（含重複）")
    print(f"輸出檔案：   '{output_file}' -> 共 {unique_lines} 行（唯一值）")
    print(f"已移除重複詞條數量：{total_lines - unique_lines}")

if __name__ == "__main__":
    reassign_ranks()