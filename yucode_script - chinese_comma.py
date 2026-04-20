# -*- coding: utf-8 -*-
import os
import sys
import re
import time

def is_chinese_char(ch):
    """判斷是否為中文字元（不包括標點符號、數字、英文等）"""
    return '\u4e00' <= ch <= '\u9fff'

def is_all_chinese(word):
    """判斷一個詞是否全部由中文字元組成"""
    return all(is_chinese_char(c) for c in word)

def load_table(table_path, encoding='utf-16', filter_non_chinese=True):
    """載入碼表，可選擇性過濾掉包含非中文字元的詞條"""
    print(f"正在載入碼表：{table_path}")
    start_time = time.time()
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
        elapsed = time.time() - start_time
        print(f"成功載入，共 {len(yucode_dict)} 個詞條（已過濾 {filtered_count} 個非中文詞條），耗時 {elapsed:.2f} 秒")
    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {table_path}")
        return None
    except Exception as e:
        print(f"載入時發生錯誤：{e}")
        return None
    return yucode_dict

def build_word_trie(words_dict):
    """
    將詞典建構為 Trie（前綴樹），加速匹配
    返回：trie 字典，以及最長詞長度
    """
    trie = {}
    max_len = 0
    for word in words_dict.keys():
        max_len = max(max_len, len(word))
        node = trie
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node[''] = words_dict[word]  # 用空字串標記結束及儲存編碼
    return trie, max_len

def chinese_to_yucode_fast(text, multi_trie, multi_max_len, single_dict):
    """
    使用 Trie 樹快速匹配，只轉換中文字元
    """
    if not text:
        return ""
    
    result = []
    i = 0
    length = len(text)
    
    while i < length:
        ch = text[i]
        
        # 非中文字元直接保留
        if not is_chinese_char(ch):
            result.append(ch)
            i += 1
            continue
        
        # 嘗試匹配多字詞
        matched = False
        node = multi_trie
        j = i
        best_match = None
        best_len = 0
        
        # 限制最大匹配長度
        max_search = min(multi_max_len, length - i)
        
        while j < i + max_search:
            ch2 = text[j]
            if ch2 in node:
                node = node[ch2]
                j += 1
                if '' in node:  # 找到一個完整匹配
                    best_match = node['']
                    best_len = j - i
            else:
                break
        
        if best_match:
            result.append(best_match)
            i += best_len
            matched = True
        
        # 若無多字詞匹配，嘗試單字匹配
        if not matched:
            if ch in single_dict:
                result.append(single_dict[ch])
            else:
                result.append(ch)
            i += 1
    
    return ' '.join(result)

def split_long_line_fast(line, yucode_line, max_length=25):
    """快速分割長行，去除多餘空格"""
    line = line.strip()
    yucode_line = yucode_line.strip()
    
    if len(line) <= max_length:
        return [(line, yucode_line)]
    
    # 按標點符號分割
    separators = r'([。；！？：])'
    
    line_parts = re.split(separators, line)
    yucode_parts = re.split(separators, yucode_line)
    
    if len(line_parts) != len(yucode_parts):
        return split_by_length_fast(line, yucode_line, max_length)
    
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
        return split_by_length_fast(line, yucode_line, max_length)
    
    return result

def split_by_length_fast(line, yucode_line, max_length=25):
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
    total_start = time.time()
    
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
    
    # 載入碼表
    multi_dict = load_table(multi_table, filter_non_chinese=True)
    if multi_dict is None:
        sys.exit(1)
    
    single_dict = load_table(single_table, filter_non_chinese=True)
    if single_dict is None:
        sys.exit(1)
    
    # 建立 Trie 樹加速匹配
    print("正在建立 Trie 樹...")
    trie_start = time.time()
    multi_trie, multi_max_len = build_word_trie(multi_dict)
    trie_elapsed = time.time() - trie_start
    print(f"Trie 樹建立完成，最長詞長度：{multi_max_len}，耗時 {trie_elapsed:.2f} 秒")
    
    # 讀取輸入檔案
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            chinese_text = f.read()
        print(f"成功讀取輸入檔案，共 {len(chinese_text)} 個字元")
    except Exception as e:
        print(f"讀取錯誤：{e}")
        sys.exit(1)
    
    # 逐行處理
    print("正在轉換...")
    convert_start = time.time()
    lines = chinese_text.splitlines()
    results = []
    line_count = 0
    
    for line in lines:
        if line.strip():
            yucode_line = chinese_to_yucode_fast(line, multi_trie, multi_max_len, single_dict)
            if len(line.strip()) > 25:
                split_results = split_long_line_fast(line, yucode_line, max_length=25)
                results.extend(split_results)
            else:
                results.append((line.strip(), yucode_line.strip()))
            line_count += 1
            # 每100行顯示進度
            if line_count % 100 == 0:
                print(f"  已處理 {line_count} 行...")
        else:
            results.append(("", ""))
    
    convert_elapsed = time.time() - convert_start
    print(f"轉換完成，共處理 {line_count} 行，耗時 {convert_elapsed:.2f} 秒")
    
    # 寫入輸出
    print("正在寫入檔案...")
    write_start = time.time()
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for original_line, yucode_line in results:
                if original_line or yucode_line:
                    f.write(f"{original_line}\t{yucode_line}\n")
                else:
                    f.write("\n")
        write_elapsed = time.time() - write_start
        print(f"寫入完成，耗時 {write_elapsed:.2f} 秒")
    except Exception as e:
        print(f"寫入錯誤：{e}")
        sys.exit(1)
    
    total_elapsed = time.time() - total_start
    print(f"\n=== 全部完成！===")
    print(f"輸出檔案：{output_file}")
    print(f"總耗時：{total_elapsed:.2f} 秒")

if __name__ == "__main__":
    main()