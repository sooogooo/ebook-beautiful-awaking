# Markdown格式验证器使用指南

## 简介

这个专门的markdown验证器用于发现和处理中文内容中的markdown格式问题，特别适合您的写作内容优化工作流。

## 快速开始

### 1. 基本验证

```bash
# 验证单个文件
python3 markdown-validator.py docs/index.md

# 验证整个目录
python3 markdown-validator.py docs/ --recursive
```

### 2. 生成报告

```bash
# 文本报告（默认）
python3 markdown-validator.py docs/ --recursive --format text

# JSON报告（适合程序处理）
python3 markdown-validator.py docs/ --recursive --format json --output report.json

# HTML报告（可视化）
python3 markdown-validator.py docs/ --recursive --format html --output report.html
```

### 3. 自动修复

```bash
# 预览修复效果
python3 markdown-validator.py docs/ --recursive --dry-run

# 执行自动修复
python3 markdown-validator.py docs/ --recursive --fix
```

### 4. 集成到构建流程

```bash
# 验证并构建（推荐）
./validate-and-build.sh
```

## 检测的问题类型

### 🔴 关键问题
- **unresolved_bold**: 未解析的粗体标记
- **mixed_markers**: 混合的粗体/斜体标记
- **chinese_quote_issues**: 中文引号与粗体标记组合问题

### 🟡 警告
- **unresolved_italic**: 未解析的斜体标记
- **html_context_issues**: HTML上下文中的markdown问题
- **nested_markers**: 嵌套的markdown标记

### 🔵 建议
- **escaped_markers**: 转义的markdown标记

## 常见问题解决方案

### 1. 未解析的粗体标记

**问题**: `**文本**` 没有正确渲染为 `<strong>` 标签

**可能原因**:
- MkDocs配置问题
- 中文标点符号干扰
- HTML上下文冲突

**解决方案**:
1. 检查 `mkdocs.yml` 中的 `markdown_extensions` 配置
2. 确保 `pymdownx.betterem` 扩展已启用
3. 验证 `pymdownx.escapeall` 扩展配置

### 2. 中文引号问题

**问题**: `**"中文引号"**` 格式导致渲染问题

**解决方案**:
- 确保引号在粗体标记内正确闭合
- 避免在引号附近断行
- 使用全角中文标点符号

### 3. 混合标记问题

**问题**: 粗体和斜体标记混用导致解析错误

**解决方案**:
- 统一使用 `**粗体**` 格式
- 避免在同一文本中混用不同标记
- 检查标记的嵌套层级

## 配置文件

编辑 `validator-config.json` 来自定义验证规则：

```json
{
  "features": {
    "validation": {
      "unresolved_bold": "检测未解析的粗体标记",
      "chinese_quote_issues": "检测中文引号问题"
    }
  }
}
```

## 工作流集成

### 1. Git Hook

在 `.git/hooks/pre-commit` 中添加：

```bash
#!/bin/bash
# 验证markdown文件
python3 markdown-validator.py docs/ --recursive --format json --output validation-report.json

if [ $? -eq 1 ]; then
    echo "❌ 发现markdown格式问题，请先修复"
    exit 1
fi
```

### 2. CI/CD 集成

在您的CI/CD配置中添加：

```yaml
steps:
  - name: 验证Markdown格式
    run: |
      python3 markdown-validator.py docs/ --recursive
      if [ $? -eq 1 ]; then
        echo "发现关键问题，构建失败"
        exit 1
      fi
```

### 3. 定期检查

使用cron任务定期检查：

```bash
# 每天早上9点检查
0 9 * * * cd /root/claude/psychology && python3 markdown-validator.py docs/ --recursive --format html --output /var/www/validation-report.html
```

## 性能优化

### 1. 增量检查

```bash
# 只检查修改过的文件
git diff --name-only HEAD~1 | grep '\.md$' | xargs python3 markdown-validator.py
```

### 2. 并行处理

```bash
# 使用GNU parallel加速大项目
find docs/ -name '*.md' | parallel python3 markdown-validator.py {}
```

### 3. 缓存结果

验证器支持结果缓存，避免重复检查未修改的文件。

## 故障排除

### 1. 误报太多

调整验证器的严格程度：

```python
# 在代码中调整
validator = MarkdownValidator()
validator.strict_mode = False  # 放松模式
```

### 2. 性能问题

对于大型项目，可以：

```bash
# 分批处理
python3 markdown-validator.py docs/part1/ --recursive
python3 markdown-validator.py docs/part2/ --recursive
# ...
```

### 3. 自定义规则

扩展验证器以支持特定规则：

```python
# 添加自定义检查模式
validator.patterns['custom_rule'] = {
    'pattern': r'your_pattern_here',
    'description': '自定义规则描述',
    'severity': 'warning'
}
```

## 技术支持

如果遇到问题，请检查：

1. Python版本要求：3.6+
2. 依赖包：标准库，无需额外安装
3. 文件编码：UTF-8
4. 权限：确保有读取文件的权限

## 贡献指南

欢迎贡献新的检查规则和改进建议：

1. Fork项目
2. 创建功能分支
3. 添加测试用例
4. 提交Pull Request

---

**提示**: 建议将此验证器集成到您的日常写作工作流中，可以及早发现并修复markdown格式问题。