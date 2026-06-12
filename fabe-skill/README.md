# FABE 销售话术生成技能

独立技能项目，用于将产品技术语言转换为用户语言，生成多场景营销文案。

## 目录结构

```
fabe-skill/
├── SKILL.md           # 技能入口文件（必需）
├── README.md          # 项目说明（本文件）
└── references/        # 参考文档（可选）
    ├── audience-guide.md    # 受众分析详解
    ├── fabe-framework.md    # FABE 框架详解
    ├── conversion-examples.md # 转换案例库
    └── checklist.md         # 自检清单
```

## SKILL.md 的作用

这是技能的**主入口文件**，包含：
- 技能元信息（name, description, argument-hint）
- 使用方式和触发词
- 核心方法论
- 示例和输出格式

## references/ 目录的作用

存放**详细参考文档**，用于：
1. **扩展知识库**：SKILL.md 中只放核心内容，详细框架放入 references
2. **提升准确性**：调用技能时，Claude 可以读取相关参考文档
3. **便于维护**：内容模块化，易于更新和补充

## 推荐添加的参考文档

### 1. audience-guide.md（受众分析）
- 普通消费者的详细特征和话术要点
- 媒体编辑的关注点和提问方式
- 技术发烧友的圈层语言和需求
- 不同受众的案例分析

### 2. fabe-framework.md（FABE 框架详解）
- F/A/B/E 各元素的详细定义
- 元素之间的连接逻辑
- 常见错误和修正方法
- 完整案例拆解

### 3. conversion-examples.md（转换案例库）
- 技术语言 → 用户语言的对照表
- 不同产品类型的转换模式
- 优秀案例和失败案例对比

### 4. checklist.md（自检清单）
- 写完后的四个检验问题
- 各受众的专项检查点
- 快速检查流程

## 如何使用 references

在 SKILL.md 中引用：
```markdown
## 参考资源

详细内容参见 `references/` 目录：
- **`audience-guide.md`** - 不同受众的详细分析
- **`fabe-framework.md`** - FABE 框架详解
- **`conversion-examples.md`** - 转换案例库
- **`checklist.md`** - 自检清单
```

## 其他可选内容

- **templates/** - 文案模板（如不同平台的格式要求）
- **examples/** - 完整案例（输入→输出对照）
- **prompts/** - 提示词模板（如果需要更精细的控制）
