import os

def load_char_dict(filepath):
    """嚴格查表：讀取單字與對應的 yucode"""
    char_map = {}
    if not os.path.exists(filepath):
        print(f"⚠️ 找不到單字碼表: {filepath}")
        return char_map
        
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                char = parts[0]
                code = parts[1]
                # 若有一字多碼，這裡僅取第一組碼作為組詞基礎
                if char not in char_map:
                    char_map[char] = code
    return char_map

def generate_phrase_dict(rank_file, char_dict_file, output_file):
    char_map = load_char_dict(char_dict_file)
    if not char_map:
        return

    print("開始進行雙字詞查表映射...")
    success_count = 0
    missing_chars = set()

    with open(output_file, 'w', encoding='utf-8') as f_out:
        # 寫入 RIME 字典檔頭 (可依需求調整)
        f_out.write("---\n")
        f_out.write("name: eyuime.phrase\n")
        f_out.write("version: \"1.0\"\n")
        f_out.write("sort: by_weight\n")
        f_out.write("...\n\n")

        with open(rank_file, 'r', encoding='utf-16') as f_in:
            for line in f_in:
                parts = line.strip().split()
                if len(parts) == 2:
                    rank = int(parts[0])
                    word = parts[1]
                    
                    # 嚴格查表：確保雙字詞的兩個字都在單字表內
                    if len(word) == 2:
                        char1, char2 = word[0], word[1]
                        if char1 in char_map and char2 in char_map:
                            # 組合雙字詞的 yucode (依據您的拆碼規則，此處以直接相連為例)
                            phrase_code = char_map[char1] + char_map[char2]
                            
                            # 利用排名的倒數作為 RIME 的詞頻權重 (Weight)
                            # 排名越前，權重數字越大
                            weight = int(10000000 / rank) 
                            
                            # 匯出標準 RIME 格式： 詞彙[Tab]編碼[Tab]權重
                            f_out.write(f"{word}\t{phrase_code}\t{weight}\n")
                            success_count += 1
                        else:
                            if char1 not in char_map: missing_chars.add(char1)
                            if char2 not in char_map: missing_chars.add(char2)

    print(f"✅ 詞庫生成完成！成功映射了 {success_count} 個雙字詞。")
    if missing_chars:
        print(f"⚠️ 發現 {len(missing_chars)} 個缺漏單字無法查表，建議後續補齊。")

if __name__ == "__main__":
    # 檔案路徑設定
    RANK_FILE = 'HK_Standard_Written_PH2.txt'
    CHAR_DICT = 'yucode_char.txt'       # 您的單字對照表 (需為 utf-8 編碼)
    OUTPUT_DICT = 'eyuime.phrase.dict.yaml'
    
    generate_phrase_dict(RANK_FILE, CHAR_DICT, OUTPUT_DICT)