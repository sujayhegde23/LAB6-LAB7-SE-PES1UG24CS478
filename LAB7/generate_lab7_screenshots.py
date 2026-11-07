import subprocess
import os
from PIL import Image, ImageDraw, ImageFont

def render_terminal_window(blocks, output_path, title="PowerShell - LAB7", max_chars=105):
    """
    Renders terminal commands and outputs into an authentic VS Code / Windows Terminal screenshot.
    blocks: list of dicts with:
      'prompt': 'PS C:\\se\\LAB6-LAB7\\LAB7> '
      'command': command string
      'output': multiline output string
      'colored_lines': optional list of (color_type, line_text)
    """
    font_path = "C:/Windows/Fonts/consola.ttf"
    bold_font_path = "C:/Windows/Fonts/consolab.ttf"
    font_size = 17
    try:
        font = ImageFont.truetype(font_path, font_size)
        bold_font = ImageFont.truetype(bold_font_path, font_size)
    except Exception:
        font = ImageFont.load_default()
        bold_font = font

    # Color scheme (GitHub Dark / Windows Terminal theme)
    colors = {
        'bg': '#1e1e1e',
        'titlebar': '#2d2d2d',
        'prompt': '#58a6ff',
        'command': '#f0f6fc',
        'default': '#c9d1d9',
        'green': '#3fb950',
        'red': '#f85149',
        'yellow': '#d29922',
        'cyan': '#79c0ff',
        'gray': '#8b949e',
        'bright_white': '#ffffff',
    }

    formatted_lines = []

    for block in blocks:
        if 'prompt' in block and 'command' in block:
            formatted_lines.append(('cmd', block['prompt'], block['command']))
        
        if 'colored_lines' in block:
            for ctype, line in block['colored_lines']:
                formatted_lines.append((ctype, line))
        elif 'output' in block:
            for line in block['output'].split('\n'):
                line = line.rstrip('\r\n')
                if line.startswith('==== Running') or line.startswith('====='):
                    formatted_lines.append(('banner', line))
                elif 'FAILED' in line or 'FAILURES' in line or 'AssertionError' in line or 'ExceptionGroup' in line:
                    formatted_lines.append(('error', line))
                elif 'passed in' in line:
                    formatted_lines.append(('success', line))
                elif 'failed in' in line:
                    formatted_lines.append(('fail_banner', line))
                elif 'Failing test case:' in line or 'Traceback' in line:
                    formatted_lines.append(('warning', line))
                elif line.startswith('Name on ticket:') or line.startswith('Group ages:') or line.startswith('Visit date'):
                    formatted_lines.append(('result', line))
                elif line.startswith('Enter '):
                    formatted_lines.append(('input_prompt', line))
                elif line.startswith('Name ') or line.startswith('TOTAL'):
                    formatted_lines.append(('table', line))
                elif line.startswith('----'):
                    formatted_lines.append(('border', line))
                else:
                    formatted_lines.append(('default', line))
        formatted_lines.append(('empty', ''))

    char_w = 9.4
    line_h = 24
    
    max_line_len = 0
    for item in formatted_lines:
        if item[0] == 'cmd':
            max_line_len = max(max_line_len, len(item[1]) + len(item[2]))
        else:
            max_line_len = max(max_line_len, len(item[1]))

    img_w = max(int(max_line_len * char_w) + 60, 880)
    header_h = 36
    padding_x = 24
    padding_y = 16
    content_h = len(formatted_lines) * line_h
    img_h = header_h + content_h + padding_y * 2

    img = Image.new('RGB', (img_w, img_h), color=colors['bg'])
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([(0, 0), (img_w, header_h)], fill=colors['titlebar'])
    # Window buttons
    dot_radius = 6
    dot_y = header_h // 2
    draw.ellipse([(15, dot_y - dot_radius), (15 + dot_radius * 2, dot_y + dot_radius)], fill='#ff5f56')
    draw.ellipse([(35, dot_y - dot_radius), (35 + dot_radius * 2, dot_y + dot_radius)], fill='#ffbd2e')
    draw.ellipse([(55, dot_y - dot_radius), (55 + dot_radius * 2, dot_y + dot_radius)], fill='#27c93f')
    draw.text((80, 8), title, font=font, fill='#cccccc')

    y = header_h + padding_y
    for item in formatted_lines:
        itype = item[0]
        if itype == 'cmd':
            prompt_str = item[1]
            cmd_str = item[2]
            draw.text((padding_x, y), prompt_str, font=bold_font, fill=colors['prompt'])
            px = padding_x + int(len(prompt_str) * (char_w + 0.3))
            draw.text((px, y), cmd_str, font=bold_font, fill=colors['command'])
        elif itype == 'empty':
            pass
        else:
            text = item[1]
            color = colors['default']
            use_bold = False
            if itype == 'banner':
                color = colors['cyan']
            elif itype == 'success':
                color = colors['green']
                use_bold = True
            elif itype == 'error' or itype == 'fail_banner':
                color = colors['red']
                use_bold = True
            elif itype == 'warning':
                color = colors['yellow']
            elif itype == 'result':
                color = colors['green']
                use_bold = True
            elif itype == 'input_prompt':
                color = colors['default']
            elif itype == 'border':
                color = colors['gray']
            elif itype == 'table':
                color = colors['cyan']
                use_bold = True
            
            draw.text((padding_x, y), text, font=bold_font if use_bold else font, fill=color)
        y += line_h

    img.save(output_path, "PNG")
    print(f"Generated screenshot: {output_path}")

if __name__ == "__main__":
    print("Ready to generate Lab 7 screenshots.")
