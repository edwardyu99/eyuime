#!/usr/bin/env python3
import sys
import os
import difflib

def compare_utf16_files(file1_path, file2_path, output_path="reneeyu_canph2345ori_diff.txt"):
    # Ensure both input files exist
    if not os.path.exists(file1_path):
        print(f"Error: File '{file1_path}' does not exist.")
        sys.exit(1)
    if not os.path.exists(file2_path):
        print(f"Error: File '{file2_path}' does not exist.")
        sys.exit(1)

    print(f"Reading and decoding '{file1_path}'...")
    try:
        # 'utf-16' codec automatically handles the BOM (Byte Order Mark)
        with open(file1_path, 'r', encoding='utf-16') as f1:
            file1_lines = f1.readlines()
    except Exception as e:
        print(f"Failed to read {file1_path} with UTF-16: {e}")
        sys.exit(1)

    print(f"Reading and decoding '{file2_path}'...")
    try:
        with open(file2_path, 'r', encoding='utf-16') as f2:
            file2_lines = f2.readlines()
    except Exception as e:
        print(f"Failed to read {file2_path} with UTF-16: {e}")
        sys.exit(1)

    print("Comparing files and generating unified diff...")
    
    # Generate a standardized unified difference comparison
    diff = difflib.unified_diff(
        file1_lines,
        file2_lines,
        fromfile=os.path.basename(file1_path),
        tofile=os.path.basename(file2_path),
        lineterm=''
    )
    
    # Convert generator output to list
    diff_list = list(diff)

    if not diff_list:
        print("No differences found. The files are identical.")
        # Create an empty or status output file anyway to confirm completion
        with open(output_path, 'w', encoding='utf-16') as out_f:
            out_f.write("No differences found. Both files are completely identical.\n")
    else:
        print(f"Writing differences to '{output_path}'...")
        try:
            with open(output_path, 'w', encoding='utf-16') as out_f:
                for line in diff_list:
                    out_f.write(line + '\n')
            print("Comparison successfully completed!")
        except Exception as e:
            print(f"Failed to write output file: {e}")
            sys.exit(1)

if __name__ == "__main__":
    # Check if correct number of arguments are passed
    if len(sys.argv) < 3:
        print("Usage: python compare_txt.py <file1> <file2>")
        print("Example: python reneeyu_canph2345_compare.py reneeyu_canph2345ori_bef88.txt reneeyu_canph2345ori.txt")
        sys.exit(1)
        
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    
    compare_utf16_files(f1, f2)