import os
import re
import jieba

# 設定工作路徑
TARGET_DIR = r"C:\Users\Dad\OneDrive\eyuime"
OUTPUT_FILE = "POEM_PH2.TXT"

def is_valid_poem_word(word):
    """檢查是否為合格的詩詞繁體雙字詞（100%過濾簡體字）"""
    # 1. 必須剛好是兩個字，且必須全為中文
    if len(word) != 2 or not re.match(r'^[\u4E00-\u9FA5]{2}$', word):
        return False
        
    # 2. 嚴格繁體檢查（利用 Big5 編碼測試）
    for char in word:
        try:
            char.encode('big5')
            # 排除少數在 Big5 中存在、但在現代屬於簡體/俗字的特殊字外觀
            if char in "体双丰儿价广厂么叶":
                return False
        except UnicodeEncodeError:
            # 如果 Big5 編碼失敗，說明不是標準繁體字，直接剔除
            return False
            
    return True

def main():
    word_set = set()
    
    # 檢查路徑是否存在
    if not os.path.exists(TARGET_DIR):
        print(f"【錯誤】找不到指定的資料夾路徑：{TARGET_DIR}")
        return

    print(f"【掃描】正在自動尋找資料夾中以《 開頭的詩詞/歌詞檔案...")
    
    # 自動篩選出所有符合條件的檔案（不分大小寫的 .txt）
    all_files = os.listdir(TARGET_DIR)
    poem_files = [f for f in all_files if f.startswith("《") and f.lower().endswith(".txt")]
    
    if not poem_files:
        print("【提示】未找到任何以《 開頭的 .TXT 檔案，請確認檔案放置的路徑是否正確。")
        return
        
    print(f"【找到】共偵測到 {len(poem_files)} 個符合條件的文字檔：")
    for pf in poem_files:
        print(f"  -> {pf}")
        
    print("\n【處理】開始進行分詞與提煉...")
    
    # 依序讀取每個檔案
    for file_name in poem_files:
        file_path = os.path.join(TARGET_DIR, file_name)
        
        # 嘗試多種常見編碼讀取檔案，防止因檔案儲存格式不同而報錯
        content = ""
        for enc in ['utf-8', 'cp950', 'utf-16', 'gbk']:
            try:
                with open(file_path, "r", encoding=enc, errors="ignore") as f:
                    content = f.read()
                break # 讀取成功就跳出編碼嘗試
            except Exception:
                continue
                
        if not content.strip():
            print(f"  ⚠️ 檔案 {file_name} 讀取失敗或內容為空，已跳過。")
            continue
            
        # 使用 jieba 進行精準分詞
        words = jieba.cut(content)
        for word in words:
            if is_valid_poem_word(word):
                word_set.add(word)

    print(f"\n【統計】所有詩詞檔案處理完畢！共提煉出 {len(word_set)} 個不重複的繁體雙字詞。")
    
    # 進行排序，讓詞庫輸出時更美觀、更有規律
    final_words = sorted(list(word_set))
    
    # 導出 POEM_PH2.TXT
    output_path = os.path.join(TARGET_DIR, OUTPUT_FILE)
    print(f"【導出】正在寫入 {OUTPUT_FILE} (UTF-16 編碼，含6位數流水號)...")
    
    try:
        with open(output_path, "w", encoding="utf-16") as f:
            for i, word in enumerate(final_words, 1):
                f.write(f"{i:06d} {word}\n")
        print(f"✨ 恭喜！{OUTPUT_FILE} 已成功生成。檔案包含 {len(final_words)} 行。")
    except Exception as e:
        print(f"【錯誤】寫入檔案時發生問題：{e}")

if __name__ == "__main__":
    main()