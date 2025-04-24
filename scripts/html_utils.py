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


def insert_default_resources(html_content, server_base_url):
    """
    将默认的 CSS 和 JavaScript 文件插入到 HTML 文件的 <head> 区块中，紧跟在 <title> 标签之后
    :param html_content: 输入的 HTML 内容
    :param server_base_url: 服务器基础路径，例如 'https://xiaopinggao.github.io/aitutor'
    :return: 插入了默认资源的 HTML 内容
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    title_tag = soup.find('title')
    if title_tag:
        # 创建新的 script 和 link 标签
        script_tag = soup.new_tag('script', src=f"{server_base_url.rstrip('/')}/doubao_chatbot.js")
        link_chat_styles = soup.new_tag('link', href=f"{server_base_url.rstrip('/')}/css/chat_styles.css", rel="stylesheet")
        link_font_awesome = soup.new_tag('link', href="https://cdn.bootcdn.net/ajax/libs/font-awesome/6.2.1/css/all.min.css", rel="stylesheet")

        # 将新的标签插入到 title 标签之后
        title_tag.insert_after(script_tag)
        script_tag.insert_after(link_chat_styles)
        link_chat_styles.insert_after(link_font_awesome)
    return str(soup)


def fix_page_meta_info(html_content, server_base_url, file_relative_path):
    """
    提取并替换 HTML 中的 OpenGraph 信息
    :param html_content: 输入的 HTML 内容
    :param server_base_url: 服务器基础路径，例如 'https://xiaopinggao.github.io/aitutor'
    :param file_relative_path: 文件的相对路径，例如 '/physics/lamp_diagnose.html'
    :return: 包含更新 OpenGraph 信息的 HTML 内容
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取页面标题作为 og:title
    title_tag = soup.find('title')
    og_title = title_tag.string if title_tag else '默认标题'

    # 拼接服务器路径和文件相对路径作为 og:url
    og_url = f"{server_base_url.rstrip('/')}/{file_relative_path.lstrip('/')}"

    # 截取页面文本内容的前一段字符作为 og:description
    text_content = soup.get_text(separator=' ', strip=True)
    import re
    title_pattern = re.escape(og_title)  # 转义标题内容以防止特殊字符干扰
    text_content = re.sub(f"^{title_pattern}\\s*", "", text_content, count=1)  # 去掉开头的 title 内容
    og_description = text_content[:100] + ('...' if len(text_content) > 100 else '')

    # 更新或创建 OpenGraph meta 标签
    opengraph_data = {
        'og:title': og_title,
        'og:type': 'website',  # 固定 og:type 为 website
        'og:url': og_url,
        'og:description': og_description,
    }

    for property_name, content_value in opengraph_data.items():
        if content_value is not None:
            old_meta = soup.find('meta', attrs={'property': property_name})
            if old_meta:
                # 修改现有的 meta 标签
                old_meta['content'] = content_value
            else:
                # 创建新的 meta 标签
                new_meta = soup.new_tag('meta', property=property_name, content=content_value)
                title_tag.insert_before(new_meta)

    # 新增：更新或创建 <link rel="canonical"> 标签
    canonical_link = soup.find('link', attrs={'rel': 'canonical'})
    if canonical_link:
        canonical_link['href'] = og_url
    else:
        new_canonical_link = soup.new_tag('link', rel='canonical', href=og_url)
        title_tag.insert_before(new_meta)

    # 更新 description 标签的内容为 og:description 的值
    description_meta = soup.find('meta', attrs={'name': 'description'})
    if description_meta:
        description_meta['content'] = og_description
    else:
        new_description_meta = soup.new_tag('meta', name='description', content=og_description)
        title_tag.insert_before(new_meta)

    # 更新 keywords 标签的内容为新的关键词列表
    keywords_meta = soup.find('meta', attrs={'name': 'keywords'})
    new_keywords = "豆荚AI学堂,AI个性化学习,AI写作,AI辅导作业,AI学习,AI提分,AI升学"
    if keywords_meta:
        keywords_meta['content'] = new_keywords
    else:
        new_keywords_meta = soup.new_tag('meta', name='keywords', content=new_keywords)
        title_tag.insert_before(new_meta)

    return str(soup)


def extract_and_save_first_image(html_content, output_dir, relative_file_path, server_base_url):
    """
    提取网页中的第一张内嵌图片并保存为本地文件，同时更新 og:image 字段。
    :param html_content: 输入的 HTML 内容
    :param output_dir: 输出文件目录路径
    :param relative_file_path: 源文件相对路径
    :param server_base_url: 服务器基础路径
    :return: 更新后的 HTML 内容
    """
    from bs4 import BeautifulSoup
    import base64
    import os

    soup = BeautifulSoup(html_content, 'html.parser')

    # 仅在 <div data-testid="message-list"><picture> 区块下寻找第一张图片
    img_tag = soup.select_one('div[data-testid="message-list"] picture img[src^="data:image"]')

    if img_tag:
        # 提取图片数据
        img_data = img_tag['src'].split(',')[1]
        img_format = img_tag['src'].split(';')[0].split('/')[-1]

        # 去除文件名中的 .html 后缀
        base_name = os.path.splitext(relative_file_path)[0]
        img_path = os.path.join(output_dir, 'imgs', f"{base_name}.{img_format}")

        # 确保目标目录存在
        os.makedirs(os.path.dirname(img_path), exist_ok=True)

        # 保存图片
        with open(img_path, 'wb') as f:
            f.write(base64.b64decode(img_data))

        # 更新 og:image 字段
        og_image_url = f"{server_base_url.rstrip('/')}/imgs/{base_name}.{img_format}"
        old_og_image = soup.find('meta', attrs={'property': 'og:image'})
        if old_og_image:
            old_og_image['content'] = og_image_url
        else:
            og_image_meta = soup.new_tag('meta', property='og:image', content=og_image_url)
            title_tag = soup.find('title')
            title_tag.insert_before(og_image_meta)

        return str(soup)
    else:
            # 移除原有的 og:image 标签
        old_og_image = soup.find('meta', attrs={'property': 'og:image'})
        if old_og_image:
            old_og_image.decompose()

        return str(soup)
