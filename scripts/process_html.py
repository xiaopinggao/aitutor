# -*- coding: utf-8 -*-
"""
process_html.py

This script processes HTML files by removing specific <div> tags and adding a banner and footer.
It can be used to process a single HTML file or multiple files in a directory.

Usage:
    python process_html.py <input_file> <output_file> [--banner_path <banner_path>] [--footer_path <footer_path>]

Author: Phillips Gao
Date: 2025-3-30
"""

import os
import sys
import logging
from html_utils import remove_csp_meta, remove_specific_divs, add_banner_and_footer

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_html_file(input_file, output_file, banner_path, footer_path):
    """
    处理单个 HTML 文件
    :param input_file: 输入 HTML 文件路径
    :param output_file: 输出 HTML 文件路径
    :param banner_path: banner 文件的路径
    :param footer_path: footer 文件的路径
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 移除指定的 <div> 标签
        css_selectors = [
            'div[class*="header-"] > div[class="relative"]',
            'div[class*="to-bottom-button-"]',
            'div[data-message-action-bar="1"]',
            'div[data-testid="suggest_message_list"]',
            'div[data-testid="chat_footer_skill_bar"]',
            'div[data-testid="chat_input"]',
            ]
        html_content = remove_specific_divs(html_content, css_selectors)

        # 移除 CSP meta 标签
        html_content = remove_csp_meta(html_content)

        # 添加 banner 和 footer
        html_content = add_banner_and_footer(html_content, banner_path, footer_path)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"已处理 {input_file}，处理后的文件保存到 {output_file}")
    except FileNotFoundError as e:
        logging.error(f"文件未找到: {e}")
    except IOError as e:
        logging.error(f"IO 错误: {e}")
    except Exception as e:
        logging.error(f"处理 {input_file} 时出错: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process a single HTML file by adding a banner and footer.")
    parser.add_argument("input_file", help="Path to the input HTML file")
    parser.add_argument("output_file", help="Path to the output HTML file")
    parser.add_argument("--banner_path", default='banner.txt', help="Path to the banner file (default: banner.txt)")
    parser.add_argument("--footer_path", default='footer.txt', help="Path to the footer file (default: footer.txt)")

    args = parser.parse_args()

    process_html_file(args.input_file, args.output_file, args.banner_path, args.footer_path)