# Markdown Validator Usage Examples

## Basic Usage

### 1. Basic Validation
```bash
python markdown_validator.py /path/to/markdown/files
```

### 2. Generate HTML Report
```bash
python markdown_validator.py /path/to/files --html report.html
```

### 3. Generate JSON Report
```bash
python markdown_validator.py /path/to/files --json report.json
```

### 4. Auto-fix Common Issues
```bash
python markdown_validator.py /path/to/files --auto-fix
```

### 5. Dry Run (Show What Would Be Fixed)
```bash
python markdown_validator.py /path/to/files --auto-fix --dry-run
```

### 6. Filter by Severity
```bash
python markdown_validator.py /path/to/files --severity critical
```

### 7. Exclude Directories
```bash
python markdown_validator.py /path/to/files --exclude-dir site,build,node_modules
```

### 8. Generate All Report Formats
```bash
python markdown_validator.py /path/to/files --output-format all
```

## Advanced Usage

### Validate Specific File Types
The validator automatically finds all `.md` files in the specified directory and subdirectories.

### Continuous Integration
```bash
# Exit with error code if critical issues found
python markdown_validator.py ./docs || exit 1
```

### Automated Reporting
```bash
# Generate comprehensive reports for documentation
python markdown_validator.py ./docs --html docs-validation.html --json docs-validation.json
```

## Example Output

### Console Output
```
🔍 Scanning directory: /path/to/markdown/files
📄 Validating: /path/to/markdown/files/file1.md
📄 Validating: /path/to/markdown/docs/chapter1.md
📄 Validating: /path/to/markdown/docs/chapter2.md

============================================================
📋 MARKDOWN VALIDATION REPORT
============================================================
📊 Validation Summary:
   Files scanned: 3
   Total issues: 5
   🔴 Critical: 2
   🟡 Warning: 2
   🔵 Suggestion: 1

------------------------------------------------------------
🔍 ISSUES BY TYPE:
   unmatched_bold: 2
   mixed_bold_markers: 1
   trailing_whitespace: 1
   chinese_punctuation_spacing: 1

🔍 ISSUES BY SEVERITY:
   critical: 2
   warning: 2
   suggestion: 1

🔍 DETAILED ISSUES:

🔴 unmatched_bold (critical)
   File: /path/to/markdown/file1.md:15
   Description: Unmatched bold marker (**), count: 1
   Suggestion: Ensure all bold markers are properly paired
   Content: This is **bold text without closing

🔴 unmatched_italic (critical)
   File: /path/to/markdown/file1.md:23
   Description: Unmatched italic marker (*), pure italic count: 1
   Suggestion: Ensure all italic markers are properly paired
   Content: This is *italic text without closing
```

### HTML Report
The HTML report includes:
- Summary statistics with visual cards
- Detailed issue breakdown by type and severity
- Color-coded issues (red for critical, yellow for warning, blue for suggestion)
- Interactive and responsive design
- Syntax-highlighted code examples

### JSON Report
The JSON report provides structured data for:
- Integration with CI/CD pipelines
- Programmatic analysis
- Custom reporting tools
- Historical tracking of issues

## Features Demonstrated

### Chinese Text Support
- Detects Chinese punctuation spacing issues
- Validates Chinese quote pairs (「」, 『』, 【】, etc.)
- Handles mixed Chinese/Latin text properly

### Advanced Markdown Validation
- Bold/italic marker validation
- Link syntax checking
- Header formatting validation
- Code block analysis
- HTML context detection

### Auto-Fix Capabilities
- Trailing whitespace removal
- Multiple blank line consolidation
- Tab-to-space conversion
- Consistent formatting

### Comprehensive Reporting
- Multiple output formats
- Severity-based filtering
- Detailed issue tracking
- Actionable suggestions

## Integration with MkDocs

The validator works seamlessly with MkDocs projects:

```bash
# Validate MkDocs documentation
python markdown_validator.py ./docs --exclude-dir site

# Generate validation report for documentation review
python markdown_validator.py ./docs --html mkdocs-validation.html

# Use in CI/CD pipeline
python markdown_validator.py ./docs --severity critical --json validation.json
```