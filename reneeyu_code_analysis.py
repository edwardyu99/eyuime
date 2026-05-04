import codecs
import sys  # 新增：用於讀取命令列參數

def analyze_duplicate_codes(file_path, uncommon_rank_threshold=2000, diff_threshold=500):
    code_groups = {}

    # 讀取並分類數據[cite: 1]
    with codecs.open(file_path, 'r', encoding='utf-16') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            code, char, tone, rank = parts[0], parts[1], parts[2], parts[3]
            if code not in code_groups:
                code_groups[code] = []
            code_groups[code].append({'char': char, 'tone': tone, 'rank': rank})

    results = []
    for code, chars in code_groups.items():
        if len(chars) < 2:
            continue

        try:
            all_ranks = []
            for c in chars:
                try:
                    all_ranks.append(int(c['rank']))
                except ValueError:
                    all_ranks.append(9999)
            
            first_rank = all_ranks[0]
            min_rank_in_group = min(all_ranks)
            
            # 判斷邏輯：如果第一碼已是最小或差距在門檻內，則跳過[cite: 1]
            if first_rank <= min_rank_in_group or (first_rank - min_rank_in_group) < diff_threshold:
                continue
        except Exception:
            pass

        first = chars[0]
        reasons = []

        # 檢查常用字門檻[cite: 1]
        if first['rank'] == '9999':
            reasons.append("rank為9999（無頻率數據）")
        else:
            try:
                rank_num = int(first['rank'])
                if rank_num > uncommon_rank_threshold:
                    reasons.append(f"rank > {uncommon_rank_threshold} (實際 {rank_num})")
            except ValueError:
                reasons.append(f"rank無法解析 ({first['rank']})")

        # 檢查聲調[cite: 1]
        try:
            tone_num = int(first['tone'])
            if tone_num < 1 or tone_num > 6:
                reasons.append(f"聲調異常 ({tone_num})")
        except ValueError:
            reasons.append(f"聲調無法解析 ({first['tone']})")

        if reasons:
            all_chars_info = []
            for i, c in enumerate(chars):
                marker = "【第一重碼】" if i == 0 else ""
                all_chars_info.append(f"{marker}{c['char']}(聲調{c['tone']}, rank{c['rank']})")
            
            results.append({
                'code': code,
                'first_char': first['char'],
                'reason': '；'.join(reasons),
                'diff': first_rank - min_rank_in_group,
                'all_chars': all_chars_info,
                'total': len(chars)
            })

    results.sort(key=lambda x: x['code'])

    # 輸出分析結果[cite: 1]
    print("=" * 80)
    print(f"分析報告：第一重碼優化分析")
    print(f"- 常用字判定門檻 (rank): {uncommon_rank_threshold}")
    print(f"- 容許排序誤差 (diff): {diff_threshold}")
    print("=" * 80)
    print(f"共找到 {len(results)} 個符合條件的編碼組\n")

    for i, entry in enumerate(results, 1):
        print(f"{i}. 編碼: {entry['code']}")
        print(f"   第一重碼字: {entry['first_char']}")
        print(f"   原因: {entry['reason']} (與最優字差距: {entry['diff']})")
        print(f"   重碼總數: {entry['total']}")
        print(f"   所有重碼字:")
        for char_str in entry['all_chars']:
            print(f"     - {char_str}")
        print()

if __name__ == "__main__":
    # 預設值
    u_threshold = 2500
    d_threshold = 2000
    
    # 讀取命令列參數：sys.argv[0] 是檔名，[1] 是第一個參數，[2] 是第二個參數
    if len(sys.argv) > 1:
        try:
            u_threshold = int(sys.argv[1])
        except ValueError:
            print(f"警告: 無法解析門檻參數 '{sys.argv[1]}', 使用預設值 {u_threshold}")
            
    if len(sys.argv) > 2:
        try:
            d_threshold = int(sys.argv[2])
        except ValueError:
            print(f"警告: 無法解析差距參數 '{sys.argv[2]}', 使用預設值 {d_threshold}")

    # 執行分析
    analyze_duplicate_codes("reneeyu_head_az_out.txt", 
                            uncommon_rank_threshold=u_threshold, 
                            diff_threshold=d_threshold)