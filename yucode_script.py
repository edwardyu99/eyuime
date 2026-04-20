# -*- coding: utf-8 -*-
import os
import sys
import re
import time
import json

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

def load_full_table(table_path, encoding='utf-16'):
    """載入完整碼表（不過濾，包含標點符號）"""
    print(f"正在載入碼表：{table_path}")
    start_time = time.time()
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
        elapsed = time.time() - start_time
        print(f"成功載入，共 {len(yucode_dict)} 個詞條，耗時 {elapsed:.2f} 秒")
    except FileNotFoundError:
        print(f"錯誤：找不到檔案 {table_path}")
        return None
    except Exception as e:
        print(f"載入時發生錯誤：{e}")
        return None
    return yucode_dict

def build_word_trie(words_dict):
    """將詞典建構為 Trie（前綴樹），加速匹配"""
    trie = {}
    max_len = 0
    for word in words_dict.keys():
        max_len = max(max_len, len(word))
        node = trie
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node[''] = words_dict[word]
    return trie, max_len

def chinese_to_yucode_fast(text, multi_trie, multi_max_len, full_dict):
    """使用 Trie 樹快速匹配，所有字元（包括標點符號）都從 full_dict 轉換"""
    if not text:
        return ""
    
    result = []
    i = 0
    length = len(text)
    
    while i < length:
        ch = text[i]
        
        # 嘗試匹配多字詞（優先）
        matched = False
        node = multi_trie
        j = i
        best_match = None
        best_len = 0
        
        max_search = min(multi_max_len, length - i)
        
        while j < i + max_search:
            ch2 = text[j]
            if ch2 in node:
                node = node[ch2]
                j += 1
                if '' in node:
                    best_match = node['']
                    best_len = j - i
            else:
                break
        
        if best_match:
            result.append(best_match)
            i += best_len
            matched = True
        
        # 若無多字詞匹配，嘗試單字匹配（包括標點符號）
        if not matched:
            if ch in full_dict:
                result.append(full_dict[ch])
            else:
                result.append(ch)
            i += 1
    
    return ' '.join(result)

def convert_js_to_json(content):
    """
    將 JavaScript 物件陣列轉換為 JSON
    處理格式如: [ { title: "xxx", author: "xxx", sentences: [ ... ] } ]
    """
    lines = content.split('\n')
    result_lines = []
    
    for line in lines:
        # 處理屬性名: title: -> "title":
        line = re.sub(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'"\1":', line)
        
        # 處理物件開頭: { -> {
        # 處理陣列開頭: [ -> [
        
        # 處理結尾逗號
        line = re.sub(r',\s*$', '', line)
        
        # 保持原樣
        result_lines.append(line)
    
    # 重新組合
    content = '\n'.join(result_lines)
    
    # 使用 json 模組解析
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        # 如果失敗，嘗試使用 eval（安全模式）
        import ast
        try:
            # 將單引號轉為雙引號
            content = content.replace("'", '"')
            return ast.literal_eval(content)
        except:
            raise e

