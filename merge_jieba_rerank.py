import os

# --- Configuration ---
input_file = 'merge_jieba.txt'
output_file = 'merge_jieba_ranked.txt'
#input_file = 'merge_jieba.txt'
#output_file = 'merge_jieba_ranked.txt'

# Note: If your file requires UTF-16, change encoding to 'utf-16'
file_encoding = 'utf-16' 

def reassign_ranks():
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    print(f"Reading '{input_file}' and reassigning ranks...")
    row_number = 1

    with open(input_file, 'r', encoding=file_encoding) as f_in, \
         open(output_file, 'w', encoding=file_encoding) as f_out:
        
        for line in f_in:
            # Skip empty lines
            if not line.strip():
                continue
            
            # column 1-6 (index 0 to 6) is the old rank/index
            # line[6:] preserves everything after the rank (the space and the word/phrase)
            remaining_content = line[6:]
            
            # Generate the new 6-digit zero-padded row number
            new_rank = f"{row_number:06d}"
            
            # Write out the updated line
            f_out.write(f"{new_rank}{remaining_content}")
            row_number += 1

    print(f"Successfully processed {row_number - 1} rows!")
    print(f"Output saved to: '{output_file}'")

if __name__ == "__main__":
    reassign_ranks()