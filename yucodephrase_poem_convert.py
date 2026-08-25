# -*- coding: utf-8 -*-
import json
import re
import sys
import os
import glob
import time

def is_chinese_char(ch):
    """判斷是否為中文字元（不包括標點符號、數字、英文等）"""
    return '\u4e00' <= ch <= '\u9fff'

def is_all_chinese(word):
    """判斷一個詞是否全部由中文字元組成"""
    return all(is_chinese_char(c) for c in word)

def load_table(filename, filter_non_chinese=False):
    """
    讀取碼表，支援多種編碼與腳本目錄路徑回退
    """
    filepath = filename
    if not os.path.exists(filepath):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"⚠️ 找不到碼表檔案：{filename}")
        return None
    
    yucode_map = {}
    filtered_count = 0
    encodings = ['utf-16', 'utf-8-sig', 'utf-8', 'gbk', 'big5', 'gb2312', 'utf-16-le', 'utf-16-be']
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = re.split(r'\s+', line)
                    if len(parts) >= 2:
                        yucode = parts[0]
                        word = parts[1]
                        if filter_non_chinese and not is_all_chinese(word):
                            filtered_count += 1
                            continue
                        if word not in yucode_map:
                            yucode_map[word] = yucode
                print(f"成功使用 {encoding} 編碼載入碼表 [{filename}]，共 {len(yucode_map)} 個詞條")
                return yucode_map
                
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    print(f"❌ 無法使用已知編碼讀取碼表檔案：{filepath}")
    return None

def build_word_trie(words_dict):
    """將詞典建構為 Trie（前綴樹），用於長詞優先快速匹配"""
    trie = {}
    max_len = 0
    if not words_dict:
        return trie, max_len
    
    for word, code in words_dict.items():
        max_len = max(max_len, len(word))
        node = trie
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node[''] = code
    return trie, max_len

def text_to_yucode_phrase(text, multi_trie, multi_max_len, full_dict):
    """
    優先使用 Trie 樹匹配多字詞組，未匹配之字詞退回單字碼表/原字
    """
    if not text:
        return ""
    
    result = []
    i = 0
    length = len(text)
    
    while i < length:
        matched = False
        best_match = None
        best_len = 0
        
        # 進行多字詞組匹配
        if multi_trie and multi_max_len > 0:
            node = multi_trie
            j = i
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
        else:
            ch = text[i]
            if full_dict and ch in full_dict:
                result.append(full_dict[ch])
            else:
                result.append(ch)
            i += 1
    
    # 組合並整理空格，消除過度連續空格
    raw_result = ' '.join(result)
    return re.sub(r' +', ' ', raw_result).strip()

def is_list_file(filepath):
    """判斷是否為詩詞列表檔案"""
    encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'gbk', 'big5']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read(500).strip()
                if content and content[0] not in '{[' and 'poem ' in content:
                    return True
        except (UnicodeDecodeError, UnicodeError, OSError):
            continue
    return False

def process_list_file(filepath, multi_trie, multi_max_len, full_dict):
    """處理詩詞列表檔案"""
    print("偵測到詩詞列表格式，進行列表轉換...")
    
    content = None
    encodings = ['utf-8', 'utf-8-sig', 'utf-16', 'gbk', 'big5']
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
                print(f"成功使用 {encoding} 編碼讀取列表檔案")
                break
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    if content is None:
        raise Exception(f"無法使用任何編碼讀取檔案 {filepath}")
    
    lines = content.strip().split('\n')
    poems = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('poem '):
            poem_name = line[5:].strip()
        elif line.startswith('poem'):
            poem_name = line[4:].strip()
        else:
            poem_name = line
        
        if poem_name:
            yucode = text_to_yucode_phrase(poem_name, multi_trie, multi_max_len, full_dict)
            poems.append({
                "text": poem_name,
                "yucode": yucode
            })
    
    return poems

def parse_poem_file(filepath):
    """解析詩詞檔案，支援 JSON 及純文字格式 (回傳: data, is_text_fallback)"""
    if not os.path.exists(filepath):
        raise Exception(f"找不到輸入檔案：{filepath}")
    
    encodings = ['utf-8-sig', 'utf-8', 'utf-16', 'gbk', 'big5']
    content = None
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
                print(f"成功使用 {encoding} 編碼讀取詩詞檔案")
                break
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    if content is None:
        raise Exception(f"無法使用任何編碼讀取檔案 {filepath}")
    
    if content.startswith('\ufeff'):
        content = content[1:]
    
    # 1. 嘗試直接 JSON 解析
    try:
        return json.loads(content), False
    except json.JSONDecodeError:
        pass

    # 2. 嘗試修復 JSON 格式
    try:
        fixed_content = re.sub(r',\s*}', '}', content)
        fixed_content = re.sub(r',\s*]', ']', fixed_content)
        if not fixed_content.strip().startswith('['):
            fixed_content = '[' + fixed_content + ']'
        return json.loads(fixed_content), False
    except json.JSONDecodeError:
        pass

    # 3. 純文字歌詞退回機制（Fallback）
    print("無法解析為 JSON，自動切換為純文字歌詞模式...")
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    return lines, True

