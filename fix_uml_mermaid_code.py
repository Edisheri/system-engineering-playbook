#!/usr/bin/env python3
import os
import re

def fix_uml_mermaid_code(directory):
    """Replace Mermaid code blocks with image references in UML files"""
    
    # Pattern to match Mermaid code blocks
    pattern = r'```mermaid\n.*?```'
    
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
                        
                        # Check if file contains Mermaid code
                        if '```mermaid' in content:
                            # Extract the base name for the image
                            base_name = file.replace('.md', '')
                            
                            # Replace Mermaid code with image reference
                            new_content = re.sub(pattern, f'![Component Diagram](../img/diagrams/{base_name}-6.png)', content, flags=re.DOTALL)
                            
                            # Only write if content changed
                            if new_content != content:
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(new_content)
                                print(f"  Updated: {file_path}")
                            else:
                                print(f"  No changes: {file_path}")
                        else:
                            print(f"  No Mermaid code found: {file_path}")
                            
                    except Exception as e:
                        print(f"  Error processing {file_path}: {e}")

if __name__ == "__main__":
    fix_uml_mermaid_code("src")
