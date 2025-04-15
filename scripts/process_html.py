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
from html_utils import remove_specific_divs, add_banner_and_footer
from html_utils import remove_csp_meta, insert_default_resources
from html_utils import fix_page_meta_info

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_html_file(src_dir, output_dir, relative_file_path, banner_file, footer_file):
    """
    处理单个 HTML 文件
    :param src_dir: 源文件目录路径
    :param output_dir: 输出文件目录路径
    :param relative_file_path: 源文件相对路径
    :param banner_file: banner 文件名
    :param footer_file: footer 文件名
    """
    try:
        # 构造完整的输入文件路径
        input_file = os.path.join(src_dir, relative_file_path)
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
            'div[class*="footer-"] > div[class*="container-"] > div[class*="inner-"]',
        ]
        html_content = remove_specific_divs(html_content, css_selectors)

        # 移除 CSP meta 标签
        html_content = remove_csp_meta(html_content)

        server_base_url = 'https://xiaopinggao.github.io/aitutor'
        html_content = fix_page_meta_info(html_content, server_base_url, relative_file_path)

        # 插入默认资源
        html_content = insert_default_resources(html_content)

        # 添加 banner 和 footer
        banner_path = os.path.join(src_dir, banner_file)
        footer_path = os.path.join(src_dir, footer_file)
        html_content = add_banner_and_footer(html_content, banner_path, footer_path)

        # 构造完整的输出文件路径
        output_file = os.path.join(output_dir, relative_file_path)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)  # 确保目标目录存在
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
    parser.add_argument("--src_dir", required=True, help="源文件目录路径")
    parser.add_argument("--output_dir", required=True, help="输出文件目录路径")
    parser.add_argument("--src_file", required=True, help="源文件相对路径")
    parser.add_argument("--banner", default='banner.txt', help="Path to the banner file (default: banner.txt)")
    parser.add_argument("--footer", default='footer.txt', help="Path to the footer file (default: footer.txt)")

    args = parser.parse_args()

    process_html_file(args.src_dir, args.output_dir, args.src_file, args.banner, args.footer)