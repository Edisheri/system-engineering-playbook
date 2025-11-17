#!/usr/bin/env python3
"""
Заменяет PNG ссылки на @drawio{} для всех UML диаграмм
"""

import re
from pathlib import Path

UML_MAPPING = {
    'uml-image-processing-1.png': 'UML_IMAGE_PROCESSING_1_UseCase.drawio',
    'uml-image-processing-2.png': 'UML_IMAGE_PROCESSING_2_Activity.drawio',
    'uml-image-processing-3.png': 'UML_IMAGE_PROCESSING_3_Sequence.drawio',
    'uml-image-processing-4.png': 'UML_IMAGE_PROCESSING_4_Class.drawio',
    'uml-image-processing-5.png': 'UML_IMAGE_PROCESSING_5_State.drawio',
    'uml-image-processing-6.png': 'UML_IMAGE_PROCESSING_6_Component.drawio',
    
    'uml-text-analysis-1.png': 'UML_TEXT_ANALYSIS_1_UseCase.drawio',
    'uml-text-analysis-2.png': 'UML_TEXT_ANALYSIS_2_Activity.drawio',
    'uml-text-analysis-3.png': 'UML_TEXT_ANALYSIS_3_Sequence.drawio',
    'uml-text-analysis-4.png': 'UML_TEXT_ANALYSIS_4_Class.drawio',
    'uml-text-analysis-5.png': 'UML_TEXT_ANALYSIS_5_State.drawio',
    'uml-text-analysis-6.png': 'UML_TEXT_ANALYSIS_6_Component.drawio',
    
    'uml-registration-1.png': 'UML_REGISTRATION_1_UseCase.drawio',
    'uml-registration-2.png': 'UML_REGISTRATION_2_Activity.drawio',
    'uml-registration-3.png': 'UML_REGISTRATION_3_Sequence.drawio',
    'uml-registration-4.png': 'UML_REGISTRATION_4_Class.drawio',
    'uml-registration-5.png': 'UML_REGISTRATION_5_State.drawio',
    'uml-registration-6.png': 'UML_REGISTRATION_6_Component.drawio',
    
    'uml-data-upload-1.png': 'UML_DATA_UPLOAD_1_UseCase.drawio',
    'uml-data-upload-2.png': 'UML_DATA_UPLOAD_2_Activity.drawio',
    'uml-data-upload-3.png': 'UML_DATA_UPLOAD_3_Sequence.drawio',
    'uml-data-upload-4.png': 'UML_DATA_UPLOAD_4_Class.drawio',
    'uml-data-upload-5.png': 'UML_DATA_UPLOAD_5_State.drawio',
    'uml-data-upload-6.png': 'UML_DATA_UPLOAD_6_Component.drawio',
}

def replace_png_in_file(filepath):
    """Заменяет PNG ссылки на @drawio{} в файле"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for png_name, drawio_name in UML_MAPPING.items():
        # Паттерн для поиска PNG ссылок
        patterns = [
            (rf'!\[.*?\]\(/img/diagrams/{re.escape(png_name)}\)', 
             f'@drawio{{https://github.com/Edisheri/system-engineering-playbook/blob/main/diagrams-codes/{drawio_name}}}'),
            (rf'!\[.*?\]\(\.\./img/diagrams/{re.escape(png_name)}\)',
             f'@drawio{{https://github.com/Edisheri/system-engineering-playbook/blob/main/diagrams-codes/{drawio_name}}}'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")
        return True
    return False

def main():
    """Обрабатывает все UML markdown файлы"""
    uml_dir = Path('src/architecture/uml')
    
    for md_file in uml_dir.glob('*.md'):
        replace_png_in_file(md_file)

if __name__ == '__main__':
    main()

