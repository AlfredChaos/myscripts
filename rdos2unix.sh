#!/bin/bash

# 遍历所有文件并执行dos2unix格式化
# 定义要遍历的目标文件夹
TARGET_DIR="/my/target/directory"

# 使用find命令遍历目标文件夹中的所有文件
for file in `find $TARGET_DIR -type f`
do
    if file --mime "$file" | grep -iq ': text'; then
        # 通过dos2unix对文本文件进行格式化
        dos2unix "$file"
        echo "Formatted file: $file"
    else
        echo "Skipped non-text file: $file"
    fi
done