#!/bin/bash

# Good Questions - 打包脚本

echo "📦 开始打包 Good Questions 技能包..."

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$SCRIPT_DIR/.."

# 输出文件名
OUTPUT_NAME="good-questions-$(date +%Y%m%d).zip"
OUTPUT_PATH="$SCRIPT_DIR/$OUTPUT_NAME"

# 打包
cd "$PLUGIN_DIR" && zip -r "$OUTPUT_PATH" \
    .claude-plugin/ \
    README.md \
    agents/ \
    skills/ \
    packages/ \
    -x "*.git*" -x "*__pycache__*" -x "*node_modules*"

echo ""
echo "✅ 打包成功！"
echo "   文件：$OUTPUT_PATH"
echo ""
echo "分发方式："
echo "  1. 发送 $OUTPUT_NAME 给对方"
echo "  2. 对方运行：unzip good-questions.zip -d ~/.claude-plugin/"
echo ""