def get_input_file():
    """取得輸入檔案名稱"""
    if len(sys.argv) >= 2:
        return sys.argv[1].strip()
    
    print("\n正在尋找可處理的檔案...")
    poem_files = glob.glob('《*.txt')
    poem_files = [f for f in poem_files if not f.endswith('out.txt')]
    
    all_files = poem_files
    
    if not all_files:
        print("找不到任何 《*.txt 檔案")
        return input("\n請輸入檔案名稱：").strip()
    
    print(f"\n找到 {len(all_files)} 個檔案：")
    for i, file in enumerate(all_files, 1):
        size = os.path.getsize(file)
        print(f"{i}. {file} ({size} bytes)")
    
    if len(all_files) == 1:
        print(f"\n只有一個檔案，自動選擇：{all_files[0]}")
        return all_files[0]
    
    print(f"\n請選擇檔案（輸入編號 1-{len(all_files)}）或直接輸入檔案名稱：")
    choice = input("> ").strip()
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(all_files):
            return all_files[idx]
    except ValueError:
        return choice
    
    return all_files[0]

def main():
    print("=" * 50)
    print("余氏詞組/單字詩詞轉換工具")
    print("=" * 50)
    
    input_file = get_input_file()
    
    if not input_file:
        print("錯誤：未指定輸入檔案")
        input("\n按 Enter 鍵結束...")
        sys.exit(1)
    
    if not os.path.exists(input_file):
        print(f"錯誤：找不到檔案 '{input_file}'")
        input("\n按 Enter 鍵結束...")
        sys.exit(1)
    
    base_name = os.path.splitext(input_file)[0]
    print(f"\n輸入檔案：{input_file}")
    
    multi_table = "reneeyu_canph2345ori.txt"
    single_table = "yus_candict_c.txt"
    
    try:
        print("\n正在載入多字詞組碼表...")
        multi_dict = load_table(multi_table, filter_non_chinese=True)
        
        print("\n正在載入單字完整碼表...")
        full_dict = load_table(single_table, filter_non_chinese=False)
        
        if full_dict is None:
            raise Exception("無法載入單字碼表，程式終止。")
        
        print("\n正在建立 Trie 樹長詞匹配結構...")
        multi_trie, multi_max_len = build_word_trie(multi_dict) if multi_dict else ({}, 0)
        print(f"Trie 樹建立完成，最長詞組長度：{multi_max_len}")
        
        print("\n正在讀取並處理輸入檔案...")
        
        if is_list_file(input_file):
            output_file = f"{base_name}out.json"
            print(f"輸出檔案：{output_file}")
            
            poems = process_list_file(input_file, multi_trie, multi_max_len, full_dict)
            print(f"處理了 {len(poems)} 個詩詞名稱")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(poems, f, ensure_ascii=False, indent=4)
                
            print(f"\n✅ 轉換完成！結果已儲存至 {output_file}")
            
        else:
            data, is_text_fallback = parse_poem_file(input_file)
            
            if is_text_fallback:
                output_file = f"{base_name}out.txt"
                print(f"輸出檔案：{output_file}")
                
                out_lines = []
                title = base_name
                if not (title.startswith('《') and title.endswith('》')):
                    title = f"《{title}》"
                out_lines.append(title)
                
                for line in data:
                    out_lines.append(line)
                    yucode_line = text_to_yucode_phrase(line, multi_trie, multi_max_len, full_dict)
                    out_lines.append(yucode_line)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(out_lines) + '\n')
                
                print(f"\n✅ 轉換完成！結果已儲存至 {output_file}")
                
                print("\n" + "=" * 50)
                print("轉換範例（前 7 行）：")
                print("=" * 50)
                for line in out_lines[:7]:
                    print(line)
                    
            else:
                output_file = f"{base_name}out.json"
                print(f"輸出檔案：{output_file}")
                
                poems = data if isinstance(data, list) else [data]
                print(f"找到 {len(poems)} 首詩詞")
                
                for poem in poems:
                    if isinstance(poem, dict):
                        if 'sentences' in poem:
                            for sentence in poem.get('sentences', []):
                                text = sentence.get('text', '')
                                if text:
                                    sentence['yucode'] = text_to_yucode_phrase(
                                        text, multi_trie, multi_max_len, full_dict
                                    )
                        elif 'text' in poem:
                            poem['yucode'] = text_to_yucode_phrase(
                                poem['text'], multi_trie, multi_max_len, full_dict
                            )
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(poems, f, ensure_ascii=False, indent=4)
                
                print(f"\n✅ 轉換完成！結果已儲存至 {output_file}")
                
                if poems:
                    print("\n" + "=" * 50)
                    print("轉換範例（前 3 筆）：")
                    print("=" * 50)
                    for i, item in enumerate(poems[:3]):
                        if isinstance(item, dict):
                            if 'title' in item:
                                print(f"{i+1}. {item.get('title', '無標題')}")
                                if 'sentences' in item and item['sentences']:
                                    first = item['sentences'][0]
                                    print(f"   原文：{first.get('text', '')}")
                                    print(f"   余氏：{first.get('yucode', '')}")
                            else:
                                print(f"{i+1}. 原文：{item.get('text', '')}")
                                print(f"   余氏：{item.get('yucode', '')}")
                            print()
            
    except Exception as e:
        print(f"\n❌ 錯誤：{e}")
    
    input("\n按 Enter 鍵結束...")

