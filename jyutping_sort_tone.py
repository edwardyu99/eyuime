def sort_jyutping_dict(input_path="jyutping.txt", output_path="jyutping_sorted.txt"):
    with open(input_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\r\n") for line in f if line.strip()]

    header = lines[0]
    data_lines = lines[1:]

    def sort_key(line):
        parts = line.split("\t")
        ucode_str = parts[1].strip() if len(parts) > 1 else ""
        tone_str = parts[5].strip() if len(parts) > 5 else ""

        # UCODE 轉十六進位整數排序
        ucode_val = int(ucode_str.replace("U+", ""), 16) if ucode_str.startswith("U+") else 0
        
        # TONE 轉整數排序 (非數字/空值歸為 0 排最前)
        tone_val = int(tone_str) if tone_str.isdigit() else 0

        return (ucode_val, tone_val)

    sorted_data = sorted(data_lines, key=sort_key)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        for line in sorted_data:
            f.write(line + "\n")

if __name__ == "__main__":
    sort_jyutping_dict()