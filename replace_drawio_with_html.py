#!/usr/bin/env python3
"""
Заменяет @drawio{} ссылки на прямые HTML iframe блоки
Работает без preprocessor - более простое и надежное решение
"""

import re
from pathlib import Path

def convert_github_to_raw(github_url):
    """Конвертирует GitHub URL в raw URL"""
    return github_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

def create_iframe_html(url):
    """Создает HTML iframe для Draw.io viewer"""
    raw_url = convert_github_to_raw(url)
    return f'''<iframe class="drawio-viewer" style="width: 100%; height: 800px; min-height: 600px; border: 1px solid #ddd; border-radius: 4px; margin: 20px 0;" src="https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=diagram&url={raw_url}"></iframe>'''

def process_file(filepath):
    """Обрабатывает один markdown файл"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Заменяем @drawio{URL} на HTML iframe
    pattern = r'@drawio\{(https://github\.com/[^\s}]+\.drawio)\}'
    content = re.sub(pattern, lambda m: create_iframe_html(m.group(1)), content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """Обрабатывает все markdown файлы"""
    src_dir = Path('src')
    md_files = list(src_dir.rglob('*.md'))
    
    print(f"Found {len(md_files)} markdown files")
    
    changed_count = 0
    for md_file in md_files:
        if process_file(md_file):
            print(f"Updated: {md_file}")
            changed_count += 1
    
    print(f"\nUpdated {changed_count} files with HTML iframes")

if __name__ == '__main__':
    main()
