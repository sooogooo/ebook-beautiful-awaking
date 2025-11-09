# 《美的觉醒》SVG视觉规范系统

## 🎨 设计理念

### 核心原则
- **极简主义**：用最少的视觉元素传达最清晰的信息
- **功能性优先**：形式服务于内容，不为了装饰而装饰
- **可读性至上**：确保所有文字在任何设备上都清晰可读
- **一致性原则**：所有配图遵循统一的视觉语言

### 设计哲学
- **东方美学**：借鉴传统水墨画的留白和意境
- **现代简约**：符合当代扁平化设计趋势
- **学术严谨**：保持专业著作的严谨性和权威性
- **人文关怀**：通过视觉设计传递温暖和包容

## 🎯 视觉要素规范

### 颜色系统

**主色调（黑白灰系列）**：
```css
/* 主要颜色 */
--color-primary: #333333;      /* 主色 - 深灰，主要文字和重要线条 */
--color-secondary: #666666;    /* 次色 - 中灰，次要文字和线条 */
--color-tertiary: #999999;     /* 辅色 - 浅灰，装饰性元素 */
--color-background: #ffffff;    /* 背景 - 纯白（透明背景时移除） */
--color-highlight: #f5f5f5;     /* 高亮 - 极浅灰，必要时使用 */

/* 功能性颜色（极少量使用） */
--color-accent: #808080;       /* 强调色 - 中性灰，用于重点强调 */
--color-success: #666666;      /* 成功色 - 使用灰色调表示积极 */
--color-warning: #666666;      /* 警告色 - 使用灰色调表示注意 */
--color-error: #666666;        /* 错误色 - 使用灰色调表示问题 */
```

**使用原则**：
- 避免使用任何彩色元素
- 通过灰度变化创造视觉层次
- 重要的信息和线条使用深色
- 次要信息使用浅色

### 线条规范

**线条粗细标准**：
```css
/* 线条粗细 */
--stroke-width-primary: 1.5px;   /* 主要线条 - 框架、重要连接线 */
--stroke-width-secondary: 1px;   /* 次要线条 - 一般连接线、边框 */
--stroke-width-tertiary: 0.5px;  /* 装饰线条 - 分隔线、装饰元素 */
--stroke-width-accent: 2px;      /* 强调线条 - 核心概念框架 */
```

**线条样式**：
- **实线**：solid，用于主要连接和框架
- **虚线**：dashed，用于次要连接和流程指示
- **点线**：dotted，用于装饰和边界
- **无连接**：none，用于独立的视觉元素

**线条圆角**：
- 标准圆角：stroke-linecap: round
- 连接点：stroke-linejoin: round
- 营造柔和、亲和的视觉效果

### 字体规范

**字体族设置**：
```css
/* 优先字体栈 */
font-family: "Helvetica Neue", "PingFang SC", "Microsoft YaHei", 
             "Hiragino Sans GB", "Arial", sans-serif;
```

**字体大小标准**：
```css
/* 字体大小 */
--font-size-title: 14px;         /* 主标题 - 章节标题 */
--font-size-subtitle: 12px;       /* 副标题 - 模块标题 */
--font-size-body: 10px;          /* 正文 - 主要内容 */
--font-size-caption: 8px;        /* 说明文字 - 注释、标签 */
--font-size-minimum: 6px;        /* 最小字体 - 极小注释 */
```

**字体粗细**：
```css
/* 字体粗细 */
--font-weight-light: 300;        /* 细体 - 主要使用 */
--font-weight-normal: 400;       /* 正常 - 强调时使用 */
--font-weight-medium: 500;       /* 中等 - 极少使用 */
```

**文字颜色**：
- 主要文字：#333333
- 次要文字：#666666
- 说明文字：#999999
- 禁用文字：#cccccc

### 间距与布局

**标准间距系统**：
```css
/* 间距系统 */
--spacing-xs: 4px;              /* 极小间距 */
--spacing-sm: 8px;              /* 小间距 */
--spacing-md: 12px;             /* 中等间距 */
--spacing-lg: 16px;             /* 大间距 */
--spacing-xl: 20px;             /* 超大间距 */
--spacing-xxl: 24px;            /* 最大间距 */
```

**网格系统**：
- 基于4px的基础网格
- 所有元素对齐到网格线
- 保持视觉秩序和一致性

**留白原则**：
- 最小页边距：20px
- 内容区域最小宽度：200px
- 元素周围最小留白：8px
- 重要信息周围增加留白

## 📐 组件规范

### 节点样式

**标准节点**：
```svg
<!-- 基础节点 -->
<rect x="0" y="0" width="120" height="40" 
      rx="4" ry="4"
      fill="none" 
      stroke="#333333" 
      stroke-width="1"/>
<text x="60" y="25" 
      text-anchor="middle" 
      font-family="Helvetica Neue, Arial, sans-serif" 
      font-size="10px" 
      font-weight="300" 
      fill="#333333">节点文本</text>
```

**重要节点**：
```svg
<!-- 强调节点 -->
<rect x="0" y="0" width="120" height="40" 
      rx="4" ry="4"
      fill="none" 
      stroke="#333333" 
      stroke-width="1.5"/>
<text x="60" y="25" 
      text-anchor="middle" 
      font-family="Helvetica Neue, Arial, sans-serif" 
      font-size="10px" 
      font-weight="400" 
      fill="#333333">重要节点</text>
```

### 连接线样式

