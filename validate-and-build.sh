#!/bin/bash

# Markdown验证和构建脚本
# 用于发现markdown格式问题并构建MkDocs站点

set -e

echo "🔍 开始Markdown格式验证..."
echo "================================"

# 运行验证器
python3 markdown-validator.py docs/ --recursive --format json --output validation-report.json

# 检查是否有关键问题
if [ $? -eq 1 ]; then
    echo "❌ 发现关键问题，请先修复"
    echo ""
    echo "📊 问题摘要:"
    python3 -c "
import json
with open('validation-report.json', 'r', encoding='utf-8') as f:
    report = json.load(f)
    
stats = report['summary']['statistics']
total = report['summary']['total_issues']
critical = len([i for i in report['issues'] if i['severity'] == 'critical'])
warning = len([i for i in report['issues'] if i['severity'] == 'warning'])

print(f'  总问题数: {total}')
print(f'  关键问题: {critical}')
print(f'  警告: {warning}')
"
    
    echo ""
    echo "📋 详细报告已生成: validation-report.json"
    echo ""
    echo "💡 建议运行以下命令查看详细问题:"
    echo "   python3 markdown-validator.py docs/ --recursive --format text"
    echo ""
    echo "🔧 或者生成HTML报告:"
    echo "   python3 markdown-validator.py docs/ --recursive --format html --output validation-report.html"
    
    exit 1
else
    echo "✅ 验证通过，开始构建MkDocs站点..."
    echo ""
    
    # 构建MkDocs站点
    /root/claude/psychology/mkdocs-env/bin/python3 -m mkdocs build
    
    echo "✅ 构建完成!"
    echo ""
    echo "🌐 站点已生成到: site/"
    echo ""
    echo "🚀 启动本地服务器:"
    echo "   /root/claude/psychology/mkdocs-env/bin/python3 -m mkdocs serve"
fi