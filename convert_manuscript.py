#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert the medibeauconsultant.md manuscript to MkDocs structure
"""

import re
import os
from pathlib import Path

def extract_chapter_structure(file_path):
    """Extract chapter structure from the manuscript"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all chapter headings
    chapter_pattern = r'## 第(\d+)章[：:](.*?)(?=\n## 第\d+章[：:]|$)'
    chapters = re.findall(chapter_pattern, content, re.DOTALL)
    
    # Find part headings
    part_pattern = r'# 第(一|二|三|四)部分[：:](.*?)(?=\n# 第[一二三四]部分[：:]|$)'
    parts = re.findall(part_pattern, content, re.DOTALL)
    
    return parts, chapters

def convert_manuscript_to_chapters(input_file, output_dir):
    """Convert the manuscript to individual chapter files"""
    
    # Read the full manuscript
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the preface
    preface_match = re.search(r'^# .+?\n(.*?)(?=\n# 第[一二三四]部分[：:])', content, re.DOTALL)
    if preface_match:
        preface = preface_match.group(1).strip()
        # Write preface to index.md
        index_path = Path(output_dir) / 'docs' / 'index.md'
        index_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("# 美的觉醒：积极心理学视角下的现代女性与专业咨询师成长指南\n\n")
            f.write("## 序言\n\n")
            f.write(preface)
    
    # Extract and write each part
    part_pattern = r'# 第(一|二|三|四)部分[：:](.*?)(?=\n# 第[一二三四]部分[：:]|$)'
    parts = re.findall(part_pattern, content, re.DOTALL)
    
    part_mapping = {'一': 'part1', '二': 'part2', '三': 'part3', '四': 'part4'}
    
    for part_num, part_content in parts:
        part_dir = part_mapping[part_num]
        part_path = Path(output_dir) / 'docs' / part_dir
        
        # Extract chapters from this part
        chapter_pattern = r'## 第(\d+)章[：:](.*?)(?=\n## 第\d+章[：:]|$)'
        chapters = re.findall(chapter_pattern, part_content, re.DOTALL)
        
        for chapter_num, chapter_content in chapters:
            chapter_file = part_path / f'chapter{chapter_num}.md'
            chapter_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Clean up chapter content
            chapter_content = re.sub(r'^\s+', '', chapter_content, flags=re.MULTILINE)
            
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(f"## 第{chapter_num}章\n\n")
                f.write(chapter_content.strip())
    
    print(f"Successfully converted manuscript to MkDocs structure in {output_dir}")

if __name__ == "__main__":
    input_file = "/root/claude/psychology/medibeauconsultant.md"
    output_dir = "/root/claude/psychology"
    
    convert_manuscript_to_chapters(input_file, output_dir)