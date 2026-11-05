import subprocess
import re
from PIL import Image, ImageDraw, ImageFont

def render_terminal_screenshot(command_blocks, output_path, title="PowerShell - LAB6"):
    """
    command_blocks: list of dicts:
      {
         'prompt': 'PS C:\\se\\LAB6-LAB7\\LAB6> ',
         'command': 'coverage run ...',
         'output': '...',
      }
    """
    font_path = "C:/Windows/Fonts/consola.ttf"
    font_size = 17
    try:
        font = ImageFont.truetype(font_path, font_size)
        bold_font = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()
        bold_font = font

    # Format lines to draw
    # Each line is a tuple: (type, text)
    # types: 'prompt', 'command', 'pytest_header', 'pytest_pass', 'table_header', 'table_line', 'table_total', 'normal'
    formatted_lines = []
    
    for block in command_blocks:
        formatted_lines.append(('command_line', block['prompt'], block['command']))
        raw_output = block['output'].strip('\r\n')
        if raw_output:
            for line in raw_output.split('\n'):
                line = line.rstrip('\r\n')
                if line.startswith('='):
                    formatted_lines.append(('pytest_banner', line))
                elif 'passed' in line:
                    formatted_lines.append(('pytest_pass', line))
                elif line.startswith('Name') and 'Stmts' in line:
                    formatted_lines.append(('table_header', line))
                elif line.startswith('----'):
                    formatted_lines.append(('table_border', line))
                elif line.startswith('TOTAL'):
                    formatted_lines.append(('table_total', line))
                elif '100%' in line:
                    formatted_lines.append(('table_row_100', line))
                else:
                    formatted_lines.append(('normal', line))
        formatted_lines.append(('empty', ''))

    # Calculate dimensions
    char_w = 9.4
    line_h = 24
    max_len = 0
    for item in formatted_lines:
        if item[0] == 'command_line':
            max_len = max(max_len, len(item[1]) + len(item[2]))
        else:
            max_len = max(max_len, len(item[1]))

    img_w = max(int(max_len * char_w) + 70, 850)
    header_h = 36
    padding_x = 25
    padding_y = 15
    content_h = len(formatted_lines) * line_h
    img_h = header_h + content_h + padding_y * 2

    # Create image
    img = Image.new('RGB', (img_w, img_h), color='#1e1e1e')
    draw = ImageDraw.Draw(img)

    # Window titlebar
    draw.rectangle([(0, 0), (img_w, header_h)], fill='#2d2d2d')
    # Window controls (red, yellow, green dots)
    dot_radius = 6
    dot_y = header_h // 2
    draw.ellipse([(15, dot_y - dot_radius), (15 + dot_radius * 2, dot_y + dot_radius)], fill='#ff5f56')
    draw.ellipse([(35, dot_y - dot_radius), (35 + dot_radius * 2, dot_y + dot_radius)], fill='#ffbd2e')
    draw.ellipse([(55, dot_y - dot_radius), (55 + dot_radius * 2, dot_y + dot_radius)], fill='#27c93f')

    # Window title text
    title_font = font
    draw.text((80, 8), title, font=title_font, fill='#cccccc')

    # Content
    y = header_h + padding_y
    for item in formatted_lines:
        itype = item[0]
        if itype == 'command_line':
            prompt_str = item[1]
            cmd_str = item[2]
            draw.text((padding_x, y), prompt_str, font=bold_font, fill='#58a6ff')
            px = padding_x + int(len(prompt_str) * (char_w + 0.3))
            draw.text((px, y), cmd_str, font=bold_font, fill='#f0f6fc')
        elif itype == 'pytest_banner':
            draw.text((padding_x, y), item[1], font=font, fill='#58a6ff')
        elif itype == 'pytest_pass':
            draw.text((padding_x, y), item[1], font=bold_font, fill='#3fb950')
        elif itype == 'table_header':
            draw.text((padding_x, y), item[1], font=bold_font, fill='#79c0ff')
        elif itype == 'table_border':
            draw.text((padding_x, y), item[1], font=font, fill='#6e7681')
        elif itype == 'table_total':
            draw.text((padding_x, y), item[1], font=bold_font, fill='#56d364')
        elif itype == 'table_row_100':
            draw.text((padding_x, y), item[1], font=font, fill='#e6edf3')
        elif itype == 'normal':
            draw.text((padding_x, y), item[1], font=font, fill='#c9d1d9')
        elif itype == 'empty':
            pass
        y += line_h

    img.save(output_path, "PNG")
    print(f"Saved terminal screenshot to {output_path}")

if __name__ == '__main__':
    print("Screenshot helper module loaded.")
