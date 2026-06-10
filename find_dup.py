with open('reneeyu_canph2345out_freqmerge.txt', 'r', encoding='utf-16') as f:
     seen = {} 
     duplicates = [] 
     for i, line in enumerate(f, 1): 
         if line.startswith('02'): 
             if line in seen: 
                 duplicates.append((i, line.strip())) 
             else: 
                 seen[line] = i 
     if duplicates: 
         print('找到以下重複的 02 開頭行：')
         for lineno, content in duplicates: 
             print(f'第 {lineno} 行 → {content}')
         print(f'\n總共 {len(duplicates)} 個重複的雙字詞行') 
     else: 
         print('沒有找到重複的 02 開頭行') 