if __name__ == '__main__':
    main()

'''
C:/Users/Dad/OneDrive/eyuime>python yucodephrase_poem_convert.py yucode_practise_yucode_0822.json
==================================================
余氏詞組/單字詩詞轉換工具
==================================================

輸入檔案：yucode_practise_yucode_0822.json

正在載入多字詞組碼表...
成功使用 utf-16 編碼載入碼表 [reneeyu_canph2345ori.txt]，共 130086 個詞條

正在載入單字完整碼表...
成功使用 utf-16 編碼載入碼表 [yus_candict_c.txt]，共 5896 個詞條

正在建立 Trie 樹長詞匹配結構...
Trie 樹建立完成，最長詞組長度：7

正在讀取並處理輸入檔案...
成功使用 utf-8-sig 編碼讀取詩詞檔案
輸出檔案：yucode_practise_yucode_0822out.json
找到 9 首詩詞

✅ 轉換完成！結果已儲存至 yucode_practise_yucode_0822out.json

==================================================
轉換範例（前 3 筆）：
==================================================
1. 青玉案·元夕
   原文：東風夜放花千樹，更吹落、星如雨。
   余氏：dugfug yefon fa cinsuz h gag cuilok uz sig yueyuu t

2. 定風波
   原文：莫聽穿林打葉聲，何妨吟嘯且徐行。
   余氏：mokteg coolam da ipsig h hofon yumsiw ceh tsuhag t

3. 水調歌頭
   原文：明月幾時有？把酒問青天。
   余氏：mngyut geysy uq bajaw men tsitin t

C:/Users/Dad/OneDrive/eyuime>yucodephrase_poem_convert.py
==================================================
余氏詞組/單字詩詞轉換工具
==================================================

正在尋找可處理的檔案...

找到 9 個檔案：
1. 《似夢迷離_林子祥》.txt (864 bytes)
2. 《定風波》.txt (275 bytes)
3. 《水調歌頭》.txt (445 bytes)
4. 《白居易_長恨歌》.txt (3003 bytes)
5. 《紅燭淚》 (原唱：紅線女).txt (431 bytes)
6. 《羅剎海市》.txt (1916 bytes)
7. 《翩翩》.txt (1192 bytes)
8. 《花妖》.txt (1418 bytes)
9. 《青玉案_元夕》.txt (306 bytes)

請選擇檔案（輸入編號 1-9）或直接輸入檔案名稱：
> 4

輸入檔案：《白居易_長恨歌》.txt

正在載入多字詞組碼表...
成功使用 utf-16 編碼載入碼表 [reneeyu_canph2345ori.txt]，共 130082 個詞條

正在載入單字完整碼表...
成功使用 utf-16 編碼載入碼表 [yus_candict_c.txt]，共 5896 個詞條

正在建立 Trie 樹長詞匹配結構...
Trie 樹建立完成，最長詞組長度：7

正在讀取並處理輸入檔案...
成功使用 utf-8-sig 編碼讀取詩詞檔案
無法解析為 JSON，自動切換為純文字歌詞模式...
輸出檔案：《白居易_長恨歌》out.txt

✅ 轉換完成！結果已儲存至 《白居易_長恨歌》out.txt

==================================================
轉換範例（前 7 行）：
==================================================
《白居易_長恨歌》
長恨歌
chehg
朝代：唐代
jiudoi uy tondoi
作者：白居易
jokjeh uy pakgy

按 Enter 鍵結束...
'''