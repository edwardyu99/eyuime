'''
請寫一個PYTHON， 讀入附上的zh-50k.txt，提取雙字詞，轉換為繁體中文， 輸出以下ph2rank.txt (UTF-16)
000001 我們
000002 可以
000003 自己
其中頭6位數字是RANK，即zh-50k.txt中的詞頻排序
'''
# 
import opencc
import os

def process_file(input_filename, output_filename):
    # 初始化 OpenCC 轉換器 (s2t.json 代表 Simplified to Traditional 簡轉繁)
    converter = opencc.OpenCC('s2t.json')

    # 確認輸入檔案是否存在
    if not os.path.exists(input_filename):
        print(f"錯誤：找不到檔案 '{input_filename}'。")
        return

    rank = 1

    # 讀取原本的 utf-8 檔案，並以 utf-16 寫入新檔案
    with open(input_filename, 'r', encoding='utf-8') as f_in, \
         open(output_filename, 'w', encoding='utf-16') as f_out:
        
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            
            # 使用空白分割字串，提取詞彙 (zh-50k.txt 的格式為: 詞 頻率)
            parts = line.split()
            if len(parts) >= 1:
                word = parts[0]
                
                # 判斷是否為「雙字詞」 (長度剛好為 2)
                if len(word) == 2:
                    # 將簡體字轉換為繁體字
                    trad_word = converter.convert(word)
                    
                    # 格式化輸出：6位數字補零的RANK + 空格 + 繁體雙字詞
                    output_line = f"{rank:06d} {trad_word}\n"
                    f_out.write(output_line)
                    
                    # RANK 計數加 1
                    rank += 1

    print(f"✅ 處理完成！共提取了 {rank - 1} 個繁體雙字詞。")
    print(f"📄 檔案已成功匯出至 '{output_filename}' (UTF-16 編碼)。")

if __name__ == "__main__":
    INPUT_FILE = 'zh-50k.txt'
    OUTPUT_FILE = 'ph2rank.txt'
    
    process_file(INPUT_FILE, OUTPUT_FILE)