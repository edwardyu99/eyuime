import os
from collections import Counter, defaultdict

def get_char_codes(code, num_chars):
    """
    將組合編碼拆解為每個單字對應的獨立 YUCODE（每字 2-3 碼）。
    """
    valid_splits = []
    
    def dfs(s, chars_left, current_split):
        if chars_left == 0:
            if len(s) == 0:
                valid_splits.append(current_split)
            return
        if len(s) == 0:
            return
        for l in range(2, min(3, len(s)) + 1):
            dfs(s[l:], chars_left - 1, current_split + [s[:l]])
            
    dfs(code, num_chars, [])
    
    candidates = []
    for split in valid_splits:
        valid = True
        for chunk in split:
            vowel = chunk if chunk[0] in 'aeiou' else chunk[1:]
            if not (1 <= len(vowel) <= 2):
                valid = False
                break
        if valid:
            candidates.append(split)
            
    if candidates:
        return candidates[0]
    if valid_splits:
        return valid_splits[0]
    return None

def determine_line_vowel(code, num_chars):
    """
    依據詞彙字數將組合編碼拆解，只提取「首字」的 2-3 碼編碼，
    並依據「組名只能是 1-2 字母」的規則動態篩選出正確的韻母。
    摘要行（如 1. 2. 等）會自動歸類至 "." 組。
    """
    char_codes = get_char_codes(code, num_chars)
    if char_codes:
        fc = char_codes[0]
        vowel = fc if fc[0] in 'aeiou' else fc[1:]
        if 1 <= len(vowel) <= 2:
            return vowel
            
    for l in [3, 2]:
        if len(code) >= l:
            fc = code[:l]
            vowel = fc if fc[0] in 'aeiou' else fc[1:]
            if 1 <= len(vowel) <= 2:
                return vowel
    return "其他"

def main():
    input_file = "reneeyu_canph2345outdup.txt"
    output_file = "reneeyu_canph2345outdup_vowel.txt"
    
    print(f"正在讀取檔案 {input_file}...")
    
    if not os.path.exists(input_file):
        print(f"錯誤：找不到檔案 {input_file}")
        return
        
    parsed_lines = []
    discovered_vowels = set()
    dup_counter = Counter()  # 紀錄產生重碼的單字次數
    char_yucode_counts = defaultdict(Counter)  # 紀錄每個單字對應的 YUCODE 出現頻率
    total_dup_lines = 0     # 紀錄重碼行數
    
    # 嘗試 UTF-16 / UTF-8 編碼讀取
    encodings = ['utf-16', 'utf-8']
    lines = None
    for enc in encodings:
        try:
            with open(input_file, "r", encoding=enc) as f:
                lines = f.readlines()
            print(f"成功使用 {enc} 解碼檔案。")
            break
        except UnicodeDecodeError:
            continue
            
    if lines is None:
        print("錯誤：無法順利解碼檔案，請檢查檔案編碼。")
        return

    # 第一階段：動態分析檔案，搜集韻母群組（保留摘要行歸類至 "." 組）並統計重碼單字與其 YUCODE
    for line in lines:
        line_str = line.strip()
        # 僅過濾空行與分隔線，不跳過以數字開頭的摘要行
        if not line_str or line_str.startswith('--'):
            continue
        parts = line_str.split()
        if len(parts) < 2:
            continue
            
        code = parts[0]
        words = parts[1:]
        
        has_duplicate = len(words) > 1
        if has_duplicate:
            total_dup_lines += 1
            for word in words:
                char_codes = get_char_codes(code, len(word))
                for idx, char in enumerate(word):
                    dup_counter[char] += 1
                    if char_codes and idx < len(char_codes):
                        char_yucode_counts[char][char_codes[idx]] += 1
                        
        num_chars = len(words[0])
        vowel = determine_line_vowel(code, num_chars)
        
        parsed_lines.append((code, line_str, vowel))
        discovered_vowels.add(vowel)
            
    # 第二階段：動態創建群組（依 ASCII 排序，"." 會自動排在首位）
    sorted_vowels = sorted(list(discovered_vowels))
    groups = {v: [] for v in sorted_vowels}
    
    for code, line_str, vowel in parsed_lines:
        groups[vowel].append((code, line_str))
        
    print(f"正在寫入排序後的資料與附件至 {output_file}...")
    
    # 第三階段：寫入檔案（包含主資料與附件 Top 50）
    with open(output_file, "w", encoding="utf-16") as f:
        # 1. 寫入各韻母分組資料
        for v in sorted_vowels:
            count = len(groups[v])
            f.write(f'"{v}"組應是 ( 首字有"{v}") ：{count} 行\n')
            sorted_lines = sorted(groups[v], key=lambda x: x[0])
            for code, original_line in sorted_lines:
                f.write(f"{original_line}\n")
            f.write("\n")
            
        # 2. 寫入附件：首 50 個最多產生重碼的單字列表（含 YUCODE）
        top50_dup = dup_counter.most_common(50)
        f.write("=" * 55 + "\n")
        f.write("附件：首 50 個最多產生重碼的單字列表\n")
        f.write("=" * 55 + "\n")
        f.write(f"（統計說明：共分析 {total_dup_lines} 行產生重碼的編碼組合）\n\n")
        f.write(f"{'排名':<6}{'單字':<6}{'YUCODE':<10}{'重碼出現次數':<12}\n")
        f.write("-" * 45 + "\n")
        for rank, (char, count) in enumerate(top50_dup, 1):
            yucode = char_yucode_counts[char].most_common(1)[0][0] if char_yucode_counts[char] else "未知"
            f.write(f"第 {rank:2d} 名： {char:<3} {yucode:<8} (重碼出現 {count} 次)\n")
        f.write("=" * 55 + "\n")
            
    print("處理完成！\n")
    
    # 第四階段：控制台完整輸出（包含 "." 組統計 + Top 50 預覽）
    print("=" * 30)
    print(" 各組行數統計結果：")
    print("=" * 30)
    total_rows = 0
    for v in sorted_vowels:
        count = len(groups[v])
        print(f' "{v}" 組：{count} 行')
        total_rows += count
    print("-" * 30)
    print(f' 總計處理：{total_rows} 行')
    print("=" * 30)
    
    print("\n" + "=" * 45)
    print(" 附件：首 50 個最多產生重碼的單字 (含 YUCODE)")
    print("=" * 45)
    top50_dup = dup_counter.most_common(50)
    for rank, (char, count) in enumerate(top50_dup, 1):
        yucode = char_yucode_counts[char].most_common(1)[0][0] if char_yucode_counts[char] else "未知"
        print(f"  第 {rank:2d} 名： {char} {yucode:<5} (重碼出現 {count} 次)")
    print("=" * 45)

if __name__ == "__main__":
    main()