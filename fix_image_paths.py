#!/usr/bin/env python3
import os
import re

def fix_image_paths(directory):
    """Fix image paths in markdown files to use relative paths from subdirectories"""
    
    # Pattern to match image references
    pattern = r'!\[([^\]]*)\]\(img/diagrams/([^)]+)\)'
    replacement = r'![\1](../img/diagrams/\2)'
    
    # Walk through all markdown files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"Processing: {file_path}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace image paths
                    new_content = re.sub(pattern, replacement, content)
                    
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
    fix_image_paths("src")
