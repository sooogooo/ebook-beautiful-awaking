#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final script to convert the medibeauconsultant.md manuscript to MkDocs structure
"""

import re
import os
from pathlib import Path

def convert_manuscript_final(input_file, output_dir):
    """Convert manuscript to MkDocs structure with proper parsing"""
    
    # Read the manuscript
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create docs directory
    docs_dir = Path(output_dir) / 'docs'
    docs_dir.mkdir(exist_ok=True)
    
    # Extract main title and preface
    title_match = re.search(r'^# (.+?)\n', content)
    main_title = title_match.group(1) if title_match else "美的觉醒"
    
    # Extract preface (everything before first part)
    preface_end = content.find('## **第一部分')
    if preface_end == -1:
        preface_end = content.find('## 第一部分')
    
    if preface_end != -1:
        preface_content = content[:preface_end]
        # Remove the main title from preface
        preface_content = re.sub(r'^# .+?\n', '', preface_content, 1)
        
        # Write index.md
        index_path = docs_dir / 'index.md'
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(f"# {main_title}\n\n")
            f.write(preface_content)
    
    # Find all parts and chapters
    part_pattern = r'## [**]*(第一部分|第二部分|第三部分|第四部分)[：:](.+?)(?=\n## [**]*(第一部分|第二部分|第三部分|第四部分)|$)'
    
    parts = re.findall(part_pattern, content, re.DOTALL)
    
    part_mapping = {
        '第一部分': 'part1',
        '第二部分': 'part2', 
        '第三部分': 'part3',
        '第四部分': 'part4'
    }
    
    for part_info in parts:
        part_name = part_info[0]
        part_title = part_info[1].strip('* ')
        part_content = part_info[2]
        
        # Create part directory
        part_dir = docs_dir / part_mapping[part_name]
        part_dir.mkdir(exist_ok=True)
        
        # Extract chapters from this part
        chapter_pattern = r'## [**]*(第\d+章)[：:](.+?)(?=\n## [**]*(第\d+章)|$)'
        chapters = re.findall(chapter_pattern, part_content, re.DOTALL)
        
        for chapter_info in chapters:
            chapter_name = chapter_info[0]
            chapter_title = chapter_info[1].strip('* ')
            chapter_content = chapter_info[2]
            
            # Extract chapter number
            chapter_num = re.search(r'第(\d+)章', chapter_name).group(1)
            
            # Write chapter file
            chapter_file = part_dir / f'chapter{chapter_num}.md'
            
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(f"## {chapter_name}\n\n")
                f.write(f"### {chapter_title}\n\n")
                f.write(chapter_content.strip())
    
    print(f"Successfully converted manuscript to MkDocs structure")
    print(f"Created {len(parts)} parts with {sum(len(re.findall(r'## [**]*(第\d+章)', p[2])) for p in parts)} chapters")

if __name__ == "__main__":
    input_file = "/root/claude/psychology/medibeauconsultant.md"
    output_dir = "/root/claude/psychology"
    
    convert_manuscript_final(input_file, output_dir)