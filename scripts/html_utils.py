# -*- coding: utf-8 -*-
"""
html_utils.py

This module provides utility functions to manipulate HTML content.
It includes functions to remove specific <div> tags and to add a banner and footer to HTML content.

Author: Phillips Gao
Date: 2025-3-30
"""

from bs4 import BeautifulSoup
import logging

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def remove_csp_meta(html_content):
    """
    移除网页 head 中的 http-equiv="content-security-policy" 这个 meta 字段
    :param html_content: 输入的 HTML 内容
    :return: 处理后的 HTML 内容
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    csp_meta = soup.find('meta', attrs={'http-equiv': 'content-security-policy'})
    if csp_meta:
        csp_meta.decompose()
    return str(soup)


def remove_specific_divs(html_content, css_selectors):
    """
    移除指定的 <div> 标签及其内容
    :param html_content: 输入的 HTML 内容
    :param css_selectors: 包含 CSS 选择器的列表
    :return: 处理后的 HTML 内容
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    for css_selector in css_selectors:
        target_divs = soup.select(css_selector)
        for div in target_divs:
            div.decompose()
    return str(soup)


def add_banner_and_footer(html_content, banner_path, footer_path):
    """
    为 HTML 内容添加统一的 banner 和 footer
    :param html_content: 输入的 HTML 内容
    :param banner_path: banner 文件的路径
    :param footer_path: footer 文件的路径
    :return: 添加了 banner 和 footer 的 HTML 内容
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    try:
        with open(banner_path, 'r', encoding='utf-8') as f:
            banner = BeautifulSoup(f.read(), 'html.parser')
        with open(footer_path, 'r', encoding='utf-8') as f:
            footer = BeautifulSoup(f.read(), 'html.parser')

        # 提取 html_content 中的标题
        title_tag = soup.find('title')
        title_text = title_tag.string if title_tag else '默认标题'

        # 替换 banner 中的 __TITLE__ 字符串
        for tag in banner.find_all(string=lambda text: text and '__TITLE__' in text):
            tag.replace_with(tag.replace('__TITLE__', title_text))

        # 找到特定的 div，插入banner和footer
        target_div = soup.select_one('div[class*="message-list-"] > div[data-testid="scroll_view"]')
        if target_div and target_div.parent and target_div.parent.parent:
            anchor_div = target_div.parent.parent
            anchor_div.insert_before(banner)
            anchor_div.insert_after(footer)
    except FileNotFoundError:
        logging.error(f"未找到 banner 或 footer 文件，请检查路径: {banner_path}, {footer_path}")
    except Exception as e:
        logging.error(f"读取 banner 或 footer 文件时出错: {e}")
    return str(soup)


def insert_default_resources(html_content):
    """
    将默认的 CSS 和 JavaScript 文件插入到 HTML 文件的 <head> 区块中，紧跟在 <title> 标签之后
    :param html_content: 输入的 HTML 内容
    :return: 插入了默认资源的 HTML 内容
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    title_tag = soup.find('title')
    if title_tag:
        # 创建新的 script 和 link 标签
        script_tag = soup.new_tag('script', src="../doubao_chatbot.js")
        link_chat_styles = soup.new_tag('link', href="../css/chat_styles.css", rel="stylesheet")
        link_font_awesome = soup.new_tag('link', href="https://cdn.bootcdn.net/ajax/libs/font-awesome/6.2.1/css/all.min.css", rel="stylesheet")

        # 将新的标签插入到 title 标签之后
        title_tag.insert_after(script_tag)
        script_tag.insert_after(link_chat_styles)
        link_chat_styles.insert_after(link_font_awesome)
    return str(soup)
