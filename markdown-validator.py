#!/usr/bin/env python3
"""
Markdown Validation Agent
专门用于发现和处理中文内容中的markdown格式问题
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import html

@dataclass
class MarkdownIssue:
    """Markdown格式问题数据类"""
    issue_type: str
    severity: str  # 'critical', 'warning', 'suggestion'
    file_path: str
    line_number: int
    line_content: str
    description: str
    suggestion: str
    context: str = ""

class MarkdownValidator:
    """Markdown验证器主类"""
    
    def __init__(self):
        self.issues = []
        self.stats = defaultdict(int)
        
        # 常见的markdown格式问题模式
        self.patterns = {
            'unresolved_bold': {
                'pattern': r'\*\*([^*]+)\*\*',
                'description': '未解析的粗体标记',
                'severity': 'critical'
            },
            'unresolved_italic': {
                'pattern': r'\*([^*]+)\*',
                'description': '未解析的斜体标记',
                'severity': 'warning'
            },
            'mixed_markers': {
                'pattern': r'\*\*([^*]+)\*|\*([^*]+)\*\*',
                'description': '混合的粗体/斜体标记',
                'severity': 'critical'
            },
            'chinese_quote_issues': {
                'pattern': r'\*\*["\'][^"\']*["\'][^*]*\*\*|\*\*["\'][^"\']*["\']\*\*',
                'description': '中文引号与粗体标记组合问题',
                'severity': 'critical'
            },
            'html_context_issues': {
                'pattern': r'<[^>]*>\*\*[^*]+\*\*<[^>]*>|<[^>]*>\*[^*]+\*<[^>]*>',
                'description': 'HTML上下文中的markdown问题',
                'severity': 'warning'
            },
            'escaped_markers': {
                'pattern': r'\\\*\*|\\\*',
                'description': '转义的markdown标记',
                'severity': 'suggestion'
            },
            'nested_markers': {
                'pattern': r'\*\*[^*]*\*[^*]*\*\*|\*[^*]*\*\*[^*]*\*',
                'description': '嵌套的markdown标记',
                'severity': 'warning'
            }
        }
        
        # 中文标点符号模式
        self.chinese_punctuation = r'[\u3002\uff0c\uff1b\uff1a\u201c\u201d\u2018\u2019\u2014\u3010\u3011\u300a\u300b\u3008\u3009\u300c\u300d\u300e\u300f\u2010\u2013\u2014\uff08\uff09\u3014\u3015\uff3b\uff3d\u3016\u3017\u3018\u3019\u301a\u301b\u301c\u301d\u301e\u301f\uff5b\uff5d\uff5e\uff09\u2026\u2014\u00b7\u2022\u2023\u25cf\u25cb\u25ce\u25a0\u25a1\u25b2\u25b3\u25bc\u25bd\u25c6\u25c7\u25aa\u25ab\u25ac\u25ad\u25ae\u25af\u25b0\u25b1\u25b6\u25b7\u25b8\u25b9\u25ba\u25bb\u25bc\u25bd\u25be\u25bf\u25c0\u25c1\u25c2\u25c3\u25c4\u25c5\u25c6\u25c7\u25c8\u25c9\u25ca\u25cb\u25cc\u25cd\u25ce\u25cf\u25d0\u25d1\u25d2\u25d3\u25d4\u25d5\u25d6\u25d7\u25d8\u25d9\u25da\u25db\u25dc\u25dd\u25de\u25df\u25e0\u25e1\u25e2\u25e3\u25e4\u25e5\u25e6\u25e7\u25e8\u25e9\u25ea\u25eb\u25ec\u25ed\u25ee\u25ef\u25f0\u25f1\u25f2\u25f3\u25f4\u25f5\u25f6\u25f7\u25f8\u25f9\u25fa\u25fb\u25fc\u25fd\u25fe\u25ff]'
        
    def validate_file(self, file_path: Path) -> List[MarkdownIssue]:
        """验证单个markdown文件"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                issues.extend(self._validate_line(line, line_num, file_path))
                
        except Exception as e:
            issues.append(MarkdownIssue(
                issue_type='file_read_error',
                severity='critical',
                file_path=str(file_path),
                line_number=0,
                line_content='',
                description=f'无法读取文件: {e}',
                suggestion='检查文件编码和权限'
            ))
            
        return issues
    
    def _validate_line(self, line: str, line_num: int, file_path: Path) -> List[MarkdownIssue]:
        """验证单行内容"""
        issues = []
        
        # 检查各种markdown格式问题
        for issue_type, config in self.patterns.items():
            matches = re.finditer(config['pattern'], line)
            for match in matches:
                # 排除一些误报
                if self._is_false_positive(match.group(), issue_type, line):
                    continue
                    
                issue = MarkdownIssue(
                    issue_type=issue_type,
                    severity=config['severity'],
                    file_path=str(file_path),
                    line_number=line_num,
                    line_content=line.strip(),
                    description=config['description'],
                    suggestion=self._get_suggestion(match.group(), issue_type),
                    context=self._get_context(line, match)
                )
                issues.append(issue)
                self.stats[issue_type] += 1
        
        # 特殊检查：中文环境下的引号问题
        issues.extend(self._check_chinese_quotes(line, line_num, file_path))
        
        return issues
    
    def _is_false_positive(self, text: str, issue_type: str, line: str) -> bool:
        """判断是否为误报"""
        # 排除代码块中的内容
        if '```' in line or line.strip().startswith('```'):
            return True
            
        # 排除HTML注释
        if '<!--' in line or '-->' in line:
            return True
            
        # 排除行内代码
        if '`' in text and text.count('`') >= 2:
            return True
            
        # 排除Mermaid图表
        if 'mermaid' in line.lower():
            return True
            
        # 对于粗体标记，检查是否在HTML标签内
        if issue_type in ['unresolved_bold', 'unresolved_italic']:
            if re.search(r'<[^>]*>[^<]*\*\*[^<]*</[^>]*>', line):
                return True
                
        # 检查是否为合法的markdown格式（正确的配对）
        if issue_type == 'unresolved_bold':
            # 计算粗体标记的数量
            bold_count = text.count('**')
            if bold_count % 2 == 0 and bold_count >= 2:
                # 可能是合法的粗体，需要进一步检查上下文
                return self._is_legitimate_bold(text, line)
                
        if issue_type == 'unresolved_italic':
            # 计算斜体标记的数量
            italic_count = text.count('*')
            if italic_count % 2 == 0 and italic_count >= 2:
                # 可能是合法的斜体
                return True
                
        return False
    
    def _is_legitimate_bold(self, text: str, line: str) -> bool:
        """检查是否为合法的粗体标记"""
        # 检查是否在标题中
        if line.strip().startswith('#'):
            return True
            
        # 检查是否有正确的内容结构
        bold_pattern = r'\*\*([^*]+)\*\*'
        matches = re.findall(bold_pattern, text)
        
        if matches:
            # 检查内容是否不为空
            for match in matches:
                if match.strip():
                    return True
                    
        return False
    
    def _get_suggestion(self, text: str, issue_type: str) -> str:
        """获取修复建议"""
        suggestions = {
            'unresolved_bold': '检查markdown渲染器配置，确保粗体标记正确解析',
            'unresolved_italic': '检查斜体标记是否被正确渲染',
            'mixed_markers': '统一使用**粗体**或*斜体*标记，避免混用',
            'chinese_quote_issues': '确保引号在粗体标记内正确闭合',
            'html_context_issues': '避免在HTML标签内使用markdown标记',
            'escaped_markers': '如果不需要转义，移除反斜杠',
            'nested_markers': '避免嵌套使用markdown标记'
        }
        
        base_suggestion = suggestions.get(issue_type, '检查markdown语法')
        
        # 根据具体问题提供更详细的建议
        if issue_type == 'unresolved_bold':
            if '"' in text or "'" in text:
                base_suggestion += '。特别注意引号与粗体标记的组合'
                
        return base_suggestion
    
    def _get_context(self, line: str, match) -> str:
        """获取问题上下文"""
        start = max(0, match.start() - 20)
        end = min(len(line), match.end() + 20)
        context = line[start:end]
        return context.strip()
    
    def _check_chinese_quotes(self, line: str, line_num: int, file_path: Path) -> List[MarkdownIssue]:
        """检查中文引号相关的问题"""
        issues = []
        
        # 检查中文引号与粗体标记的组合问题
        pattern = r'\*\*["\'][^"\']*["\'][^*]*\*\*'
        matches = re.finditer(pattern, line)
        
        for match in matches:
            # 检查引号是否平衡
            quote_count = match.group().count('"') + match.group().count('"')
            if quote_count % 2 != 0:
                issues.append(MarkdownIssue(
                    issue_type='unbalanced_quotes',
                    severity='critical',
                    file_path=str(file_path),
                    line_number=line_num,
                    line_content=line.strip(),
                    description='中文引号不平衡',
                    suggestion='确保所有引号都正确闭合',
                    context=self._get_context(line, match)
                ))
        
        return issues
    
    def scan_directory(self, directory: Path, recursive: bool = True) -> List[MarkdownIssue]:
        """扫描目录中的所有markdown文件"""
        issues = []
        
        if recursive:
            pattern = "**/*.md"
        else:
            pattern = "*.md"
            
        markdown_files = list(directory.glob(pattern))
        
        print(f"发现 {len(markdown_files)} 个markdown文件")
        
        for file_path in markdown_files:
            print(f"正在验证: {file_path}")
            file_issues = self.validate_file(file_path)
            issues.extend(file_issues)
            
        return issues
    
    def generate_report(self, issues: List[MarkdownIssue], output_format: str = 'text') -> str:
        """生成验证报告"""
        if output_format == 'json':
            return self._generate_json_report(issues)
        elif output_format == 'html':
            return self._generate_html_report(issues)
        else:
            return self._generate_text_report(issues)
    
    def _generate_text_report(self, issues: List[MarkdownIssue]) -> str:
        """生成文本格式报告"""
        report = []
        report.append("=" * 60)
        report.append("Markdown格式验证报告")
        report.append("=" * 60)
        report.append("")
        
        # 统计信息
        report.append("📊 统计信息:")
        report.append(f"  总问题数: {len(issues)}")
        for issue_type, count in self.stats.items():
            severity = next((p['severity'] for p in self.patterns.values() if p.get('description', '').split()[0] == issue_type.split('_')[0]), 'unknown')
            emoji = {'critical': '🔴', 'warning': '🟡', 'suggestion': '🔵'}.get(severity, '⚪')
            report.append(f"  {emoji} {issue_type}: {count}")
        report.append("")
        
        # 按严重程度分组
        by_severity = defaultdict(list)
        for issue in issues:
            by_severity[issue.severity].append(issue)
        
        # 输出关键问题
        if by_severity['critical']:
            report.append("🔴 关键问题:")
            for issue in by_severity['critical']:
                report.append(f"  文件: {issue.file_path}:{issue.line_number}")
                report.append(f"  问题: {issue.description}")
                report.append(f"  内容: {issue.line_content}")
                report.append(f"  建议: {issue.suggestion}")
                report.append("")
        
        # 输出警告
        if by_severity['warning']:
            report.append("🟡 警告:")
            for issue in by_severity['warning']:
                report.append(f"  文件: {issue.file_path}:{issue.line_number}")
                report.append(f"  问题: {issue.description}")
                report.append(f"  内容: {issue.line_content}")
                report.append("")
        
        # 输出建议
        if by_severity['suggestion']:
            report.append("🔵 建议:")
            for issue in by_severity['suggestion']:
                report.append(f"  文件: {issue.file_path}:{issue.line_number}")
                report.append(f"  问题: {issue.description}")
                report.append("")
        
        return "\n".join(report)
    
    def _generate_json_report(self, issues: List[MarkdownIssue]) -> str:
        """生成JSON格式报告"""
        report_data = {
            'summary': {
                'total_issues': len(issues),
                'statistics': dict(self.stats)
            },
            'issues': []
        }
        
        for issue in issues:
            report_data['issues'].append({
                'type': issue.issue_type,
                'severity': issue.severity,
                'file_path': issue.file_path,
                'line_number': issue.line_number,
                'line_content': issue.line_content,
                'description': issue.description,
                'suggestion': issue.suggestion,
                'context': issue.context
            })
        
        return json.dumps(report_data, ensure_ascii=False, indent=2)
    
    def _generate_html_report(self, issues: List[MarkdownIssue]) -> str:
        """生成HTML格式报告"""
        html_content = []
        html_content.append("""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown格式验证报告</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        .stats { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .issue { margin: 15px 0; padding: 15px; border-radius: 5px; border-left: 4px solid; }
        .critical { background: #fff5f5; border-color: #dc3545; }
        .warning { background: #fff3cd; border-color: #ffc107; }
        .suggestion { background: #e7f3ff; border-color: #007bff; }
        .issue-header { font-weight: bold; margin-bottom: 5px; }
        .issue-content { background: #f8f9fa; padding: 10px; border-radius: 3px; font-family: monospace; margin: 5px 0; }
        .issue-suggestion { color: #666; font-style: italic; margin-top: 5px; }
        .file-path { color: #007bff; text-decoration: none; }
        .file-path:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 Markdown格式验证报告</h1>
""")
        
        # 统计信息
        html_content.append('<div class="stats">')
        html_content.append('<h2>📊 统计信息</h2>')
        html_content.append(f'<p><strong>总问题数:</strong> {len(issues)}</p>')
        html_content.append('<ul>')
        for issue_type, count in self.stats.items():
            severity = next((p['severity'] for p in self.patterns.values() if issue_type in p['description']), 'unknown')
            color = {'critical': '#dc3545', 'warning': '#ffc107', 'suggestion': '#007bff'}.get(severity, '#6c757d')
            html_content.append(f'<li style="color: {color}">{issue_type}: {count}</li>')
        html_content.append('</ul>')
        html_content.append('</div>')
        
        # 问题详情
        html_content.append('<h2>🔍 问题详情</h2>')
        
        for issue in issues:
            html_content.append(f'<div class="issue {issue.severity}">')
            html_content.append(f'<div class="issue-header">{issue.description}</div>')
            html_content.append(f'<div><strong>文件:</strong> <a href="{issue.file_path}" class="file-path">{issue.file_path}:{issue.line_number}</a></div>')
            html_content.append(f'<div class="issue-content">{html.escape(issue.line_content)}</div>')
            html_content.append(f'<div class="issue-suggestion"><strong>建议:</strong> {issue.suggestion}</div>')
            html_content.append('</div>')
        
        html_content.append("""
    </div>
</body>
</html>
""")
        
        return "\n".join(html_content)
    
    def auto_fix(self, issues: List[MarkdownIssue], dry_run: bool = True) -> List[str]:
        """自动修复简单的问题"""
        fixes = []
        
        # 按文件分组
        by_file = defaultdict(list)
        for issue in issues:
            by_file[issue.file_path].append(issue)
        
        for file_path, file_issues in by_file.items():
            if not os.path.exists(file_path):
                continue
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            fixed_lines = lines.copy()
            changes_made = False
            
            for issue in file_issues:
                if issue.issue_type == 'escaped_markers' and not dry_run:
                    # 移除不必要的转义
                    line_num = issue.line_number - 1
                    if 0 <= line_num < len(fixed_lines):
                        fixed_lines[line_num] = fixed_lines[line_num].replace(r'\*\*', '**').replace(r'\*', '*')
                        changes_made = True
            
            if changes_made and not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(fixed_lines))
                fixes.append(f"修复了文件: {file_path}")
            elif changes_made and dry_run:
                fixes.append(f"可以修复文件: {file_path}")
        
        return fixes

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Markdown格式验证器')
    parser.add_argument('path', help='要验证的文件或目录路径')
    parser.add_argument('--format', choices=['text', 'json', 'html'], default='text', 
                       help='输出格式 (默认: text)')
    parser.add_argument('--recursive', '-r', action='store_true', 
                       help='递归扫描子目录')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--fix', action='store_true', 
                       help='自动修复可修复的问题')
    parser.add_argument('--dry-run', action='store_true', 
                       help='显示将要修复的内容但不实际执行')
    
    args = parser.parse_args()
    
    # 初始化验证器
    validator = MarkdownValidator()
    
    # 确定路径
    path = Path(args.path)
    
    # 执行验证
    if path.is_file():
        print(f"验证文件: {path}")
        issues = validator.validate_file(path)
    else:
        print(f"扫描目录: {path}")
        issues = validator.scan_directory(path, args.recursive)
    
    # 生成报告
    report = validator.generate_report(issues, args.format)
    
    # 输出结果
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存到: {args.output}")
    else:
        print(report)
    
    # 自动修复
    if args.fix or args.dry_run:
        fixes = validator.auto_fix(issues, dry_run=args.dry_run)
        if fixes:
            print("\n🔧 修复结果:")
            for fix in fixes:
                print(f"  {fix}")
        else:
            print("\n🔧 没有可以自动修复的问题")
    
    # 退出码
    critical_issues = [issue for issue in issues if issue.severity == 'critical']
    if critical_issues:
        print(f"\n❌ 发现 {len(critical_issues)} 个关键问题")
        exit(1)
    else:
        print(f"\n✅ 没有关键问题")
        exit(0)

if __name__ == "__main__":
    main()