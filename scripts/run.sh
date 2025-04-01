#!/bin/bash

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 定义根目录
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# 定义源目录和目标目录
SRC_DIR="$ROOT_DIR/src"
HTML_DIR="$ROOT_DIR/docs"

# 创建目标目录（如果不存在）
mkdir -p "$HTML_DIR"

# 递归遍历src目录下的所有html文件
find "$SRC_DIR" -type f -name "*.html" -not -name "index.html" | while read -r file; do
    # 获取文件相对于src目录的路径
    relative_path="${file#$SRC_DIR/}"
    # 获取文件所在的子目录
    dir_path=$(dirname "$relative_path")
    # 创建对应的子目录（如果不存在）
    mkdir -p "$HTML_DIR/$dir_path"
    # 获取文件名
    file_name=$(basename "$file")
    # 构建输出文件路径
    output_file="$HTML_DIR/$relative_path"
    # 调用process_html.py处理文件
    echo python "$SCRIPT_DIR/process_html.py" "$file" "$output_file" --banner_path "$SRC_DIR/banner.txt" --footer_path "$SRC_DIR/footer.txt"
    python "$SCRIPT_DIR/process_html.py" "$file" "$output_file" --banner_path "$SRC_DIR/banner.txt" --footer_path "$SRC_DIR/footer.txt"
done
