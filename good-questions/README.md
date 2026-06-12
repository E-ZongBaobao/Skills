# HV Analysis - 提问艺术技能包

> 真正厉害的人，不是解决问题，而是重新定义问题。

## 概述

这是一个**完整的 7 步思考工作流**技能，帮你系统性地深入分析问题。

## 核心技能

### hv-analysis

**一键启动完整流程：**
```
/hv-analysis
/hv-analysis 如何做出好的内容来实现时间自由
```

**7 步流程：**
```
步骤 1：元认知校准 → 确认问题确实是问题
步骤 2：视角切换   → 从默认视角跳到新坐标
步骤 3：连续追问   → 从现象深入到系统结构
步骤 4：问题重构   → 重新定义问题本身
步骤 5：反事实思维 → 先怀疑现实，再重构现实
步骤 6：系统思维   → 把问题放进系统中理解
步骤 7：假设驱动   → 提出假设，用 MVP 验证
```

---

## 交互模式

开始前，先问用户选择：

| 模式 | 特点 | 适合 |
|------|------|------|
| **A. 深度引导** | 我主动推荐，你只需选择 | 想被带着思考、需要灵感 |
| **B. 问答模式** | 我只提问，你自己探索 | 喜欢独立思考 |
| **C. 均衡模式** | 我问问题 + 提供选项 | 推荐（默认） |

---

## 安装

### 方式 1：一键安装
```bash
bash packages/install.sh
```

### 方式 2：手动安装
```bash
cp -r hv-analysis ~/.claude-plugin/
```

### 方式 3：打包分发
```bash
bash packages/package.sh
# 发送 good-questions-YYYYMMDD.zip 给对方
```

---

## 使用

```
/hv-analysis 你的问题
/hv-analysis 如何做出好的内容来实现时间自由 [A/B/C]
```

---

## 文件结构

```
hv-analysis/
├── SKILL.md              # 主技能定义
├── references/           # 引用资料
│   ├── 7-steps.md
│   ├── perspectives.md
│   ├── why-layers.md
│   ├── what-if-questions.md
│   ├── reframing-techniques.md
│   ├── systems-framework.md
│   ├── mvp-methods.md
│   └── checklist.md
└── scripts/              # 脚本（预留）
```
