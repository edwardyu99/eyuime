import json
import re

def load_yucode_dict(filepath='yus_candict_c.txt'):
    """
    讀取余氏碼表，建立漢字到粵拼的映射字典
    """
    yucode_map = {}
    
    encodings = ['utf-16', 'utf-8', 'gbk', 'big5', 'gb2312', 'utf-16-le', 'utf-16-be']
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
                print(f"成功使用 {encoding} 編碼讀取檔案")
                
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
        elif char in '，。？、；：「」『』！':
            # 保留中文標點符號
            pass  # 不加入結果中，保持原有格式
        else:
            # 未知字符保留原樣
            result.append(char)
    return ' '.join(result)

def parse_poem_file(filepath='poem.txt'):
    """解析詩詞檔案，處理可能的不完整 JSON 格式"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
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

def main():
    # 讀取余氏碼表
    print("正在載入余氏碼表...")
    yucode_map = load_yucode_dict('yus_candict_c.txt')
    print(f"已載入 {len(yucode_map)} 個漢字映射")
    
    # 讀取並解析詩詞檔案
    print("\n正在讀取詩詞檔案...")
    data = parse_poem_file('poem.txt')
    
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
    with open('poemout.txt', 'w', encoding='utf-8') as f:
        if len(poems) == 1:
            json.dump(poems[0], f, ensure_ascii=False, indent=4)
        else:
            json.dump(poems, f, ensure_ascii=False, indent=4)
    
    print("\n轉換完成！結果已儲存至 poemout.txt")
    
    # 顯示第一首詩的轉換結果範例
    if poems and 'sentences' in poems[0]:
        print("\n轉換範例（第一句）：")
        first_sentence = poems[0]['sentences'][0]
        print(f"原文：{first_sentence['text']}")
        print(f"粵拼：{first_sentence['yucode']}")

if __name__ == '__main__':
    main()