# -*- coding: utf-8 -*-
"""
add_bookmarks.py

功能描述：
    该脚本用于为PDF文件添加书签。通过分析PDF文档的文本内容，自动识别可能的章节标题，并将这些标题添加为书签。
    书签的层级结构基于标题的格式和位置，支持中文和数字编号的标题识别。

使用方法：
    1. 确保已安装PyMuPDF库（pip install pymupdf）
    2. 运行脚本时提供1个参数：输入PDF文件路径，生成的文件将覆盖输入文件。
    3. 示例：python add_bookmarks.py input.pdf

依赖库：
    - PyMuPDF (fitz) works on pip install pymupdf==1.25.3
    - re (正则表达式)
    - sys (系统参数)
    - os (文件路径操作)

作者: Phillips Gao
日期: 2025-3-30
"""

import fitz  # PyMuPDF
import re
import sys
import os

def extract_titles(doc):
    bookmarks = []

    print("解析每一页标题...")
    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        blocks = page.get_text("dict")["blocks"]

        level1_texts = []
        level2_texts = []

        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                line_text = ""
                sizes = []

                for span in line["spans"]:
                    text = re.sub(r'[\u200b\u200c\u200d]+', '', span.get("text", "")).strip()
                    size = span.get("size", 0)
                    if text:
                        line_text += text
                        sizes.append(size)

                if not line_text or not sizes:
                    continue

                avg_size = sum(sizes) / len(sizes)

                if avg_size > 40:
                    level1_texts.append(line_text.strip())
                elif 30 < avg_size <= 40:
                    level2_texts.append(line_text.strip())

        if level1_texts:
            bookmarks.append((1, " ".join(level1_texts), page_number))
            print(f"{level1_texts}(p{page_number + 1})")
        if level2_texts:
            bookmarks.append((2, " ".join(level2_texts), page_number))
            print(f"-- {level2_texts}(p{page_number + 1})")

    return bookmarks


def add_bookmarks(input_pdf):
    doc = fitz.open(input_pdf)
    titles = extract_titles(doc)

    if not titles:
        print("⚠️ 未找到可识别的标题，未添加书签。")
    else:
        toc = [[level, title, page_num + 1] for (level, title, page_num) in titles]
        doc.set_toc(toc)
        print(f"📑 添加了 {len(toc)} 条书签：")
        for t in toc:
            indent = "  " * (t[0] - 1)
            print(f"{indent}- {t[1]}（p{t[2]}）")

    # 保存原文件（覆盖写入）
    doc.save(input_pdf, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    print(f"✅ 已保存带书签的 PDF 文件到：{input_pdf}")

def main():
    if len(sys.argv) < 2:
        print("用法：python add_bookmarks.py 输入文件1.pdf 输入文件2.pdf ...")
        sys.exit(1)

    input_pdfs = sys.argv[1:]

    for input_pdf in input_pdfs:
        if not os.path.exists(input_pdf):
            print(f"❌ 输入文件不存在：{input_pdf}")
            continue

        print(f"处理文件: {input_pdf}")
        add_bookmarks(input_pdf)

if __name__ == "__main__":
    main()
