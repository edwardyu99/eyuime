import jieba
import jieba.posseg as pseg
import re

# 載入你的自定義香港字典
jieba.load_userdict("hk_dict.txt")

# 請將 input_file 替換為你的香港繁體語料庫檔案路徑
input_file = "hk_corpus_text.txt"
output_file = "HK_PH2.TXT"

def generate_hk_ph2(input_path, output_path, target_count=80000):
    word_set = set()
    
    # 僅允許純中文字符（排除包含數字、英文字母或標點的詞）
    chinese_pattern = re.compile(r'^[\u4E00-\u9FA5]{2}$')
    
    # 常見姓氏黑名單正則表達式，排除如「李總」、「黃父」、「陳生」等
    surname_pattern = re.compile(r'^(陳|林|黃|吳|李|張|王|梁|劉|楊|周|鄭|何|郭|曾)[總嫌生父婦哥姐媽伯叔太]')

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                # 使用 pseg 進行分詞與詞性標注
                words = pseg.cut(line.strip())
                for word, flag in words:
                    # 條件 1: 必須是雙字詞且全為中文
                    if len(word) == 2 and chinese_pattern.match(word):
                        # 條件 2: 排除人名(nr, nrfg, nrt)和地名(ns)
                        if flag not in ['nr', 'ns', 'nrfg', 'nrt']:
                            # 條件 3: 排除帶有姓氏的稱謂
                            if not surname_pattern.match(word):
                                word_set.add(word)
                                
                    # 達到目標數量即停止
                    if len(word_set) >= target_count:
                        break
                if len(word_set) >= target_count:
                    break
                    
    except FileNotFoundError:
        print(f"錯誤：找不到語料庫檔案 {input_path}")
        return

    # 將結果輸出為 UTF-16 格式，並加上 6 位數流水號
    with open(output_path, 'w', encoding='utf-16') as f:
        # 將集合轉為列表，不強制排序（符合無需排序的要求）
        for i, word in enumerate(list(word_set), 1):
            f.write(f"{i:06d} {word}\n")
            
    print(f"成功匯出 {len(word_set)} 個雙字詞至 {output_path}")

# 執行提取程式
if __name__ == "__main__":
    generate_hk_ph2(input_file, output_file, target_count=90000)