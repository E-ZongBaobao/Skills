#!/bin/bash

# Good Questions - 卸载脚本

echo "🗑️  开始卸载 Good Questions 技能包..."

TARGET_DIR="$HOME/.claude-plugin/good-questions"

if [ ! -d "$TARGET_DIR" ]; then
    echo "❌ 未检测到已安装的版本"
    exit 1
fi

read -p "确定卸载？(y/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$TARGET_DIR"
    echo "✅ 卸载成功！"
else
    echo "❌ 卸载取消"
fi
