import os

def determine_line_vowel(code, num_chars):
    """
    依據詞彙字數將組合編碼拆解，只提取「首字」的 2-3 碼編碼，
    並依據「組名只能是 1-2 字母」的規則動態篩選出正確的韻母。
    """
    valid_splits = []
    
    # 透過 DFS 找出所有符合字數（每個字元 2~3 碼）的合法拆分
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
        fc = split[0]  # 只拿第一個單字的編碼（2 碼或 3 碼）
        
        # 提取韻母：若首字母為元音則取全部，否則去首字母
        if fc[0] in 'aeiou':
            vowel = fc
        else:
            vowel = fc[1:]
            
        # 核心修正：組名只能是 1-2 字母，不可能 3 字母。以此過濾掉錯誤的斷字
        if 1 <= len(vowel) <= 2:
            candidates.append((fc, vowel))
            
    # 如果嚴格拆分找不到任何符合的（防呆兜底邏輯）
    if not candidates:
        for l in [3, 2]:
            if len(code) >= l:
                fc = code[:l]
                vowel = fc if fc[0] in 'aeiou' else fc[1:]
                if 1 <= len(vowel) <= 2:
                    return vowel
        return "其他"
        
    # 排序：在合法的候選中，優先選擇首字編碼較長的（3碼 > 2碼），確保最長匹配
    candidates.sort(key=lambda x: len(x[0]), reverse=True)
    return candidates[0][1]

def main():
    input_file = "reneeyu_canph2345outdup.txt"
    output_file = "reneeyu_canph2345outdup_vowel.txt"
    
    print(f"正在讀取檔案 {input_file} (UTF-16)...")
    
    if not os.path.exists(input_file):
        print(f"錯誤：找不到檔案 {input_file}")
        return
        
    parsed_lines = []
    discovered_vowels = set()
    
    # 第一階段：動態分析檔案，搜集所有合法的韻母群組
    with open(input_file, "r", encoding="utf-16") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            parts = line_str.split()
            code = parts[0]
            words = parts[1:]
            
            if not words:
                continue
                
            num_chars = len(words[0])
            vowel = determine_line_vowel(code, num_chars)
            
            parsed_lines.append((code, line_str, vowel))
            discovered_vowels.add(vowel)
            
    # 第二階段：動態創建群組（依 A-Z 排序組名）
    sorted_vowels = sorted(list(discovered_vowels))
    groups = {v: [] for v in sorted_vowels}
    
    # 將資料分流
    for code, line_str, vowel in parsed_lines:
        groups[vowel].append((code, line_str))
        
    print(f"正在寫入排序後的資料至 {output_file}...")
    
    # 第三階段：寫入檔案
    with open(output_file, "w", encoding="utf-16") as f:
        for v in sorted_vowels:
            f.write(f'"{v}"組應是 ( 首字有"{v}")\n')
            # 群組內部依編碼 A-Z 排序
            sorted_lines = sorted(groups[v], key=lambda x: x[0])
            for code, original_line in sorted_lines:
                f.write(f"{original_line}\n")
            f.write("\n")
            
    print("處理完成！\n")
    
    # 第四階段：動態列出每組的行數
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

if __name__ == "__main__":
    main()

#-------------------------------------------------------------
