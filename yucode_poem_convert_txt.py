import json
import re
import sys
import os
import glob

def load_yucode_dict(filepath='yus_candict_c.txt'):
    """
    讀取余氏碼表，建立漢字到余氏的映射字典
    """
    if not os.path.exists(filepath):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, 'yus_candict_c.txt')
    
    if not os.path.exists(filepath):
        raise Exception(f"找不到余氏碼表檔案：{filepath}")
    
    yucode_map = {}
    encodings = ['utf-16', 'utf-8', 'gbk', 'big5', 'gb2312', 'utf-16-le', 'utf-16-be']
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
                print(f"成功使用 {encoding} 編碼讀取余氏碼表")
                
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = re.split(r'\s+', line)
                    if len(parts) >= 2:
                        yucode = parts[0]
                        char = parts[1]
                        if char not in yucode_map:
                            yucode_map[char] = yucode
                
                return yucode_map
                
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    raise Exception(f"無法使用任何編碼讀取檔案 {filepath}")

def text_to_yucode(text, yucode_map):
    """將中文文字轉換為粵拼"""
    result = []
    for char in text:
        if char in yucode_map:
            result.append(yucode_map[char])
        elif char.isspace():
            result.append(char)
        else:
            result.append(char)
    return ' '.join(result)

def is_list_file(filepath):
    """判斷是否為詩詞列表檔案"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(500)
            content = content.strip()
            if content and content[0] not in '{[' and 'poem ' in content:
                return True
    except:
        pass
    
    encodings = ['utf-16', 'gbk', 'big5']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read(500)
                content = content.strip()
                if content and content[0] not in '{[' and 'poem ' in content:
                    return True
        except:
            continue
    
    return False

def process_list_file(filepath, yucode_map):
    """處理詩詞列表檔案"""
    print("偵測到詩詞列表格式，進行列表轉換...")
    
    content = None
    encodings = ['utf-8', 'utf-16', 'gbk', 'big5']
    
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
            yucode = text_to_yucode(poem_name, yucode_map)
            poems.append({
                "text": poem_name,
                "yucode": yucode
            })
    
    return poems

def parse_poem_file(filepath):
    """解析詩詞檔案，支援 JSON 及純文字格式 (回傳: data, is_text_fallback)"""
    if not os.path.exists(filepath):
        raise Exception(f"找不到輸入檔案：{filepath}")
    
    encodings = ['utf-8', 'utf-16', 'gbk', 'big5']
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
        print("找不到任何 poem*.txt 檔案")
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
    print("余氏碼表詩詞轉換工具")
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
    
    try:
        print("正在載入余氏碼表...")
        yucode_map = load_yucode_dict('yus_candict_c.txt')
        print(f"已載入 {len(yucode_map)} 個漢字映射")
        
        print("\n正在讀取檔案...")
        
        if is_list_file(input_file):
            output_file = f"{base_name}out.json"
            print(f"輸出檔案：{output_file}")
            
            data = process_list_file(input_file, yucode_map)
            poems = data
            print(f"處理了 {len(poems)} 個詩詞名稱")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(poems, f, ensure_ascii=False, indent=4)
                
            print(f"\n✅ 轉換完成！結果已儲存至 {output_file}")
            
        else:
            data, is_text_fallback = parse_poem_file(input_file)
            
            if is_text_fallback:
                # 純文字 Fallback 模式 -> 輸出 .out.txt
                output_file = f"{base_name}out.txt"
                print(f"輸出檔案：{output_file}")
                
                out_lines = []
                title = base_name
                if not (title.startswith('《') and title.endswith('》')):
                    title = f"《{title}》"
                out_lines.append(title)
                
                for line in data:
                    out_lines.append(line)
                    yucode_line = text_to_yucode(line, yucode_map)
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
                # JSON 模式 -> 輸出 .out.json
                output_file = f"{base_name}out.json"
                print(f"輸出檔案：{output_file}")
                
                if isinstance(data, list):
                    poems = data
                else:
                    poems = [data]
                
                print(f"找到 {len(poems)} 首詩詞")
                
                for poem in poems:
                    for sentence in poem.get('sentences', []):
                        text = sentence.get('text', '')
                        if text:
                            sentence['yucode'] = text_to_yucode(text, yucode_map)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(poems, f, ensure_ascii=False, indent=4)
                
                print(f"\n✅ 轉換完成！結果已儲存至 {output_file}")
                
                if poems:
                    print("\n" + "=" * 50)
                    print("轉換範例（前 3 筆）：")
                    print("=" * 50)
                    for i, item in enumerate(poems[:3]):
                        if 'title' in item:
                            print(f"{i+1}. {item.get('title', '無標題')}")
                            if 'sentences' in item and item['sentences']:
                                first = item['sentences'][0]
                                print(f"   原文：{first['text']}")
                                print(f"   余氏：{first['yucode']}")
                        else:
                            print(f"{i+1}. {item.get('text', '')}")
                            print(f"   余氏：{item.get('yucode', '')}")
                        print()
            
    except Exception as e:
        print(f"\n❌ 錯誤：{e}")
    
    input("\n按 Enter 鍵結束...")

if __name__ == '__main__':
    main()

'''
C:/Users/Dad/OneDrive/eyuime>yucode_poem_convert_txt.py
==================================================
余氏碼表詩詞轉換工具
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
> 1

輸入檔案：《似夢迷離_林子祥》.txt
正在載入余氏碼表...
成功使用 utf-16 編碼讀取余氏碼表
已載入 5896 個漢字映射

正在讀取檔案...
成功使用 utf-8 編碼讀取詩詞檔案
無法解析為 JSON，自動切換為純文字歌詞模式...
輸出檔案：《似夢迷離_林子祥》out.txt

✅ 轉換完成！結果已儲存至 《似夢迷離_林子祥》out.txt

==================================================
轉換範例（前 7 行）：
==================================================
《似夢迷離_林子祥》
似夢迷離 林子祥
chi mwg mae ley   lam jia che
作詞：潘偉源
jok cee uy poo way yun
作曲：林子祥
jok kuk uy lam jia che

按 Enter 鍵結束...
'''