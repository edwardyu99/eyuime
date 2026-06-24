import requests
import json
import re
import time

def get_hk_wikipedia_corpus(output_file="hk_corpus_text.txt", max_pages=150):
    print("【啟動】開始透過維基百科 API 下載高質量香港書面語料...")
    
    # 使用維基百科官方 API (指定中文語系)
    api_url = "https://zh.wikipedia.org/w/api.php"
    
    # 核心搜尋關鍵字，確保涵蓋政府、新聞、刊物、歷史與論文探討內容
    search_keywords = ["香港政府", "香港經濟", "香港歷史", "香港法律", "香港都市規劃", "香港教育", "香港醫療"]
    
    # 為了避免重覆下載相同頁面
    processed_ids = set()
    total_chars = 0
    
    headers = {
        "User-Agent": "HKCorpusBuilder/1.0 (contact: your_email@example.com) Python-requests"
    }

    with open(output_file, "w", encoding="utf-8") as f:
        for keyword in search_keywords:
            print(f"\n正在搜尋關鍵字：【{keyword}】相關的深度條目...")
            
            # 1. 搜尋相關條目列表
            search_params = {
                "action": "query",
                "list": "search",
                "srsearch": keyword,
                "srlimit": 40,  # 每個關鍵字抓取前 40 個深度條目
                "format": "json"
            }
            
            try:
                res = requests.get(api_url, params=search_params, headers=headers, timeout=10)
                search_data = res.json()
                search_results = search_data.get("query", {}).get("search", [])
                
                # 2. 逐一獲取這些條目的「純文字內文」
                for item in search_results:
                    page_id = item.get("pageid")
                    title = item.get("title")
                    
                    if page_id in processed_ids:
                        continue
                    processed_ids.add(page_id)
                    
                    # 抓取內文純文字 (explaintext=1 會自動去掉 HTML 標籤、側欄與圖片)
                    content_params = {
                        "action": "query",
                        "prop": "extracts",
                        "pageids": page_id,
                        "explaintext": 1,
                        "format": "json"
                    }
                    
                    c_res = requests.get(api_url, params=content_params, headers=headers, timeout=10)
                    c_data = c_res.json()
                    
                    pages = c_data.get("query", {}).get("pages", {})
                    page_content = pages.get(str(page_id), {}).get("extract", "")
                    
                    if page_content:
                        # 簡單清洗：只保留中文字、標點和換行
                        clean_content = re.sub(r'[^\u4E00-\u9FA5\n，。？；：！「」]', '', page_content)
                        f.write(f"=== {title} ===\n")
                        f.write(clean_content + "\n\n")
                        
                        total_chars += len(clean_content)
                        print(f"  -> 已成功寫入條目: 《{title}》 ({len(clean_content)} 字)")
                        
                    # 禮貌爬取，每次稍微停頓，避免給伺服器造成負擔
                    time.sleep(0.3)
                    
                    if len(processed_ids) >= max_pages:
                        break
            except Exception as e:
                print(f"擷取關鍵字 {keyword} 時發生錯誤: {e}")
                continue
                
            if len(processed_ids) >= max_pages:
                break

    print("\n" + "="*50)
    print(f"【大功告成】語料庫建立完畢！")
    print(f"檔案路徑: {output_file}")
    print(f"共下載了 {len(processed_ids)} 個深度百科條目")
    print(f"總計獲得 {total_chars} 個標準香港繁體中文字元")
    print("="*50)
    print("現在你可以直接執行分詞腳本，提取 7-9 萬個雙字詞了！")

if __name__ == "__main__":
    get_hk_wikipedia_corpus()