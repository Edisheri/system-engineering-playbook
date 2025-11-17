#!/usr/bin/env python3
"""
Скрипт для исправления наложения текста в Draw.io файлах
Увеличивает расстояния между элементами и размеры текстовых блоков
"""

import re
import os
from pathlib import Path

def fix_drawio_file(filepath):
    """Исправляет наложение текста в Draw.io файле"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Увеличиваем размер страницы
    content = re.sub(
        r'pageWidth="(\d+)" pageHeight="(\d+)"',
        lambda m: f'pageWidth="{max(1200, int(m.group(1)))}" pageHeight="{max(900, int(m.group(2)))}"',
        content
    )
    
    # Увеличиваем dx и dy для большего пространства
    content = re.sub(
        r'dx="(\d+)" dy="(\d+)"',
        lambda m: f'dx="{max(1200, int(m.group(1)))}" dy="{max(1000, int(m.group(2)))}"',
        content
    )
    
    # Увеличиваем высоту текстовых блоков (height)
    def increase_height(match):
        height = int(match.group(1))
        if height < 30:
            return f'height="{max(30, height + 10)}"'
        return match.group(0)
    
    content = re.sub(r'height="(\d+)"', increase_height, content)
    
    # Увеличиваем расстояния между элементами по Y (y координаты)
    # Для входов (I) - увеличиваем y на 150
    def shift_y_coords(match):
        y = int(match.group(1))
        # Если y < 400, это входы/управление - сдвигаем вверх
        if y < 400:
            return f'y="{y + 150}"'
        # Если y > 500, это механизмы - сдвигаем вниз
        elif y > 500:
            return f'y="{y + 150}"'
        # Центральная функция - сдвигаем вниз
        else:
            return f'y="{y + 150}"'
    
    # Применяем сдвиг к y координатам в geometry
    def shift_geometry(match):
        full_match = match.group(0)
        y_match = re.search(r'y="(\d+)"', full_match)
        if y_match:
            y = int(y_match.group(1))
            if y < 400:
                new_y = y + 150
            elif y > 500:
                new_y = y + 150
            else:
                new_y = y + 150
            return re.sub(r'y="\d+"', f'y="{new_y}"', full_match)
        return full_match
    
    content = re.sub(r'<mxGeometry[^>]*y="\d+"[^>]*>', shift_geometry, content)
    
    # Также сдвигаем mxPoint координаты
    def shift_mxpoint(match):
        full_match = match.group(0)
        y_match = re.search(r'y="(\d+)"', full_match)
        if y_match:
            y = int(y_match.group(1))
            new_y = y + 150
            return re.sub(r'y="\d+"', f'y="{new_y}"', full_match)
        return full_match
    
    content = re.sub(r'<mxPoint[^>]*y="\d+"[^>]*>', shift_mxpoint, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {filepath}")

def main():
    """Обрабатывает все .drawio файлы в diagrams-codes"""
    diagrams_dir = Path('diagrams-codes')
    
    for drawio_file in diagrams_dir.glob('*.drawio'):
        if drawio_file.name.startswith('UML_'):
            continue  # Пропускаем UML файлы, они будут созданы отдельно
        try:
            fix_drawio_file(drawio_file)
        except Exception as e:
            print(f"Error processing {drawio_file}: {e}")

if __name__ == '__main__':
    main()

