#!/bin/bash  

# 检查输入参数  
if [ "$#" -ne 1 ] && [ "$#" -ne 2 ]; then  
    echo "用法: $0 <文件> <类型 (mac|ip)>(可选)"  
    exit 1  
fi  

FILE=$1  
TYPE=$2

if [ -z "$TYPE" ]; then  
    sort "$File" | uniq -c | sort -nr
    exit 0
fi
# 根据输入的类型统计  
if [ "$TYPE" == "mac" ]; then  
    # 统计 mac 地址的重复出现次数  
    awk -F',' '{print $1}' "$FILE" | sort | uniq -c | sort -nr  
elif [ "$TYPE" == "ip" ]; then  
    # 统计 ip 地址的重复出现次数  
    awk -F',' '{print $2}' "$FILE" | sort | uniq -c | sort -nr  
else
    echo "错误: 统计类型必须是 'mac' 或 'ip'"  
    exit 1  
fi