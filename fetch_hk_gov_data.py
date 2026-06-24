import requests
import json

def fetch_hk_gov_data(output_file="hk_corpus_text.txt"):
    print("正在從香港政府開放數據下載新聞公報語料...")
    
    url = "https://www.news.gov.hk/tc/common/html/ticker.json"
    
    # 關鍵修正：加入 User-Agent，偽裝成一般 Windows 的 Chrome 瀏覽器
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # 測試回傳的是不是標準 JSON
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("\n【連線成功，但被防火牆攔截！】")
            print("伺服器沒有回傳 JSON。回傳的網頁內容前 200 字如下（通常是 Access Denied）：")
            print("-" * 50)
            print(response.text[:200].strip())
            print("-" * 50)
            print("建議：請直接使用下方的『步驟二』獲取海量歷史文本。")
            return
        
        with open(output_file, "w", encoding="utf-8") as f:
            count = 0
            for item in data:
                title = item.get("title", "")
                summary = item.get("description", "")
                
                if title:
                    f.write(title + "\n")
                    count += 1
                if summary:
                    f.write(summary + "\n")
                    
        print(f"成功下載並生成 {output_file}，共寫入 {count} 條當日新聞。")
        
    except Exception as e:
        print(f"下載失敗: {e}")

if __name__ == "__main__":
    fetch_hk_gov_data()