import pandas as pd

# 1. 讀取原始的詞頻檔案（原始格式為 Tab 分隔）
input_file = "Cifu-v1.txt"
output_file = "Cifu_formatted.txt"

df = pd.read_csv(input_file, sep='\t')

# 2. 將資料寫入新的 TXT 檔案，並以 " | " 作為欄位分隔符號
with open(output_file, 'w', encoding='utf-8') as f:
    # 寫入標題列
    headers = df.columns.tolist()
    f.write(" | ".join(headers) + "\n")
    
    # 寫入一條分隔線，增強視覺可讀性
    f.write("-" * 150 + "\n")
    
    # 逐行寫入資料
    for idx, row in df.iterrows():
        row_str = " | ".join([str(val) for val in row.values])
        f.write(row_str + "\n")

print(f"轉換完成！新檔案已儲存至：{output_file}")