def parse_poem_file(filepath):
    """解析詩詞檔案（JavaScript 格式）"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 顯示檔案開頭
    lines = content.split('\n')
    print(f"檔案前幾行：")
    for i, line in enumerate(lines[:10]):
        print(f"  {i+1}: {line[:80]}")
    
    # 方法1：直接使用 JSON 解析（先轉換格式）
    try:
        # 替換所有無引號的屬性名
        fixed = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', content)
        # 替換單引號為雙引號（小心處理）
        fixed = re.sub(r"'([^']*)'", r'"\1"', fixed)
        # 移除結尾逗號
        fixed = re.sub(r',\s*}', '}', fixed)
        fixed = re.sub(r',\s*\]', ']', fixed)
        
        data = json.loads(fixed)
        print(f"✅ 解析成功，共 {len(data)} 首詩詞")
        return data
    except json.JSONDecodeError as e:
        print(f"JSON 解析失敗：{e}")
    
    # 方法2：逐行手動解析
    print("嘗試手動解析...")
    try:
        # 找到陣列開始
        start_idx = content.find('[')
        end_idx = content.rfind(']')
        if start_idx == -1 or end_idx == -1:
            raise ValueError("找不到陣列")
        
        array_content = content[start_idx:end_idx+1]
        
        # 使用 eval（注意：只在可信檔案使用）
        # 先將 null/true/false 轉換
        array_content = array_content.replace('null', 'None')
        array_content = array_content.replace('true', 'True')
        array_content = array_content.replace('false', 'False')
        
        # 使用 ast.literal_eval
        import ast
        data = ast.literal_eval(array_content)
        print(f"✅ 手動解析成功，共 {len(data)} 首詩詞")
        return data
    except Exception as e2:
        print(f"手動解析也失敗：{e2}")
        print("\n請確認檔案格式正確。")
        print("期望格式：")
        print("  [")
        print("    { title: '標題', author: '作者', sentences: [...] },")
        print("    ...")
        print("  ]")
        sys.exit(1)

def process_poem_file(input_file, output_file, multi_trie, multi_max_len, full_dict):
    """處理詩詞檔案"""
    data = parse_poem_file(input_file)
    
    total_sentences = 0
    total_poems = 0
    
    def process_item(item):
        nonlocal total_sentences, total_poems
        if isinstance(item, dict):
            if 'title' in item and 'sentences' in item:
                total_poems += 1
                print(f"\n📖 處理詩詞 [{total_poems}]: {item.get('title', '未知')} - {item.get('author', '未知')}")
            
            if 'text' in item:
                # 轉換 text 為 yucode
                new_yucode = chinese_to_yucode_fast(
                    item['text'], multi_trie, multi_max_len, full_dict
                )
                item['yucode'] = new_yucode
                total_sentences += 1
                text_preview = item['text'][:40] + "..." if len(item['text']) > 40 else item['text']
                yucode_preview = new_yucode[:50] + "..." if len(new_yucode) > 50 else new_yucode
                print(f"  ✅ {text_preview} -> {yucode_preview}")
            else:
                for value in item.values():
                    process_item(value)
        elif isinstance(item, list):
            for element in item:
                process_item(element)
    
    process_item(data)
    
    print(f"\n📊 統計：共處理 {total_poems} 首詩詞，{total_sentences} 個句子")
    
    # 輸出為標準 JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return f"{total_poems} 首詩詞, {total_sentences} 個句子"

def main():
    total_start = time.time()
    
    if len(sys.argv) != 2:
        print("使用方法: python yucode_script.py <輸入檔案>")
        print("支援格式：.txt 或 .json（含 JavaScript 格式）")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"錯誤：找不到輸入檔案 {input_file}")
        sys.exit(1)
    
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_yucode.json"
    
    multi_table = "reneeyu_canph2345ori.txt"
    single_table = "yus_candict_c.txt"
    
    print(f"多字詞碼表：{multi_table}")
    print(f"單字碼表：{single_table}")
    print()
    
    # 載入碼表
    multi_dict = load_table(multi_table, filter_non_chinese=True)
    if multi_dict is None:
        sys.exit(1)
    
    full_dict = load_full_table(single_table)
    if full_dict is None:
        sys.exit(1)
    
    print(f"完整碼表共 {len(full_dict)} 個詞條（包含標點符號）")
    
    # 建立 Trie 樹
    print("正在建立 Trie 樹...")
    trie_start = time.time()
    multi_trie, multi_max_len = build_word_trie(multi_dict)
    trie_elapsed = time.time() - trie_start
    print(f"Trie 樹建立完成，最長詞長度：{multi_max_len}，耗時 {trie_elapsed:.2f} 秒")
    print()
    
    # 處理檔案
    print("正在轉換...")
    convert_start = time.time()
    result_info = process_poem_file(input_file, output_file, multi_trie, multi_max_len, full_dict)
    convert_elapsed = time.time() - convert_start
    
    print(f"\n轉換完成，耗時 {convert_elapsed:.2f} 秒")
    
    total_elapsed = time.time() - total_start
    print(f"\n=== 全部完成！===")
    print(f"輸出檔案：{output_file}")
    print(f"處理結果：{result_info}")
    print(f"總耗時：{total_elapsed:.2f} 秒")

if __name__ == "__main__":
    main()