**标准连接线**：
```svg
<!-- 基础连接线 -->
<path d="M 0 0 L 100 0" 
      stroke="#666666" 
      stroke-width="1" 
      fill="none"/>
```

**强调连接线**：
```svg
<!-- 重要连接线 -->
<path d="M 0 0 L 100 0" 
      stroke="#333333" 
      stroke-width="1.5" 
      fill="none"/>
```

**虚线连接**：
```svg
<!-- 虚线连接 -->
<path d="M 0 0 L 100 0" 
      stroke="#999999" 
      stroke-width="1" 
      stroke-dasharray="4,2" 
      fill="none"/>
```

### 箭头样式

**标准箭头**：
```svg
<!-- 基础箭头 -->
<path d="M 0 0 L 6 3 L 0 6" 
      stroke="#666666" 
      stroke-width="1" 
      fill="none"/>
```

**填充箭头**：
```svg
<!-- 填充箭头 -->
<path d="M 0 0 L 6 3 L 0 6 L 2 3 Z" 
      fill="#666666"/>
```

## 🎭 图表类型规范

### 流程图规范

**布局方向**：
- 主要流向：从左到右，从上到下
- 分支数量：不超过3个主要分支
- 层级深度：不超过5层

**节点规范**：
- 起始节点：圆角矩形，深色边框
- 过程节点：标准矩形，中等边框
- 决策节点：菱形，中等边框
- 结束节点：圆角矩形，深色边框

### 关系图规范

**布局方式**：
- 中心辐射式：核心概念在中心
- 网络式：多节点互联
- 层级式：上下级关系明确

**连接规范**：
- 主要关系：粗实线
- 次要关系：细实线
- 弱关系：虚线
- 影响关系：箭头指示方向

### 对比图规范

**并排布局**：
- 左右对比：垂直中轴对齐
- 上下对比：水平中轴对齐
- 矩阵对比：网格对齐

**视觉区分**：
- 通过线条粗细区分重要性
- 通过颜色深浅区分层次
- 通过位置关系区分类别

## ✨ 交互规范

### 基础交互

**点击放大**：
```css
.interactive-element {
  cursor: pointer;
  transition: transform 0.3s ease;
}

.interactive-element:hover {
  transform: scale(1.02);
}

.interactive-element:active {
  transform: scale(1.5);
}
```

**悬停效果**：
```css
.interactive-element {
  opacity: 0.8;
  transition: opacity 0.2s ease;
}

.interactive-element:hover {
  opacity: 1;
}
```

### 响应式设计

**移动端适配**：
```css
@media (max-width: 768px) {
  .svg-container {
    font-size: 12px;
    stroke-width: 1.5px;
  }
}

@media (max-width: 480px) {
  .svg-container {
    font-size: 14px;
    stroke-width: 2px;
  }
}
```

**高分辨率屏幕**：
```css
@media (-webkit-min-device-pixel-ratio: 2) {
  .svg-container {
    stroke-width: 0.5px;
  }
}
```

## 📏 质量标准

### 文件规范

**文件大小**：
- 简单图标：< 5KB
- 标准图表：< 20KB
- 复杂图表：< 50KB

**命名规范**：
- 格式：`模块-功能-编号.svg`
- 示例：`psychology-self-mirror-01.svg`
- 版本控制：`v1.0`, `v1.1`, `v2.0`

**代码规范**：
```xml
<!-- SVG代码结构 -->
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- 定义可重用元素 -->
  <defs>
    <!-- 样式定义 -->
  </defs>
  
  <!-- 背景层（可选） -->
  
  <!-- 内容层 -->
  
  <!-- 装饰层 -->
</svg>
```

### 性能要求

**加载时间**：
- 首次渲染：< 1秒
- 交互响应：< 100ms
- 动画流畅度：60fps

**兼容性**：
- 现代浏览器：Chrome 60+, Firefox 55+, Safari 12+
- 移动端：iOS 12+, Android 8+
- 降级支持：IE 11+

### 可访问性

**屏幕阅读器支持**：
```svg
<title>图表标题</title>
<desc>图表详细描述</desc>
```

**键盘导航**：
- 支持Tab键导航
- 提供焦点指示器
- 支持键盘操作

## 🔧 实施工具

### 设计工具
- **矢量设计**：Adobe Illustrator, Figma
- **代码编辑**：VS Code, Sublime Text
- **优化工具**：SVGO, SVGOMG

### 验证工具
- **语法检查**：W3C SVG Validator
- **性能测试**：Chrome DevTools
- **兼容性测试**：BrowserStack

### 版本管理
- **代码托管**：Git
- **文件管理**：语义化版本控制
- **备份策略**：云端+本地备份

## 📚 使用指南

### 快速开始

1. **复制模板**：使用标准SVG模板开始设计
2. **应用样式**：按照规范设置颜色、字体、线条
3. **测试效果**：在不同设备和浏览器上测试
4. **优化代码**：使用SVGO优化文件大小

### 常见问题

**Q: 如何确保文字在小屏幕上可读？**
A: 最小字体不小于12px，使用高对比度颜色

**Q: 如何处理复杂的层级关系？**
A: 使用不同的线条粗细和灰度来区分层级

**Q: 如何平衡美观和功能性？**
A: 始终以信息传达为第一要务，装饰性元素简化

---

**更新日期**：2025年1月
**版本**：v1.0
**维护者**：《美的觉醒》设计团队