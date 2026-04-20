# -*- coding: utf-8 -*-
import os
import sys
import re

def is_chinese_char(ch):
    """判斷是否為中文字元（不包括標點符號、數字、英文等）"""
    return '\u4e00' <= ch <= '\u9fff'

def is_all_chinese(word):
    """判斷一個詞是否全部由中文字元組成"""
    return all(is_chinese_char(c) for c in word)

def load_table(table_path, encoding='utf-16', filter_non_chinese=True):
    """載入碼表，可選擇性過濾掉包含非中文字元的詞條"""
    print(f"正在載入碼表：{table_path}")
    yucode_dict = {}
    filtered_count = 0
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
                    if filter_non_chinese and not is_all_chinese(chinese_word):
                        filtered_count += 1
                        continue
                    if chinese_word not in yucode_dict:
                        yucode_dict[chinese_word] = yucode
        print(f"成功載入，共 {len(yucode_dict)} 個詞條（已過濾 {filtered_count} 個非中文詞條）")
    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {table_path}")
        return None
    except Exception as e:
        print(f"載入時發生錯誤：{e}")
        return None
    return yucode_dict

def chinese_to_yucode(text, multi_dict, single_dict):
    """只轉換中文字元，標點符號等保留原樣"""
    if not text:
        return ""
    
    multi_words = sorted(multi_dict.keys(), key=len, reverse=True)
    
    result = []
    i = 0
    length = len(text)
    
    while i < length:
        matched = False
        
        if is_chinese_char(text[i]):
            for word in multi_words:
                word_len = len(word)
                if i + word_len <= length and text[i:i+word_len] == word:
                    result.append(multi_dict[word])
                    i += word_len
                    matched = True
                    break
        
        if not matched and is_chinese_char(text[i]):
            single_char = text[i]
            if single_char in single_dict:
                result.append(single_dict[single_char])
                i += 1
                matched = True
        
        if not matched:
            result.append(text[i])
            i += 1
    
    return ' '.join(result)

def split_long_line(line, yucode_line, max_length=25):
    """將過長的行分割成多行，去除多餘空格"""
    # 先去除兩端空格
    line = line.strip()
    yucode_line = yucode_line.strip()
    
    if len(line) <= max_length:
        return [(line, yucode_line)]
    
    # 按標點符號分割
    separators = r'([。；！？：])'
    
    line_parts = re.split(separators, line)
    yucode_parts = re.split(separators, yucode_line)
    
    if len(line_parts) != len(yucode_parts):
        return split_by_length(line, yucode_line, max_length)
    
    result = []
    current_line = ""
    current_yucode = ""
    
    for i in range(0, len(line_parts), 2):
        if i + 1 < len(line_parts):
            segment = line_parts[i] + line_parts[i + 1]
            yucode_segment = yucode_parts[i] + yucode_parts[i + 1]
        else:
            segment = line_parts[i]
            yucode_segment = yucode_parts[i]
        
        if len(current_line + segment) > max_length and current_line:
            result.append((current_line.strip(), current_yucode.strip()))
            current_line = segment
            current_yucode = yucode_segment
        else:
            current_line += segment
            current_yucode += yucode_segment
    
    if current_line:
        result.append((current_line.strip(), current_yucode.strip()))
    
    if len(result) == 1 and len(result[0][0]) > max_length:
        return split_by_length(line, yucode_line, max_length)
    
    return result

def split_by_length(line, yucode_line, max_length=25):
    """簡單按字元長度分割"""
    line = line.strip()
    yucode_line = yucode_line.strip()
    result = []
    for i in range(0, len(line), max_length):
        line_chunk = line[i:i+max_length].strip()
        yucode_chunk = yucode_line[i:i+max_length].strip()
        if line_chunk:
            result.append((line_chunk, yucode_chunk))
    return result

def main():
    if len(sys.argv) != 2:
        print("使用方法: python yucode_script.py <輸入檔案>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"錯誤：找不到輸入檔案 {input_file}")
        sys.exit(1)
    
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_yucode.txt"
    
    multi_table = "reneeyu_canph2345ori.txt"
    single_table = "yus_candict_c.txt"
    
    print(f"多字詞碼表：{multi_table}")
    print(f"單字碼表：{single_table}")
    
    multi_dict = load_table(multi_table, filter_non_chinese=True)
    if multi_dict is None:
        sys.exit(1)
    
    single_dict = load_table(single_table, filter_non_chinese=True)
    if single_dict is None:
        sys.exit(1)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            chinese_text = f.read()
        print(f"成功讀取輸入檔案，共 {len(chinese_text)} 個字元")
    except Exception as e:
        print(f"讀取錯誤：{e}")
        sys.exit(1)
    
    lines = chinese_text.splitlines()
    results = []
    
    for line in lines:
        if line.strip():
            yucode_line = chinese_to_yucode(line, multi_dict, single_dict)
            if len(line.strip()) > 25:
                split_results = split_long_line(line, yucode_line, max_length=25)
                results.extend(split_results)
            else:
                results.append((line.strip(), yucode_line.strip()))
        else:
            results.append(("", ""))
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for original_line, yucode_line in results:
                if original_line or yucode_line:
                    # 使用 tab 分隔，確保對齊
                    f.write(f"{original_line}\t{yucode_line}\n")
                else:
                    f.write("\n")
        print(f"\n轉換完成！輸出檔案：{output_file}")
    except Exception as e:
        print(f"寫入錯誤：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()