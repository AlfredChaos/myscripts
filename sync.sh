#!/bin/bash

# 检查是否传入了两个参数
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_path> <target_path>"
    exit 1
fi

# 读取参数
SOURCE_PATH=$1
TARGET_PATH=$2

# 检查源路径是否存在
if [ ! -d "$SOURCE_PATH" ]; then
    echo "Error: Source path does not exist."
    exit 1
fi

# 检查目标路径是否存在，如果不存在则创建
if [ ! -d "$TARGET_PATH" ]; then
    echo "Target path does not exist, creating it..."
    mkdir -p "$TARGET_PATH"
fi

# 进入源路径
cd "$SOURCE_PATH"

# 执行git status并获取被修改的文件列表
MODIFIED_FILES=$(git status --porcelain | grep -E '^ M' | awk '{print $2}')

# 循环遍历被修改的文件，并将它们复制到目标路径
for file in $MODIFIED_FILES; do
    # 获取文件的绝对路径
    ABSOLUTE_FILE_PATH=$(realpath "$file")

    # 构建目标文件的路径
    DEST_FILE_PATH="$TARGET_PATH/$(basename "$ABSOLUTE_FILE_PATH")"

    # 复制文件
    cp "$ABSOLUTE_FILE_PATH" "$DEST_FILE_PATH"

    # 输出复制的文件信息
    echo "Copied '$ABSOLUTE_FILE_PATH' to '$DEST_FILE_PATH'"
done

echo "Script completed."