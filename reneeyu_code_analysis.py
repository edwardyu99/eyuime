import codecs

def analyze_duplicate_codes(file_path, uncommon_rank_threshold=3000):
    code_groups = {}

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
        first = chars[0]
        reasons = []

        if first['rank'] == '9999':
            reasons.append("rank為9999（無頻率數據）")
        else:
            try:
                rank_num = int(first['rank'])
                if rank_num > uncommon_rank_threshold:
                    reasons.append(f"rank > {uncommon_rank_threshold} (實際 {rank_num})")
            except ValueError:
                reasons.append(f"rank無法解析 ({first['rank']})")

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
                'all_chars': all_chars_info,
                'total': len(chars)
            })

    results.sort(key=lambda x: x['code'])

    print("=" * 80)
    print(f"第一重碼字非常用分析 (rank 門檻: {uncommon_rank_threshold})")
    print("=" * 80)
    print(f"共找到 {len(results)} 個符合條件的字組\n")

    for i, entry in enumerate(results, 1):
        if entry['total'] > 9:
            print(f"{i}. 編碼: {entry['code']}")
            print(f"   第一重碼字: {entry['first_char']}")
            print(f"   原因: {entry['reason']}")
            print(f"   重碼總數: {entry['total']}")
            print(f"   所有重碼字:")
            for char_str in entry['all_chars']:
            	print(f"     - {char_str}")
            print()

    print("=" * 80)
    print("統計摘要")
    print("=" * 80)
    print(f"總編碼數: {len(code_groups)}")
    multi = sum(1 for c in code_groups.values() if len(c) >= 2)
    print(f"有重碼的編碼數: {multi}")
    print(f"第一重碼為非常用字的編碼數: {len(results)}")

if __name__ == "__main__":
    analyze_duplicate_codes("reneeyu_head_az_out.txt", uncommon_rank_threshold=2500)