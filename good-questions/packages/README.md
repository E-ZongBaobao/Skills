# Good Questions - 提问艺术技能包

这是一个**可打包、可分发、可自动/手动调用**的技能包。

---

## 快速开始

### 方式 1：一键安装

```bash
# 克隆或下载技能包
cd /Users/ninebot/Documents/Claude/good-questions

# 运行安装脚本
bash packages/install.sh
```

安装后，任何地方都能用：
```
/ask-better-questions 你的问题
```

---

### 方式 2：打包分发

```bash
# 打包成 ZIP
bash packages/package.sh

# 生成 good-questions.zip
```

发给别人后，对方运行：
```bash
unzip good-questions.zip -d ~/.claude-plugin/
```

---

### 方式 3：手动安装

```bash
cp -r good-questions ~/.claude-plugin/
```

---

## 使用方式

### 手动调用

```
/ask-better-questions 如何做出好的内容来实现时间自由
```

### 自动触发

当你问以下问题时，技能会自动触发：
- "帮我分析问题"
- "怎么想清楚这个问题"
- "如何思考"
- "帮我思考"

---

## 文件结构

```
good-questions/
├── .claude-plugin/
│   └── plugin.json          # 插件配置
├── README.md                 # 使用说明
├── packages/
│   ├── install.sh           # 一键安装脚本
│   ├── package.sh           # 打包脚本
│   └── README.md            # 本文件
├── agents/
│   ├── ask-better-questions.md
│   └── AGENT-PROMPT.md
└── skills/
    └── ask-better-questions/
        └── SKILL.md         # 主工作流技能
```

---

## 交互模式

每个技能支持三种模式：

| 模式 | 特点 | 适合 |
|------|------|------|
| **A. 深度引导** | 我主动推荐，你只需选择 | 想被带着思考 |
| **B. 问答模式** | 我只提问，你自己探索 | 喜欢独立思考 |
| **C. 均衡模式** | 我问问题 + 提供选项 | 推荐 |

---

## 7 步工作流

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

## 验证安装

安装后，运行：
```
/help
```

看到 `/ask-better-questions` 就说明安装成功。
