import json
import re
import sys
import os
import glob

def load_yucode_dict(filepath='yus_candict_c.txt'):
    """
    讀取余氏碼表，建立漢字到粵拼的映射字典
    """
    # 如果沒找到檔案，嘗試在程式所在目錄尋找
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
        elif char in '，。？、；：「」『』！～…—－·':
            # 保留中文標點符號
            result.append(char)
        elif char.isspace():
            # 保留空格
            result.append(char)
        else:
            # 未知字符保留原樣
            result.append(char)
    return ' '.join(result)

def is_list_file(filepath):
    """判斷是否為詩詞列表檔案（純文字，每行一個詩詞名稱）"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(500)  # 只讀取前 500 個字符
            # 如果內容不以 { 或 [ 開頭，且包含 "poem "，則視為列表檔案
            content = content.strip()
            if content and content[0] not in '{[' and 'poem ' in content:
                return True
    except:
        pass
    
    # 嘗試其他編碼
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
    
    # 讀取檔案內容
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
    
    # 解析每一行
    lines = content.strip().split('\n')
    poems = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 移除 "poem " 前綴
        if line.startswith('poem '):
            poem_name = line[5:].strip()
        elif line.startswith('poem'):
            poem_name = line[4:].strip()
        else:
            poem_name = line
        
        if poem_name:
            # 生成粵拼
            yucode = text_to_yucode(poem_name, yucode_map)
            poems.append({
                "text": poem_name,
                "yucode": yucode
            })
    
    return poems

def parse_poem_file(filepath):
    """解析詩詞檔案，處理可能的不完整 JSON 格式"""
    if not os.path.exists(filepath):
        raise Exception(f"找不到輸入檔案：{filepath}")
    
    # 嘗試不同的編碼
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
    
    # 清理可能的 BOM 字符
    if content.startswith('\ufeff'):
        content = content[1:]
    
    # 嘗試直接解析
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON 解析錯誤：{e}")
        print("嘗試修復 JSON 格式...")
        
        # 方法1：嘗試將內容包裝成陣列
        try:
            # 移除多餘的逗號
            fixed_content = re.sub(r',\s*}', '}', content)
            fixed_content = re.sub(r',\s*]', ']', fixed_content)
            
            # 如果不是以 [ 開頭，則包裝成陣列
            if not fixed_content.strip().startswith('['):
                fixed_content = '[' + fixed_content + ']'
            
            return json.loads(fixed_content)
        except:
            pass
        
        # 方法2：逐個解析 JSON 物件
        objects = []
        decoder = json.JSONDecoder()
        idx = 0
        content = content.strip()
        
        while idx < len(content):
            try:
                obj, idx = decoder.raw_decode(content, idx)
                objects.append(obj)
                # 跳過逗號和空白
                while idx < len(content) and content[idx] in ' \t\n\r,':
                    idx += 1
            except json.JSONDecodeError:
                # 如果無法解析，嘗試跳過一個字符
                idx += 1
        
        if objects:
            print(f"成功解析 {len(objects)} 個詩詞物件")
            return objects
        
        raise Exception("無法解析詩詞檔案")

def get_input_file():
    """取得輸入檔案名稱"""
    # 檢查命令列參數
    if len(sys.argv) >= 2:
        return sys.argv[1].strip()
    
    # 如果沒有參數，尋找檔案
    print("\n正在尋找可處理的檔案...")
    
    # 尋找 poem*.txt 檔案
    poem_files = glob.glob('poem*.txt')
    # 過濾掉輸出檔案
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
    
    # 取得輸入檔案
    input_file = get_input_file()
    
    if not input_file:
        print("錯誤：未指定輸入檔案")
        input("\n按 Enter 鍵結束...")
        sys.exit(1)
    
    # 檢查檔案是否存在
    if not os.path.exists(input_file):
        print(f"錯誤：找不到檔案 '{input_file}'")
        input("\n按 Enter 鍵結束...")
        sys.exit(1)
    
    # 設定輸出檔案名稱
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}out.json"
    
    print(f"\n輸入檔案：{input_file}")
    print(f"輸出檔案：{output_file}")
    print()
    
    try:
        # 讀取余氏碼表
        print("正在載入余氏碼表...")
        yucode_map = load_yucode_dict('yus_candict_c.txt')
        print(f"已載入 {len(yucode_map)} 個漢字映射")
        
        print("\n正在讀取檔案...")
        
        # 判斷檔案類型
        if is_list_file(input_file):
            # 處理列表檔案
            data = process_list_file(input_file, yucode_map)
            poems = data
            print(f"處理了 {len(poems)} 個詩詞名稱")
        else:
            # 處理 JSON 詩詞檔案
            data = parse_poem_file(input_file)
            
            # 處理所有詩詞物件
            if isinstance(data, list):
                poems = data
            else:
                poems = [data]
            
            print(f"找到 {len(poems)} 首詩詞")
            
            # 為每個詩詞的每個句子生成 yucode
            for poem in poems:
                for sentence in poem.get('sentences', []):
                    text = sentence.get('text', '')
                    if text:
                        sentence['yucode'] = text_to_yucode(text, yucode_map)
        
        # 寫入輸出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            if len(poems) == 1 and not isinstance(poems, list):
                json.dump(poems, f, ensure_ascii=False, indent=4)
            else:
                json.dump(poems, f, ensure_ascii=False, indent=4)
        
        print(f"\n✅ 轉換完成！結果已儲存至 {output_file}")
        
        # 顯示轉換結果範例
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
                        print(f"   粵拼：{first['yucode']}")
                else:
                    print(f"{i+1}. {item.get('text', '')}")
                    print(f"   粵拼：{item.get('yucode', '')}")
                print()
            
    except Exception as e:
        print(f"\n❌ 錯誤：{e}")
    
    input("\n按 Enter 鍵結束...")

if __name__ == '__main__':
    main()