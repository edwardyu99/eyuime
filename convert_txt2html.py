import sys
import os
import re 

def get_output_filename(input_file):
    base, _ = os.path.splitext(input_file)
    return base + ".html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-HK">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --primary-color: #1e293b;
            --secondary-color: #334155;
            --accent-color: #2563eb;
            --accent-light: #eff6ff;
            --tone1-color: #0d9488;
            --tone1-bg: #ccfbf1;
            --tone26-color: #d97706;
            --tone26-bg: #fef3c7;
            --tone4-color: #c026d3;
            --tone4-bg: #fae8ff;
            --bg-color: #f8fafc;
            --container-bg: #ffffff;
            --border-color: #cbd5e1;
            --text-color: #334155;
            --code-bg: #f1f5f9;
        }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang TC", "Microsoft JhengHei", sans-serif; background-color: var(--bg-color); color: var(--text-color); line-height: 1.7; margin: 0; padding: 30px 15px; font-size: 17px; }}
        .container {{ max-width: 1100px; margin: 0 auto; background: var(--container-bg); padding: 40px; border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); }}
        header {{ text-align: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 20px; margin-bottom: 35px; }}
        h1 {{ color: var(--primary-color); font-size: 2em; margin: 0 0 10px 0; }}
        .version {{ color: #64748b; font-size: 0.95em; font-weight: 500; }}
        .intro {{ background-color: var(--accent-light); border-left: 4px solid var(--accent-color); padding: 16px 20px; margin-bottom: 35px; border-radius: 0 8px 8px 0; color: #1e40af; font-weight: 500; }}
        h2 {{ color: var(--primary-color); border-bottom: 2px solid #e2e8f0; padding-bottom: 10px; margin-top: 40px; font-size: 1.4em; }}
        h3 {{ color: var(--secondary-color); font-size: 1.15em; margin-top: 25px; }}
        ul, ol {{ padding-left: 24px; }}
        li {{ margin-bottom: 14px; }}
        code {{ background-color: var(--code-bg); color: #b91c1c; padding: 2px 6px; border-radius: 4px; font-family: 'Consolas', 'Monaco', monospace; font-size: 0.92em; border: 1px solid #e2e8f0; }}
        .highlight {{ color: var(--accent-color); font-weight: 600; }}
        .table-container {{ overflow-x: auto; margin: 20px 0; border-radius: 8px; border: 1px solid var(--border-color); }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.92em; text-align: center; }}
        th, td {{ padding: 8px 12px; border: 1px solid var(--border-color); vertical-align: middle; }}
        th {{ background-color: #f1f5f9; color: var(--primary-color); font-weight: 600; }}
        .grid-table td {{ text-align: left; }}
        .notes-section {{ background-color: #fffbeb; border: 1px solid #fde68a; padding: 20px; border-radius: 8px; margin-top: 20px; font-size: 0.9em; }}
        .notes-section h4 {{ margin-top: 0; color: #b45309; font-size: 1.05em; margin-bottom: 12px; }}
        .note-item {{ margin-bottom: 10px; line-height: 1.6; }}
        .rule-table {{ width: 100%; border-collapse: separate; border-spacing: 0; background: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #cbd5e1; margin-bottom: 25px; text-align: left; }}
        .rule-table th {{ background-color: #1e293b; color: #ffffff; padding: 10px 14px; font-size: 0.92em; }}
        .rule-table td {{ padding: 8px 14px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #f1f5f9; }}
        .rule-table tr:hover {{ background-color: #f8fafc; }}
        .poem-section {{ background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 25px; border-radius: 12px; margin-top: 40px; text-align: center; }}
        .poem-title {{ color: #166534; font-size: 1.35em; font-weight: bold; margin-bottom: 20px; }}
        .poem-verse {{ margin-bottom: 20px; }}
        .pinyin-line {{ font-family: 'Consolas', monospace; color: #15803d; font-size: 0.95em; }}
        .hanzi-line {{ font-size: 1.2em; color: #14532d; font-weight: bold; letter-spacing: 2px; margin-top: 2px; }}
    </style>
</head>
<body>
    <div class="container">
{content}
    </div>
</body>
</html>
"""

def parse_ascii_table(table_text):
    """將 ASCII 網格表格轉換為 HTML 表格"""
    lines = [line.strip() for line in table_text.strip().split('\n') if '├' not in line and '└' not in line and '┌' not in line]
    html = ['<div class="table-container"><table class="grid-table"><tbody>']
    for line in lines:
        cells = [c.strip() for c in line.split('│') if c.strip() != '']
        if cells:
            html.append('<tr>')
            for cell in cells:
                formatted_cell = re.sub(r'([a-z/#0-9]+)', r'<code>\1</code>', cell)
                html.append(f'  <td>{formatted_cell}</td>')
            html.append('</tr>')
    html.append('</tbody></table></div>')
    return '\n'.join(html)

def parse_notes_block(notes_text, title_text="韻母與聲調備註說明"):
    """解析 [#x] 類型的備註說明"""
    items = re.split(r'(\[\#\d+\]：?)', notes_text.strip())
    html = ['<div class="notes-section">', f'<h4>{title_text}</h4>']
    
    i = 1
    while i < len(items):
        tag = items[i].strip().replace('：', '')
        content = items[i+1].strip() if i+1 < len(items) else ''
        content = re.sub(r'([a-zA-Z0-9\->]+)', r'<code>\1</code>', content)
        html.append(f'<div class="note-item"><strong>{tag}</strong> {content}</div>')
        i += 2
        
    html.append('</div>')
    return '\n'.join(html)

def parse_tone_matrix_table(t_text):
    """解析單字母韻母聲調對應表"""
    lines = [l.strip() for l in t_text.strip().split('\n') if l.strip()]
    if not lines:
        return ""
    
    html = ['<div class="table-container"><table class="rule-table">', '<thead><tr>']
    headers = lines[0].split()
    for h in headers:
        html.append(f'  <th>{h}</th>')
    html.append('</tr></thead><tbody>')
    
    for line in lines[1:]:
        tokens = line.split()
        if len(tokens) >= 15:
            row_label = f"{tokens[0]} {tokens[1]}"
            cols = [row_label] + tokens[2:]
        else:
            cols = tokens
            
        html.append('<tr>')
        for cell in cols:
            formatted = re.sub(r'([a-z0-9\-]+)', r'<code>\1</code>', cell)
            html.append(f'  <td>{formatted}</td>')
        html.append('</tr>')
        
    html.append('</tbody></table></div>')
    return '\n'.join(html)

def parse_plain_table(table_text):
    """將多空格或 Tab 對齊的文本表格轉為 HTML 表格"""
    lines = [l.strip() for l in table_text.strip().split('\n') if l.strip()]
    if not lines:
        return ""
    
    html = ['<div class="table-container"><table class="rule-table">', '<thead><tr>']
    
    # 支援 Tab 或多個空格分隔欄位
    if '\t' in lines[0]:
        headers = [h.strip() for h in lines[0].split('\t')]
    else:
        headers = [h.strip() for h in re.split(r'\s{2,}', lines[0])]
        
    for h in headers:
        html.append(f'  <th>{h}</th>')
    html.append('</tr></thead><tbody>')
    
    for line in lines[1:]:
        if '\t' in line:
            cells = [c.strip() for c in line.split('\t')]
        else:
            cells = [c.strip() for c in re.split(r'\s{2,}', line)]
            
        html.append('<tr>')
        for cell in cells:
            formatted = re.sub(r'([a-zA-Z0-9]+)', r'<code>\1</code>', cell) if cell else ""
            html.append(f'  <td>{formatted}</td>')
        html.append('</tr>')
        
    html.append('</tbody></table></div>')
    return '\n'.join(html)

def parse_section_three(sec_text):
    """解析 (三) 聲調 完整區塊"""
    html = ['<section>', '    <h2>🎵 (三) 聲調</h2>']
    
    # 1. 簡介文字
    intro_m = re.search(r'🎵 \(三\) 聲調\s*(.*?)(?=\(1\) 單字母韻母)', sec_text, re.DOTALL)
    if intro_m:
        p_str = re.sub(r'([a-zA-Z0-9\->]+)', r'<code>\1</code>', intro_m.group(1).strip())
        html.append(f'    <p>{p_str}</p>')
    
    # 2. (1) 單字母韻母
    html.append('    <h3>(1) 單字母韻母 (a e i o u)</h3>')
    
    t1_match = re.search(r'調類.*?陽去 6.*?\n', sec_text, re.DOTALL)
    if t1_match:
        html.append(parse_tone_matrix_table(t1_match.group(0)))
        
    notes_m = re.search(r'(\[\#9\].*?)(?=\(2\) 其他多字母韻母|$)', sec_text, re.DOTALL)
    if notes_m:
        html.append(parse_notes_block(notes_m.group(1), title_text="單字母聲調補充說明"))
        
    # 3. (2) 其他多字母韻母的處理
    html.append('    <h3>(2) 其他多字母韻母的處理</h3>')
    
    sec2_m = re.search(r'\(2\) 其他多字母韻母的處理(.*)', sec_text, re.DOTALL)
    if sec2_m:
        body = sec2_m.group(1).strip()
        # 相容空格與 Tab 分隔的表頭匹配
        header_match = re.search(r'韻母[\t ]+1聲', body)
        if header_match:
            table_start = header_match.start()
            intro_text = body[:table_start].strip()
            table_text = body[table_start:].strip()
            
            if intro_text:
                intro_fmt = re.sub(r'([a-zA-Z0-9\->]+)', r'<code>\1</code>', intro_text).replace('\n', '<br>')
                html.append(f'    <p>{intro_fmt}</p>')
            
            if table_text:
                html.append(parse_plain_table(table_text))
        else:
            body_fmt = re.sub(r'([a-zA-Z0-9\->]+)', r'<code>\1</code>', body).replace('\n', '<br>')
            html.append(f'    <p>{body_fmt}</p>')

    html.append('</section>')
    return '\n'.join(html)

def parse_poem_section(poem_lines):
    """解析結尾詩詞區塊"""
    html = ['<section class="poem-section">']
    title = ""
    verses = []
    
    i = 0
    while i < len(poem_lines):
        line = poem_lines[i].strip()
        if not line or line.startswith('ui poem'):
            i += 1
            continue
        if line.startswith('【') and '】' in line:
            title = line
            i += 1
            continue
        
        pinyin_line = line
        hanzi_line = poem_lines[i+1].strip() if i + 1 < len(poem_lines) else ""
        verses.append((pinyin_line, hanzi_line))
        i += 2

    html.append(f'    <div class="poem-title">{title}</div>')
    for pinyin, hanzi in verses:
        html.append('    <div class="poem-verse">')
        html.append(f'        <div class="pinyin-line">{pinyin}</div>')
        if hanzi:
            html.append(f'        <div class="hanzi-line">{hanzi}</div>')
        html.append('    </div>')
    html.append('</section>')
    return '\n'.join(html)

def convert_txt2html(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    html_parts = []
    
    # 1. 頁頭與簡介
    title_match = re.search(r'📘\s*(.*)', text)
    title = title_match.group(1).strip() if title_match else "余氏輸入法 3+3 拼音編碼說明"
    
    version_match = re.search(r'(版本：.*)', text)
    version = version_match.group(1).strip() if version_match else ""
    
    intro_match = re.search(r'(余氏詞庫雙字詞拼音是3\+3編碼。.*)', text)
    intro = intro_match.group(1).strip() if intro_match else ""

    html_parts.append(f"""<header>
    <h1>📘 {title}</h1>
    <p class="version">{version}</p>
</header>
<section class="intro">
    {intro}
</section>""")

    # 2. (一) 三碼簡化
    html_parts.append('<section>\n    <h2>🔤 (一) 三碼簡化</h2>\n    <ol>')
    items = re.findall(r'🔹 \d+\.\s*(.*?)(?=(🔹 \d+\.|\(二\)|$))', text, re.DOTALL)
    for item, _ in items:
        item_str = item.strip()
        item_str = re.sub(r'([a-zA-Z0-9\->]+)', r'<code>\1</code>', item_str)
        html_parts.append(f'        <li>{item_str}</li>')
    html_parts.append('    </ol>\n</section>')

    # 3. (二) 韻母及 ASCII 表格
    html_parts.append('<section>\n    <h2>🎵 (二) 韻母</h2>')
    ascii_table_match = re.search(r'┌.*?└─────────┘', text, re.DOTALL)
    if ascii_table_match:
        html_parts.append(parse_ascii_table(ascii_table_match.group(0)))

    notes_match = re.search(r'(\[\#1\].*?)(?=🎵 \(三\) 聲調|$)', text, re.DOTALL)
    if notes_match:
        html_parts.append(parse_notes_block(notes_match.group(1)))
    html_parts.append('</section>')

    # 4. (三) 聲調
    sec3_match = re.search(r'(🎵 \(三\) 聲調.*?)(?=ui poem|$)', text, re.DOTALL)
    if sec3_match:
        html_parts.append(parse_section_three(sec3_match.group(1)))

    # 5. 詩詞區塊
    poem_match = re.search(r'(ui poem.*$)', text, re.DOTALL)
    if poem_match:
        html_parts.append(parse_poem_section(poem_match.group(1).strip().split('\n')))

    full_content = '\n'.join(html_parts)
    final_html = HTML_TEMPLATE.format(title=title, content=full_content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)

if __name__ == "__main__":
    default_input = "余氏輸入法3-3拼音編碼說明.txt"

    if len(sys.argv) < 2:
        print("💡 用法: python convert_txt2html.py <輸入檔案.txt>")
        print(f"ℹ️ 未提供參數，預設使用：'{default_input}'\n")
        input_txt = default_input
    else:
        input_txt = sys.argv[1]

    output_html = get_output_filename(input_txt)
    convert_txt2html(input_txt, output_html)