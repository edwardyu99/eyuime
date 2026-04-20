# -*- coding: utf-8 -*-
import os
import sys
import re

def is_chinese_char(ch):
    """判斷是否為中文字元（不包括標點符號、數字、英文等）"""
    return '\u4e00' <= ch <= '\u9fff'

def load_table(table_path, encoding='utf-16'):
    """載入碼表，回傳字典 {中文字詞: yucode}"""
    print(f"正在載入碼表：{table_path}")
    yucode_dict = {}
    try:
        with open(table_path, 'r', encoding=encoding) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    yucode = parts[0]
                    chinese_word = parts[1]
                    if chinese_word not in yucode_dict:
                        yucode_dict[chinese_word] = yucode
        print(f"成功載入，共 {len(yucode_dict)} 個詞條")
    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {table_path}")
        return None
    except Exception as e:
        print(f"載入時發生錯誤：{e}")
        return None
    return yucode_dict

def chinese_to_yucode(text, multi_dict, single_dict):
    """
    先使用多字詞碼表匹配（包括其中的單字），若無匹配則使用單字碼表匹配單字。
    只轉換中文字元，標點符號及非中文字元直接保留原樣。
    """
    if not text:
        return ""
    
    # 收集多字詞碼表中的所有詞，按長度遞減排序
    multi_words = sorted(multi_dict.keys(), key=len, reverse=True)
    
    result = []
    i = 0
    length = len(text)
    
    while i < length:
        matched = False
        
        # 1. 先嘗試從多字詞碼表匹配（長詞優先）
        for word in multi_words:
            word_len = len(word)
            if i + word_len <= length and text[i:i+word_len] == word:
                # 確保匹配的詞全部由中文字組成（多字詞碼表應皆為中文）
                result.append(multi_dict[word])
                i += word_len
                matched = True
                break
        
        # 2. 若多字詞碼表沒匹配到，且當前字元為中文字，嘗試用單字碼表
        if not matched and is_chinese_char(text[i]):
            single_char = text[i]
            if single_char in single_dict:
                result.append(single_dict[single_char])
                i += 1
                matched = True
        
        # 3. 若仍無匹配（非中文字元 或 連單字碼表都沒有），保留原字元
        if not matched:
            result.append(text[i])
            i += 1
    
    return ' '.join(result)

def main():
    if len(sys.argv) != 2:
        print("使用方法: python yucode_script.py <輸入檔案>")
        print("範例: python yucode_script.py 中文.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"錯誤：找不到輸入檔案 {input_file}")
        sys.exit(1)
    
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_yucode.txt"
    
    multi_table = "reneeyu_canph2345ori.txt"   # 多字詞碼表（優先）
    single_table = "yus_candict_c.txt"         # 單字碼表（備用）
    
    print(f"多字詞碼表：{multi_table}")
    print(f"單字碼表：{single_table}")
    
    multi_dict = load_table(multi_table)
    if multi_dict is None:
        print("錯誤：無法載入多字詞碼表，程式終止。")
        sys.exit(1)
    
    single_dict = load_table(single_table)
    if single_dict is None:
        print("錯誤：無法載入單字碼表，程式終止。")
        sys.exit(1)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            chinese_text = f.read()
        print(f"成功讀取輸入檔案，共 {len(chinese_text)} 個字元")
    except Exception as e:
        print(f"讀取 {input_file} 時發生錯誤：{e}")
        sys.exit(1)
    
    lines = chinese_text.splitlines()
    results = []
    
    for line in lines:
        if line.strip():
            yucode_line = chinese_to_yucode(line, multi_dict, single_dict)
            results.append((line, yucode_line))
        else:
            results.append(("", ""))
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for original_line, yucode_line in results:
                if original_line or yucode_line:
                    f.write(f"{original_line}\t{yucode_line}\n")
                else:
                    f.write("\n")
        print(f"\n轉換完成！")
        print(f"輸入檔案：{input_file}")
        print(f"輸出檔案：{output_file}")
    except Exception as e:
        print(f"寫入 {output_file} 時發生錯誤：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()