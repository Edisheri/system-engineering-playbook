#!/usr/bin/env python3
import os
import re

def fix_uml_relative_paths(directory):
    """Fix UML image paths to use relative paths from uml/ subdirectory"""
    
    # Pattern to match image references with absolute paths
    pattern = r'!\[([^\]]*)\]\(/img/diagrams/([^)]+)\)'
    replacement = r'![\1](../img/diagrams/\2)'
    
    # Walk through UML files
    for root, dirs, files in os.walk(directory):
        if 'uml' in root:
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
    fix_uml_relative_paths("src")
