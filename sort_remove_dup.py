file_path = 'sample.txt'

# Read all lines
with open(file_path, 'r', encoding='utf-16') as f:
    lines = f.readlines()

input_count = len(lines)

# Track duplicates and keep first occurrence
seen = {}
duplicates = {}
unique_lines = []

for line in lines:
    if line in seen:
        duplicates[line] = duplicates.get(line, 1) + 1
    else:
        seen[line] = True
        unique_lines.append(line)

# Sort the unique lines
unique_lines.sort()

output_count = len(unique_lines)

# Write back to file
with open(file_path, 'w', encoding='utf-16') as f:
    f.writelines(unique_lines)

# === Report ===
print("=" * 50)
print(f"File         : {file_path}")
print(f"Input lines  : {input_count:,}")
print(f"Output lines : {output_count:,}")
print(f"Duplicates removed : {input_count - output_count:,}")
print("=" * 50)

if duplicates:
    print(f"\nDuplicated lines found ({len(duplicates)} unique duplicated lines):")
    for line, count in duplicates.items():
        clean_line = line.strip()
        display = clean_line[:77] + "..." if len(clean_line) > 80 else clean_line
        print(f"  • {display}  (appeared {count + 1} times)")
else:
    print("\nNo duplicates found.")