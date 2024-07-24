#!/bin/bash  

# 检查输入参数  
if [ "$#" -ne 2 ]; then  
    echo "用法: $0 <目录> <关键字>"  
    exit 1  
fi  

DIRECTORY=$1  
KEYWORD=$2  

# 遍历目录  
find "$DIRECTORY" -type f | while read -r file; do  
    if [[ "$file" == *.log ]]; then  
        echo "搜索 $file 中的关键字 '$KEYWORD':"  
        grep "$KEYWORD" "$file" && echo  
    elif [[ "$file" == *.xz ]]; then  
        echo "搜索 $file 中的关键字 '$KEYWORD':"  
        xzcat "$file" | grep "$KEYWORD" && echo  
    fi  
done