import codecs
import sys  # 用於讀取命令列參數

def analyze_duplicate_codes(file_path, uncommon_rank_threshold=2000, diff_threshold=500):
    """
    分析輸入檔中的重碼資料，篩選出第一重碼可能需要優化的編碼。

    參數:
        file_path (str): 輸入的 UTF-16 編碼文字檔路徑。
        uncommon_rank_threshold (int): 常用字判定門檻，rank 大於此值將被視為不常用。
        diff_threshold (int): 容許的排序誤差，若第一重碼與最優字的 rank 差距小於此值則跳過。
    """
    code_groups = {}  # 以編碼為鍵，存放該編碼下所有候選字的字典

    # 讀取並分類數據
    # 檔案格式預期為：每行有「編碼 漢字 聲調 頻率排名」以空白分隔
    with codecs.open(file_path, 'r', encoding='utf-16') as f:
        for line in f:
            line = line.strip()
            if not line:          # 跳過空行
                continue
            parts = line.split()
            if len(parts) < 4:    # 格式不完整則跳過
                continue
            code, char, tone, rank = parts[0], parts[1], parts[2], parts[3]
            if code not in code_groups:
                code_groups[code] = []
            # 將同一編碼下的所有字及其屬性加入列表
            code_groups[code].append({'char': char, 'tone': tone, 'rank': rank})

    results = []  # 存放需要優化的編碼組結果

    for code, chars in code_groups.items():
        # 跳過<10重碼  #只有一個候選字的不算重碼，跳過
        if len(chars) < 10: # 2:
            continue

        try:
            all_ranks = []  # 收集該編碼下所有字的 rank 數值
            for c in chars:
                try:
                    all_ranks.append(int(c['rank']))
                except ValueError:
                    # 若 rank 無法轉換為整數（例如為空或特殊值），視為極大值 9999
                    all_ranks.append(9999)
            
            first_rank = all_ranks[0]          # 原本排序中的第一個（即第一重碼）的 rank
            min_rank_in_group = min(all_ranks) # 該編碼下最高的頻率（最小的 rank 值）
            
            # 判斷邏輯：若第一重碼已經是頻率最高，或者與最高頻率的差距小於門檻，
            # 則認為排序尚可，不需特別列出，直接跳過
            if first_rank <= min_rank_in_group or (first_rank - min_rank_in_group) < diff_threshold:
                continue
        except Exception:
            # 任何意外情況都直接跳過，防止程式中斷
            pass

        # 從列表取得第一重碼資訊
        first = chars[0]
        reasons = []  # 儲存需要優化的原因

        # 檢查常用字門檻：rank 為 9999 表示完全無頻率數據
        if first['rank'] == '9999':
            reasons.append("rank為9999（無頻率數據）")
        else:
            try:
                rank_num = int(first['rank'])
                if rank_num > uncommon_rank_threshold:
                    # rank 超過門檻代表該字不常用，卻佔據了第一重碼的位置
                    reasons.append(f"rank > {uncommon_rank_threshold} (實際 {rank_num})")
            except ValueError:
                reasons.append(f"rank無法解析 ({first['rank']})")

        # 檢查聲調是否正常（假設合法範圍為 1~6）
        try:
            tone_num = int(first['tone'])
            if tone_num < 1 or tone_num > 6:
                reasons.append(f"聲調異常 ({tone_num})")
        except ValueError:
            reasons.append(f"聲調無法解析 ({first['tone']})")

        # 若有任何需優化的原因，則記錄此編碼組
        if reasons:
            all_chars_info = []  # 組裝該編碼下所有字的顯示字串
            for i, c in enumerate(chars):
                marker = "【第一重碼】" if i == 0 else ""
                all_chars_info.append(f"{marker}{c['char']}(聲調{c['tone']}, rank{c['rank']})")
            
            # 找出最優字資訊（rank 最小的字，如有多個則取第一個）
            min_index = all_ranks.index(min_rank_in_group)
            best_char = chars[min_index]['char']
            best_tone = chars[min_index]['tone']
            best_rank = chars[min_index]['rank']
            best_char_info = f"{best_char}(聲調{best_tone}, rank{best_rank})"
            
            results.append({
                'code': code,
                'first_char': first['char'],
                'reason': '；'.join(reasons),
                'diff': first_rank - min_rank_in_group,  # 第一重碼與最佳排名的差距
                'all_chars': all_chars_info,
                'total': len(chars),
                'best_char_info': best_char_info  # 儲存最優字資訊
            })

    # 依照編碼排序，讓輸出井然有序
    results.sort(key=lambda x: x['code'])

    # 開啟記錄檔，準備寫入報告
    with open('reneeyu_tonerank_analysis_log.txt', 'w', encoding='utf-8') as log_file:
        # 輔助函數：同時輸出到螢幕與記錄檔
        def log(message):
            print(message)
            log_file.write(message + '\n')

        # 輸出分析報告
        log("=" * 80)
        log(f"分析報告：第一重碼優化分析")
        log(f"- 常用字判定門檻 (rank): {uncommon_rank_threshold}")
        log(f"- 容許排序誤差 (diff): {diff_threshold}")
        log("=" * 80)
        log(f"共找到 {len(results)} 個符合條件的編碼組\n")

        for i, entry in enumerate(results, 1):
            log(f"{i}. 編碼: {entry['code']}")
            log(f"   第一重碼字: {entry['first_char']}")
            log(f"   原因: {entry['reason']} (與最優字 {entry['best_char_info']} 差距: {entry['diff']})")
            log(f"   重碼總數: {entry['total']}")
            log(f"   所有重碼字:")
            for char_str in entry['all_chars']:
                log(f"     - {char_str}")
            log("")  # 空行分隔各組

if __name__ == "__main__":
    # 預設的門檻值，可透過命令列參數覆蓋
    u_threshold = 1000 #2500   # 常用字 rank 上限
    d_threshold = 500  #2000   # 允許的 rank 差距
    
    # 讀取命令列參數：sys.argv[0] 是程式本身，[1] 是第一參數（常用字門檻），[2] 是第二參數（允許差距）
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

    # 執行分析，輸入檔固定為 "reneeyu_head_az_out.txt"
    analyze_duplicate_codes("reneeyu_head_az_out.txt", 
                            uncommon_rank_threshold=u_threshold, 
                            diff_threshold=d_threshold)