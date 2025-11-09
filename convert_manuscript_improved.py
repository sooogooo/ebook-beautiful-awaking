#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Improved script to convert the medibeauconsultant.md manuscript to MkDocs structure
"""

import re
import os
from pathlib import Path

def parse_manuscript_structure(file_path):
    """Parse the manuscript structure more accurately"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content by parts
    part_pattern = r'(?=# 第[一二三四]部分[：:])'
    parts = re.split(part_pattern, content)
    
    # Remove empty strings and clean up
    parts = [p.strip() for p in parts if p.strip()]
    
    # Structure to hold all content
    structure = {
        'preface': '',
        'parts': {}
    }
    
    for part in parts:
        if part.startswith('# 第'):
            # Extract part title
            part_match = re.match(r'# 第([一二三四])部分[：:](.*?)(?=\n)', part, re.DOTALL)
            if part_match:
                part_num = part_match.group(1)
                part_title = part_match.group(2).strip()
                
                # Remove the part header from the content
                part_content = re.sub(r'# 第[一二三四]部分[：:].*?\n', '', part, 1)
                
                # Extract chapters from this part
                chapters = []
                chapter_pattern = r'(?=## 第\d+章[：:])'
                chapter_sections = re.split(chapter_pattern, part_content)
                
                for chapter_section in chapter_sections:
                    chapter_section = chapter_section.strip()
                    if chapter_section.startswith('## 第'):
                        chapter_match = re.match(r'## 第(\d+)章[：:](.*?)(?=\n)', chapter_section, re.DOTALL)
                        if chapter_match:
                            chapter_num = chapter_match.group(1)
                            chapter_title = chapter_match.group(2).strip()
                            
                            # Remove the chapter header from the content
                            chapter_content = re.sub(r'## 第\d+章[：:].*?\n', '', chapter_section, 1)
                            
                            chapters.append({
                                'number': chapter_num,
                                'title': chapter_title,
                                'content': chapter_content.strip()
                            })
                
                structure['parts'][part_num] = {
                    'title': part_title,
                    'chapters': chapters
                }
        else:
            # This is the preface
            structure['preface'] = part
    
    return structure

def convert_to_mkdocs(input_file, output_dir):
    """Convert manuscript to MkDocs structure"""
    
    # Parse the manuscript
    structure = parse_manuscript_structure(input_file)
    
    # Create docs directory structure
    docs_dir = Path(output_dir) / 'docs'
    docs_dir.mkdir(exist_ok=True)
    
    # Write index.md with preface
    index_path = docs_dir / 'index.md'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("# 美的觉醒\n\n")
        f.write("**积极心理学视角下的现代女性与专业咨询师成长指南**\n\n")
        f.write("---\n\n")
        f.write("## 序言\n\n")
        f.write(structure['preface'])
    
    # Part mapping
    part_mapping = {'一': 'part1', '二': 'part2', '三': 'part3', '四': 'part4'}
    
    # Process each part
    for part_num, part_data in structure['parts'].items():
        part_dir = docs_dir / part_mapping[part_num]
        part_dir.mkdir(exist_ok=True)
        
        # Write each chapter
        for chapter in part_data['chapters']:
            chapter_file = part_dir / f'chapter{chapter["number"]}.md'
            
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(f"## 第{chapter['number']}章\n\n")
                f.write(f"### {chapter['title']}\n\n")
                f.write(chapter['content'])
    
    print(f"Successfully converted manuscript to MkDocs structure")
    print(f"Created {len(structure['parts'])} parts with {sum(len(p['chapters']) for p in structure['parts'].values())} chapters")

if __name__ == "__main__":
    input_file = "/root/claude/psychology/medibeauconsultant.md"
    output_dir = "/root/claude/psychology"
    
    convert_to_mkdocs(input_file, output_dir)