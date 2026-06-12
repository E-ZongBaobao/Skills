#!/bin/bash

# Good Questions - 一键安装脚本

echo "🚀 开始安装 Good Questions 技能包..."

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$SCRIPT_DIR/.."

# 目标目录
TARGET_DIR="$HOME/.claude-plugin"

# 创建目标目录
mkdir -p "$TARGET_DIR"

# 检查是否已安装
if [ -d "$TARGET_DIR/good-questions" ]; then
    echo "⚠️  已检测到已安装的版本"
    read -p "是否覆盖？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 安装取消"
        exit 1
    fi
    # 删除旧版本
    rm -rf "$TARGET_DIR/good-questions"
fi

# 复制插件
cp -r "$PLUGIN_DIR" "$TARGET_DIR/good-questions"

echo "✅ 安装成功！"
echo ""
echo "使用方法："
echo "  /ask-better-questions 你的问题"
echo ""
echo "重启 Claude Code 后即可使用"
