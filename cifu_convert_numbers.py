import os

def convert_to_fullwidth_and_chinese_num(input_file, output_file):
    # 建立空的查表字典
    mapping = {}
    
    # 1. 將所有半形 ASCII 字元 (英文字母、標點符號) 對應到全形字元
    # 半形範圍是 0x0021 到 0x007E，利用固定偏移量 0xFEE0 轉全形
    for i in range(0x0021, 0x007E + 1):
        mapping[chr(i)] = chr(i + 0xFEE0)
        
    # 空格需要特殊處理
    mapping[' '] = '　'
    
    # (優化細節) 將半形點和逗號直接對應為中文標準標點，而非全形英文標點
    mapping['.'] = '。'
    mapping[','] = '，'
    
    # 2. 數字轉中文規則 (這會自動覆蓋掉第一步裡半形數字轉全形數字的設定)
    num_half = "0123456789"
    num_full = "０１２３４５６７８９"
    num_chi = "零一二三四五六七八九"
    
    for i in range(10):
        mapping[num_half[i]] = num_chi[i]
        mapping[num_full[i]] = num_chi[i]

    # 生成最終的查表引擎
    translate_table = str.maketrans(mapping)

    if not os.path.exists(input_file):
        print(f"⚠️ 找不到檔案: {input_file}")
        return

    print("開始進行綜合查表處理 (英標轉全形 + 數字轉中文)...")
    processed_count = 0
    
    with open(input_file, 'r', encoding='utf-16') as f_in, \
         open(output_file, 'w', encoding='utf-16') as f_out:
        
        for line in f_in:
            parts = line.strip().split()
            if len(parts) >= 2:
                rank = parts[0]
                word = parts[1]
                
                # 執行極速查表替換
                converted_word = word.translate(translate_table)
                
                if word != converted_word:
                    processed_count += 1
                
                f_out.write(f"{rank} {converted_word}\n")

    print(f"✅ 處理完成！共轉換了 {processed_count} 個包含數字、半形英文或標點的詞彙。")
    print(f"📄 轉換後的純淨檔案已匯出至：{output_file}")

if __name__ == "__main__":
    INPUT_FILE = 'HK_Standard_Written_PH2.txt'
    OUTPUT_FILE = 'HK_Standard_Written_PH2_FinalClean.txt'
    
    convert_to_fullwidth_and_chinese_num(INPUT_FILE, OUTPUT_FILE)