#!/bin/bash

# 检查 iftop 命令是否存在
if ! command -v iftop &> /dev/null; then
    echo "iftop 命令不存在，请先安装 iftop。"
    exit 1
fi

# 检查是否提供了足够的参数
if [ "$#" -ne 3 ]; then
    echo "使用方法: $0 <采集时间> <指定网卡> <指定存放采集数据的目录>"
    exit 1
fi

# 读取参数
COLLECT_TIME=$1
INTERFACES=$2
OUTPUT_DIR=$3

# 检查输出目录是否存在，如果不存在则创建
if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
fi

# 检查指定的网卡是否存在
IFS=',' read -ra ADDR <<< "$INTERFACES"
for INTERFACE in "${ADDR[@]}"; do
    if ! ip link show "$INTERFACE" &> /dev/null; then
        echo "指定的网卡 $INTERFACE 不存在。"
        exit 1
    fi
done

# 启动后台监控
for INTERFACE in "${ADDR[@]}"; do
    OUTPUT_FILE="${OUTPUT_DIR}/${INTERFACE}.txt"
    echo "开始监控 $INTERFACE，数据将保存到 $OUTPUT_FILE"
    while true; do
        # 记录开始时间
        echo "Timestamp: $(date)" >> "$OUTPUT_FILE"
        # 执行 iftop 命令
        iftop -t -s 1 -i "$INTERFACE" >> "$OUTPUT_FILE"
        # 等待一秒钟
        sleep 1
    done &
done

echo "监控已启动，将在后台运行。"
# 等待指定的采集时间
sleep "$COLLECT_TIME"

# 采集时间到后停止监控
for INTERFACE in "${ADDR[@]}"; do
    pkill -f "iftop.*$INTERFACE"
done

echo "监控结束。"