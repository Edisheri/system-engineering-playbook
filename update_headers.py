#!/usr/bin/env python3
import os
import re

def update_headers(directory):
    """Update headers in markdown files according to ISO/IEC/IEEE 29148-2011 standard"""
    
    # Mapping of old headers to new headers
    header_mappings = {
        # Architecture files
        r'^# IDEF0': '# 3.1.2. IDEF0',
        r'^# IDEF3': '# 3.1.3. IDEF3', 
        r'^# DFD': '# 3.1.4. DFD',
        r'^# BPMN': '# 3.1.5. BPMN',
        r'^# Компонентная схема': '# 3.1.7. Компонентная схема',
        
        # ADR files
        r'^# ADR-001': '# 4.1. ADR-001',
        r'^# ADR-002': '# 4.2. ADR-002', 
        r'^# ADR-003': '# 4.3. ADR-003',
        
        # API files
        r'^# API Documentation': '# 5.1. API Documentation',
        
        # Infrastructure files
        r'^# Инфраструктура': '# 6.1. Инфраструктура',
        r'^# Customer Journey Map': '# 6.2. Customer Journey Map',
        
        # Appendix files
        r'^# Примеры: DrawIO': '# 7.1. Примеры: DrawIO',
        r'^# Примеры: Markdown': '# 7.2. Примеры: Markdown',
        r'^# Swagger Example': '# 7.3. Swagger Example',
    }
    
    # Walk through all markdown files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Apply header mappings
                    new_content = content
                    for old_pattern, new_header in header_mappings.items():
                        new_content = re.sub(old_pattern, new_header, new_content, flags=re.MULTILINE)
                    
                    # Only write if content changed
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"  Updated: {file_path}")
                    else:
                        print(f"  No changes: {file_path}")
                        
                except Exception as e:
                    print(f"  Error processing {file_path}: {e}")

if __name__ == "__main__":
    update_headers("src")
