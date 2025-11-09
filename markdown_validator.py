#!/usr/bin/env python3
"""
Markdown Validation Agent
A comprehensive tool for validating markdown files with special support for Chinese text.

Features:
- Scans markdown files recursively
- Detects formatting issues (bold, italic, mixed markers)
- Handles Chinese typography-specific issues
- Validates markdown syntax compliance
- Generates detailed reports in multiple formats
- Auto-fix capabilities for common issues
"""

import os
import re
import json
import html
import argparse
import sys
import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import traceback


@dataclass
class ValidationIssue:
    """Represents a validation issue found in markdown."""
    issue_type: str
    severity: str  # 'critical', 'warning', 'suggestion'
    file_path: str
    line_number: int
    column_number: int
    line_content: str
    description: str
    suggestion: str
    context: str = ""


@dataclass
class ValidationReport:
    """Comprehensive validation report."""
    total_files: int
    total_issues: int
    issues_by_type: Dict[str, int]
    issues_by_severity: Dict[str, int]
    issues: List[ValidationIssue]
    summary: str


class MarkdownValidator:
    """Main validator class for markdown files."""
    
    def __init__(self):
        self.issues = []
        self.file_count = 0
        self.chinese_punctuation_pairs = {
            '「': '」', '『': '』', '【': '】', '（': '）', '《': '》'
        }
        self.issues_by_type = Counter()
        self.issues_by_severity = Counter()
        
    def validate_directory(self, directory: str, exclude_dirs: List[str] = None) -> ValidationReport:
        """Validate all markdown files in a directory recursively."""
        exclude_dirs = exclude_dirs or ['.git', '__pycache__', 'node_modules', 'site', '.pytest_cache']
        
        print(f"🔍 Scanning directory: {directory}")
        
        for root, dirs, files in os.walk(directory):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    self.validate_file(file_path)
        
        return self.generate_report()
    
    def validate_file(self, file_path: str) -> List[ValidationIssue]:
        """Validate a single markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            print(f"📄 Validating: {file_path}")
            self.file_count += 1
            
            # Split into lines for line number tracking
            lines = content.split('\n')
            
            # Run all validation checks
            self._check_bold_italic_issues(file_path, lines)
            self._check_mixed_markers(file_path, lines)
            self._check_chinese_punctuation(file_path, lines)
            self._check_html_contexts(file_path, lines)
            self._check_quote_issues(file_path, lines)
            self._check_whitespace_issues(file_path, lines)
            self._check_link_issues(file_path, lines)
            self._check_header_issues(file_path, lines)
            self._check_code_blocks(file_path, lines)
            
        except Exception as e:
            error_issue = ValidationIssue(
                issue_type="file_read_error",
                severity="critical",
                file_path=file_path,
                line_number=0,
                column_number=0,
                line_content="",
                description=f"Could not read file: {str(e)}",
                suggestion="Check file permissions and encoding"
            )
            self.issues.append(error_issue)
            self.issues_by_type["file_read_error"] += 1
            self.issues_by_severity["critical"] += 1
            
        return [issue for issue in self.issues if issue.file_path == file_path]
    
    def _check_bold_italic_issues(self, file_path: str, lines: List[str]):
        """Check for unresolved bold and italic markers."""
        for line_num, line in enumerate(lines, 1):
            # Check for unmatched bold markers
            bold_count = line.count('**')
            if bold_count % 2 != 0:
                self._add_issue(
                    issue_type="unmatched_bold",
                    severity="critical",
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line,
                    description=f"Unmatched bold marker (**), count: {bold_count}",
                    suggestion="Ensure all bold markers are properly paired"
                )
            
            # Check for unmatched italic markers
            italic_count = line.count('*')
            # Subtract the bold markers (each ** contains two *)
            pure_italic_count = italic_count - (bold_count * 2)
            if pure_italic_count % 2 != 0:
                self._add_issue(
                    issue_type="unmatched_italic",
                    severity="critical",
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line,
                    description=f"Unmatched italic marker (*), pure italic count: {pure_italic_count}",
                    suggestion="Ensure all italic markers are properly paired"
                )
            
            # Check for potential incorrect nesting
            if '**' in line and '*' in line:
                # Look for patterns like **text* or *text**
                if re.search(r'\*\*[^*]*\*[^*]*$', line) or re.search(r'\*[^*]*\*\*[^*]*$', line):
                    self._add_issue(
                        issue_type="incorrect_nesting",
                        severity="warning",
                        file_path=file_path,
                        line_number=line_num,
                        line_content=line,
                        description="Potential incorrect nesting of bold and italic markers",
                        suggestion="Check bold/italic nesting order"
                    )
    
    def _check_mixed_markers(self, file_path: str, lines: List[str]):
        """Check for mixed or incorrectly paired markers."""
        for line_num, line in enumerate(lines, 1):
            # Check for mixed bold markers (using both ** and __)
            if '**' in line and '__' in line:
                self._add_issue(
                    issue_type="mixed_bold_markers",
                    severity="warning",
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line,
                    description="Mixed bold marker styles (** and __) in same line",
                    suggestion="Use consistent bold marker style (** recommended)"
                )
            
            # Check for mixed italic markers (using both * and _)
            italic_star_count = line.count('*') - 2 * line.count('**')
            italic_underscore_count = line.count('_') - 2 * line.count('__')
            
            if italic_star_count > 0 and italic_underscore_count > 0:
                self._add_issue(
                    issue_type="mixed_italic_markers",
                    severity="warning",
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line,
                    description="Mixed italic marker styles (* and _) in same line",
                    suggestion="Use consistent italic marker style (* recommended)"
                )
    
    def _check_chinese_punctuation(self, file_path: str, lines: List[str]):
        """Check for Chinese punctuation and markdown interactions."""
        for line_num, line in enumerate(lines, 1):
            # Check for Chinese quotes without proper spacing
            if re.search(r'[a-zA-Z0-9][「『【（《]', line) or re.search(r'[」』】）》》][a-zA-Z0-9]', line):
                self._add_issue(
                    issue_type="chinese_punctuation_spacing",
                    severity="suggestion",
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line,
                    description="Chinese punctuation adjacent to Latin characters without spacing",
                    suggestion="Add proper spacing between Chinese punctuation and Latin characters"
                )
            
            # Check for unmatched Chinese punctuation pairs
            for open_punct, close_punct in self.chinese_punctuation_pairs.items():
                open_count = line.count(open_punct)
                close_count = line.count(close_punct)
                if open_count != close_count:
                    self._add_issue(
                        issue_type="unmatched_chinese_punctuation",
                        severity="warning",
                        file_path=file_path,
                        line_number=line_num,
                        line_content=line,
                        description=f"Unmatched Chinese punctuation: {open_punct} ({open_count}) vs {close_punct} ({close_count})",
                        suggestion=f"Ensure proper pairing of {open_punct} and {close_punct}"
                    )
    
    def _check_html_contexts(self, file_path: str, lines: List[str]):
        """Check for markdown inside HTML blocks."""
        in_html_block = False
        html_block_lines = []
        
        for line_num, line in enumerate(lines, 1):
            # Check for HTML block start/end
            if re.match(r'^\s*<[a-zA-Z][^>]*>', line) and not re.search(r'/>\s*$', line):
                in_html_block = True
                html_block_lines = []
            elif re.match(r'^\s*</[a-zA-Z][^>]*>', line) and in_html_block:
                in_html_block = False
                # Check the collected HTML block for markdown
                html_content = '\n'.join(html_block_lines)
                if re.search(r'[*_`#\[\]]', html_content):
                    self._add_issue(
                        issue_type="markdown_in_html",
                        severity="warning",
                        file_path=file_path,
                        line_number=line_num - len(html_block_lines),
                        line_content=html_block_lines[0] if html_block_lines else line,
                        description="Markdown syntax detected inside HTML block",
                        suggestion="Avoid mixing markdown syntax inside HTML blocks"
                    )
            elif in_html_block:
                html_block_lines.append(line)
            
            # Check for inline HTML with markdown
            if re.search(r'<[^>]+>.*[*_`#\[].*<[^>]+>', line):
                self._add_issue(
                    issue_type="markdown_in_inline_html",
                    severity="suggestion",
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line,
                    description="Markdown syntax mixed with inline HTML",
                    suggestion="Consider using pure HTML or pure markdown for consistency"
                )
    
    def _check_quote_issues(self, file_path: str, lines: List[str]):
        """Check for problematic quote patterns."""
        for line_num, line in enumerate(lines, 1):
            # Check for smart quotes in markdown (can cause issues)
            if ('"' in line or '"' in line or "'" in line) and re.search(r'[*_`#\[', line):
                self._add_issue(
                    issue_type="smart_quotes_with_markdown",
                    severity="suggestion",
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line,
                    description="Smart quotes mixed with markdown syntax",
                    suggestion="Use straight quotes (\") for markdown compatibility"
                )
            
            # Check for inconsistent quote usage
            straight_quotes = line.count('"')
            smart_quotes = line.count('"') + line.count('"')
            if straight_quotes > 0 and smart_quotes > 0:
                self._add_issue(
                    issue_type="mixed_quote_types",
                    severity="warning",
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line,
                    description="Mixed straight and smart quotes",
                    suggestion="Use consistent quote type throughout document"
                )
    
    def _check_whitespace_issues(self, file_path: str, lines: List[str]):
        """Check for whitespace and formatting issues."""
        for line_num, line in enumerate(lines, 1):
            # Check for trailing whitespace
            if line.rstrip() != line:
                self._add_issue(
                    issue_type="trailing_whitespace",
                    severity="suggestion",
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line,
                    description="Trailing whitespace detected",
                    suggestion="Remove trailing whitespace for cleaner formatting"
                )
            
            # Check for multiple consecutive blank lines
            if line_num > 1 and not line.strip() and not lines[line_num-2].strip():
                self._add_issue(
                    issue_type="multiple_blank_lines",
                    severity="suggestion",
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line,
                    description="Multiple consecutive blank lines",
                    suggestion="Use single blank lines between paragraphs"
                )
            
            # Check for tabs vs spaces inconsistency
            if '\t' in line:
                self._add_issue(
                    issue_type="tabs_instead_of_spaces",
                    severity="suggestion",
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line,
                    description="Tab character detected",
                    suggestion="Use spaces for indentation (markdown standard)"
                )
    
    def _check_link_issues(self, file_path: str, lines: List[str]):
        """Check for link and reference issues."""
        for line_num, line in enumerate(lines, 1):
            # Check for broken link syntax
            broken_links = re.findall(r'\[([^\]]+)\]\(([^)]*)', line)
            for text, url in broken_links:
                if not url or url.isspace():
                    self._add_issue(
                        issue_type="empty_link_url",
                        severity="critical",
                        file_path=file_path,
                        line_number=line_num,
                        line_content=line,
                        description=f"Empty URL in link: [{text}]()",
                        suggestion="Provide a valid URL for the link"
                    )
            
            # Check for unmatched brackets in links
            open_brackets = line.count('[')
            close_brackets = line.count(']')
            open_parens = line.count('(')
            close_parens = line.count(')')
            
            if open_brackets != close_brackets:
                self._add_issue(
                    issue_type="unmatched_link_brackets",
                    severity="critical",
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line,
                    description=f"Unmatched link brackets: [={open_brackets}, ]={close_brackets}",
                    suggestion="Ensure proper bracket pairing in links"
                )
            
            if open_parens != close_parens:
                self._add_issue(
                    issue_type="unmatched_link_parens",
                    severity="critical",
                    file_path=file_path,
                    line_number=line_num,
                    line_content=line,
                    description=f"Unmatched link parentheses: (={open_parens}, )={close_parens}",
                    suggestion="Ensure proper parentheses pairing in links"
                )
    
    def _check_header_issues(self, file_path: str, lines: List[str]):
        """Check for header formatting issues."""
        for line_num, line in enumerate(lines, 1):
            # Check for header spacing
            if re.match(r'^#+\s', line):
                # Check if header has proper spacing before and after
                if line_num > 1 and lines[line_num-2].strip():
                    self._add_issue(
                        issue_type="header_spacing_before",
                        severity="suggestion",
                        file_path=file_path,
                        line_number=line_num,
                        line_content=line,
                        description="Header should have blank line before it",
                        suggestion="Add blank line before headers for proper spacing"
                    )
                
                if line_num < len(lines) and lines[line_num].strip():
                    self._add_issue(
                        issue_type="header_spacing_after",
                        severity="suggestion",
                        file_path=file_path,
                        line_number=line_num,
                        line_content=line,
                        description="Header should have blank line after it",
                        suggestion="Add blank line after headers for proper spacing"
                    )
            
            # Check for header level consistency
            if re.match(r'^#+\s', line):
                header_level = len(re.match(r'^(#+)\s', line).group(1))
                if header_level > 6:
                    self._add_issue(
                        issue_type="invalid_header_level",
                        severity="warning",
                        file_path=file_path,
                        line_number=line_num,
                        line_content=line,
                        description=f"Invalid header level: {header_level} (max 6)",
                        suggestion="Use header levels 1-6 only"
                    )
    
    def _check_code_blocks(self, file_path: str, lines: List[str]):
        """Check for code block issues."""
        in_code_block = False
        code_block_start = 0
        
        for line_num, line in enumerate(lines, 1):
            # Check for code block markers
            if re.match(r'^```', line):
                if not in_code_block:
                    in_code_block = True
                    code_block_start = line_num
                    # Check for language specification
                    if line.strip() == '```':
                        self._add_issue(
                            issue_type="code_block_no_language",
                            severity="suggestion",
                            file_path=file_path,
                            line_number=line_num,
                            line_content=line,
                            description="Code block missing language specification",
                            suggestion="Add language hint after ``` (e.g., ```python)"
                        )
                else:
                    in_code_block = False
                    # Check for empty code blocks
                    if line_num - code_block_start <= 2:
                        self._add_issue(
                            issue_type="empty_code_block",
                            severity="suggestion",
                            file_path=file_path,
                            line_number=code_block_start,
                            line_content=lines[code_block_start-1],
                            description="Empty or very short code block",
                            suggestion="Remove empty code blocks or add content"
                        )
            
            # Check for inline code issues
            if re.search(r'`[^`]*`', line):
                # Check for nested backticks
                if re.search(r'`[^`]*`[^`]*`', line) and not re.search(r'``', line):
                    self._add_issue(
                        issue_type="nested_inline_code",
                        severity="warning",
                        file_path=file_path,
                        line_number=line_num,
                        line_content=line,
                        description="Potential nested inline code markers",
                        suggestion="Use proper escaping or double backticks for nested code"
                    )
    
    def _add_issue(self, issue_type: str, severity: str, file_path: str, 
                   line_number: int, line_content: str, description: str, 
                   suggestion: str):
        """Add a validation issue to the collection."""
        # Find column number if possible
        column_number = 0
        if issue_type in ["unmatched_bold", "unmatched_italic"]:
            # Find the first problematic marker
            bold_pos = line_content.find('**')
            italic_pos = line_content.find('*')
            if bold_pos != -1 and issue_type == "unmatched_bold":
                column_number = bold_pos + 1
            elif italic_pos != -1 and issue_type == "unmatched_italic":
                column_number = italic_pos + 1
        
        # Get context (surrounding lines)
        context = ""
        if line_number > 1:
            context += f"L{line_number-1}: {line_content[:50]}...\n"
        context += f"L{line_number}: {line_content[:50]}..."
        
        issue = ValidationIssue(
            issue_type=issue_type,
            severity=severity,
            file_path=file_path,
            line_number=line_number,
            column_number=column_number,
            line_content=line_content[:100],  # Truncate long lines
            description=description,
            suggestion=suggestion,
            context=context
        )
        
        self.issues.append(issue)
        self.issues_by_type[issue_type] += 1
        self.issues_by_severity[severity] += 1
    
    def generate_report(self) -> ValidationReport:
        """Generate a comprehensive validation report."""
        summary = self._generate_summary()
        
        return ValidationReport(
            total_files=self.file_count,
            total_issues=len(self.issues),
            issues_by_type=dict(self.issues_by_type),
            issues_by_severity=dict(self.issues_by_severity),
            issues=self.issues,
            summary=summary
        )
    
    def _generate_summary(self) -> str:
        """Generate a summary of the validation results."""
        if not self.issues:
            return f"✅ All {self.file_count} markdown files are valid!"
        
        critical_count = self.issues_by_severity.get('critical', 0)
        warning_count = self.issues_by_severity.get('warning', 0)
        suggestion_count = self.issues_by_severity.get('suggestion', 0)
        
        summary = f"📊 Validation Summary:\n"
        summary += f"   Files scanned: {self.file_count}\n"
        summary += f"   Total issues: {len(self.issues)}\n"
        summary += f"   🔴 Critical: {critical_count}\n"
        summary += f"   🟡 Warning: {warning_count}\n"
        summary += f"   🔵 Suggestion: {suggestion_count}\n"
        
        return summary
    
    def auto_fix_issues(self, file_path: str, dry_run: bool = True) -> List[str]:
        """Auto-fix common issues in a file."""
        fixes_applied = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix trailing whitespace
            content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)
            if content != original_content:
                fixes_applied.append("Removed trailing whitespace")
            
            # Fix multiple blank lines
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            if content != original_content and "Removed trailing whitespace" not in fixes_applied:
                fixes_applied.append("Consolidated multiple blank lines")
            
            # Fix tabs to spaces (4 spaces per tab)
            content = content.replace('\t', '    ')
            if content != original_content and "Removed trailing whitespace" not in fixes_applied and "Consolidated multiple blank lines" not in fixes_applied:
                fixes_applied.append("Converted tabs to spaces")
            
            if not dry_run and fixes_applied:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Applied fixes to {file_path}: {', '.join(fixes_applied)}")
            elif dry_run and fixes_applied:
                print(f"🔧 Would apply fixes to {file_path}: {', '.join(fixes_applied)}")
            
        except Exception as e:
            print(f"❌ Error auto-fixing {file_path}: {str(e)}")
        
        return fixes_applied


class ReportGenerator:
    """Generate reports in various formats."""
    
    @staticmethod
    def generate_console_report(report: ValidationReport):
        """Generate a console-friendly report."""
        print("\n" + "="*60)
        print("📋 MARKDOWN VALIDATION REPORT")
        print("="*60)
        print(report.summary)
        print("\n" + "-"*60)
        
        if report.issues:
            print("🔍 ISSUES BY TYPE:")
            for issue_type, count in report.issues_by_type.items():
                print(f"   {issue_type}: {count}")
            
            print("\n🔍 ISSUES BY SEVERITY:")
            for severity, count in report.issues_by_severity.items():
                print(f"   {severity}: {count}")
            
            print("\n🔍 DETAILED ISSUES:")
            for issue in report.issues[:20]:  # Show first 20 issues
                severity_icon = {"critical": "🔴", "warning": "🟡", "suggestion": "🔵"}.get(issue.severity, "⚪")
                print(f"\n{severity_icon} {issue.issue_type} ({issue.severity})")
                print(f"   File: {issue.file_path}:{issue.line_number}")
                print(f"   Description: {issue.description}")
                print(f"   Suggestion: {issue.suggestion}")
                if issue.line_content:
                    print(f"   Content: {issue.line_content}")
            
            if len(report.issues) > 20:
                print(f"\n... and {len(report.issues) - 20} more issues")
    
    @staticmethod
    def generate_html_report(report: ValidationReport, output_file: str):
        """Generate an HTML report."""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Validation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 2px solid #007acc; padding-bottom: 10px; }}
        .summary {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .issue {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
        .critical {{ border-left: 4px solid #dc3545; background: #fff5f5; }}
        .warning {{ border-left: 4px solid #ffc107; background: #fffbf0; }}
        .suggestion {{ border-left: 4px solid #17a2b8; background: #f0fcff; }}
        .issue-type {{ font-weight: bold; color: #333; }}
        .file-path {{ font-family: monospace; background: #f8f9fa; padding: 2px 4px; border-radius: 3px; }}
        .line-content {{ font-family: monospace; background: #f8f9fa; padding: 10px; border-radius: 3px; margin: 5px 0; white-space: pre-wrap; }}
        .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-card {{ flex: 1; background: white; border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center; }}
        .stat-number {{ font-size: 24px; font-weight: bold; }}
        .critical-stat {{ color: #dc3545; }}
        .warning-stat {{ color: #ffc107; }}
        .suggestion-stat {{ color: #17a2b8; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📋 Markdown Validation Report</h1>
        
        <div class="summary">
            <h2>Summary</h2>
            <p><strong>Files scanned:</strong> {report.total_files}</p>
            <p><strong>Total issues:</strong> {report.total_issues}</p>
            <p><strong>Report generated:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number critical-stat">{report.issues_by_severity.get('critical', 0)}</div>
                <div>Critical Issues</div>
            </div>
            <div class="stat-card">
                <div class="stat-number warning-stat">{report.issues_by_severity.get('warning', 0)}</div>
                <div>Warnings</div>
            </div>
            <div class="stat-card">
                <div class="stat-number suggestion-stat">{report.issues_by_severity.get('suggestion', 0)}</div>
                <div>Suggestions</div>
            </div>
        </div>
        
        <h2>Issues by Type</h2>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr style="background: #f8f9fa;">
                <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Issue Type</th>
                <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Count</th>
            </tr>
        """
        
        for issue_type, count in report.issues_by_type.items():
            html_content += f"""
            <tr>
                <td style="padding: 10px; border: 1px solid #ddd;">{issue_type}</td>
                <td style="padding: 10px; border: 1px solid #ddd;">{count}</td>
            </tr>
            """
        
        html_content += """
        </table>
        
        <h2>Detailed Issues</h2>
        """
        
        for issue in report.issues:
            html_content += f"""
            <div class="issue {issue.severity}">
                <div class="issue-type">{issue.issue_type.upper()} ({issue.severity})</div>
                <p><strong>File:</strong> <span class="file-path">{issue.file_path}:{issue.line_number}</span></p>
                <p><strong>Description:</strong> {issue.description}</p>
                <p><strong>Suggestion:</strong> {issue.suggestion}</p>
                {f'<div class="line-content">{html.escape(issue.line_content)}</div>' if issue.line_content else ''}
            </div>
            """
        
        html_content += """
    </div>
</body>
</html>
        """
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 HTML report generated: {output_file}")
    
    @staticmethod
    def generate_json_report(report: ValidationReport, output_file: str):
        """Generate a JSON report."""
        json_data = {
            "metadata": {
                "total_files": report.total_files,
                "total_issues": report.total_issues,
                "generated_at": datetime.datetime.now().isoformat()
            },
            "summary": {
                "issues_by_type": report.issues_by_type,
                "issues_by_severity": report.issues_by_severity
            },
            "issues": [asdict(issue) for issue in report.issues]
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 JSON report generated: {output_file}")


def main():
    """Main entry point for the markdown validation agent."""
    parser = argparse.ArgumentParser(
        description="Markdown Validation Agent - Comprehensive markdown file validator with Chinese text support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/markdown/files                    # Basic validation
  %(prog)s /path/to/files --html report.html          # Generate HTML report
  %(prog)s /path/to/files --json report.json          # Generate JSON report
  %(prog)s /path/to/files --auto-fix                  # Auto-fix common issues
  %(prog)s /path/to/files --severity critical          # Show only critical issues
  %(prog)s /path/to/files --exclude-dir site,build    # Exclude directories
        """
    )
    
    parser.add_argument('directory', help='Directory containing markdown files to validate')
    parser.add_argument('--html', help='Generate HTML report (output file path)')
    parser.add_argument('--json', help='Generate JSON report (output file path)')
    parser.add_argument('--auto-fix', action='store_true', help='Auto-fix common issues')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed without making changes')
    parser.add_argument('--severity', choices=['critical', 'warning', 'suggestion'], 
                       help='Filter issues by severity level')
    parser.add_argument('--exclude-dir', help='Comma-separated list of directories to exclude')
    parser.add_argument('--output-format', choices=['console', 'html', 'json', 'all'], 
                       default='console', help='Output format (default: console)')
    
    args = parser.parse_args()
    
    # Check if directory exists
    if not os.path.isdir(args.directory):
        print(f"❌ Error: Directory '{args.directory}' does not exist")
        sys.exit(1)
    
    # Parse exclude directories
    exclude_dirs = []
    if args.exclude_dir:
        exclude_dirs = [d.strip() for d in args.exclude_dir.split(',')]
    
    # Initialize validator
    validator = MarkdownValidator()
    
    try:
        # Run validation
        print("🚀 Starting markdown validation...")
        report = validator.validate_directory(args.directory, exclude_dirs)
        
        # Filter issues by severity if specified
        if args.severity:
            report.issues = [issue for issue in report.issues if issue.severity == args.severity]
            report.total_issues = len(report.issues)
            # Recalculate counts
            report.issues_by_type = Counter(issue.issue_type for issue in report.issues)
            report.issues_by_severity = Counter(issue.severity for issue in report.issues)
        
        # Auto-fix if requested
        if args.auto_fix:
            print("\n🔧 Auto-fixing common issues...")
            for issue in report.issues:
                if issue.issue_type in ["trailing_whitespace", "multiple_blank_lines", "tabs_instead_of_spaces"]:
                    validator.auto_fix_issues(issue.file_path, dry_run=args.dry_run)
        
        # Generate reports
        if args.output_format in ['console', 'all']:
            ReportGenerator.generate_console_report(report)
        
        if args.html or args.output_format in ['html', 'all']:
            html_file = args.html or 'markdown_validation_report.html'
            ReportGenerator.generate_html_report(report, html_file)
        
        if args.json or args.output_format in ['json', 'all']:
            json_file = args.json or 'markdown_validation_report.json'
            ReportGenerator.generate_json_report(report, json_file)
        
        # Exit with appropriate code
        if report.issues_by_severity.get('critical', 0) > 0:
            print("\n❌ Validation completed with critical issues")
            sys.exit(1)
        elif report.total_issues > 0:
            print("\n⚠️ Validation completed with non-critical issues")
            sys.exit(0)
        else:
            print("\n✅ Validation completed successfully")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()