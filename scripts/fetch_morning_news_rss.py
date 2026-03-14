#!/usr/bin/env python3
"""
早朝新闻采集脚本 - RSS 版本
使用 RSS 订阅源采集新闻
"""
import json
import pathlib
import datetime
import subprocess
import sys
import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import ssl

REPO = pathlib.Path(__file__).resolve().parent.parent
DATA = REPO / "data"
DATA.mkdir(exist_ok=True)

# 禁用 SSL 验证
ssl._create_default_https_context = ssl._create_unverified_context

# RSS 源配置 - 使用国内可访问的 RSS 源
RSS_SOURCES = {
    "politics": [
        {"name": "BBC中文", "url": "https://rsshub.app/bbc/chinese"},
        {"name": "路透中文", "url": "https://rsshub.app/reuters/investigates/china"},
    ],
    "military": [
        {"name": "新浪军事", "url": "https://rsshub.app/sina/news/mil"},
    ],
    "economy": [
        {"name": "新浪财经", "url": "https://rsshub.app/sina/finance"},
        {"name": "财新", "url": "https://rsshub.app/caixin/latest"},
    ],
    "ai": [
        {"name": "机器之心", "url": "https://rsshub.app/jiqizhixin"},
        {"name": "量子位", "url": "https://rsshub.app/qbitai"},
    ]
}


def fetch_rss(url, timeout=10):
    """获取 RSS 内容"""
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"      Error fetching {url}: {e}")
        return None


def parse_rss(xml_content):
    """解析 RSS XML"""
    items = []
    if not xml_content:
        return items
    
    try:
        # 尝试解析 XML
        root = ET.fromstring(xml_content)
        
        # RSS 2.0
        for item in root.findall('.//item'):
            title = item.find('title')
            link = item.find('link')
            description = item.find('description')
            pub_date = item.find('pubDate')
            
            title_text = title.text if title is not None else ""
            link_text = link.text if link is not None else ""
            desc_text = description.text if description is not None else ""
            pub_text = pub_date.text if pub_date is not None else "today"
            
            # 清理 HTML 标签
            desc_text = re.sub(r'<[^>]+>', '', desc_text)
            desc_text = desc_text[:100] + "..." if len(desc_text) > 100 else desc_text
            
            if title_text and link_text:
                items.append({
                    "title": title_text.strip(),
                    "summary": desc_text.strip(),
                    "url": link_text.strip(),
                    "published": pub_text
                })
    except Exception as e:
        print(f"      Parse error: {e}")
    
    return items


def main():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    
    print(f"[{time_str}] Starting RSS news collection...")
    
    categories = []
    
    for category_key, sources in RSS_SOURCES.items():
        print(f"  Category: {category_key}")
        all_items = []
        
        for source in sources:
            print(f"    Fetching: {source['name']}")
            xml = fetch_rss(source['url'])
            items = parse_rss(xml)
            
            # 添加来源信息
            for item in items:
                item['source'] = source['name']
                item['image_url'] = ""
            
            all_items.extend(items[:3])  # 每个源取前3条
            print(f"      Found {len(items)} items")
        
        # 去重（基于标题）
        seen_titles = set()
        unique_items = []
        for item in all_items:
            if item['title'] not in seen_titles:
                seen_titles.add(item['title'])
                unique_items.append(item)
        
        categories.append({
            "key": category_key,
            "label": get_category_label(category_key),
            "items": unique_items[:5]  # 每类最多5条
        })
    
    # 构建输出
    output = {
        "date": date_str,
        "generatedAt": time_str,
        "categories": categories
    }
    
    # 保存到文件
    output_file = DATA / "morning_brief.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"[{datetime.datetime.now().strftime('%H:%M')}] News saved to {output_file}")
    
    # 触发刷新
    print("Triggering data refresh...")
    try:
        subprocess.run(
            [sys.executable, str(REPO / "scripts" / "refresh_live_data.py")],
            cwd=str(REPO),
            timeout=30
        )
        print("Refresh completed")
    except Exception as e:
        print(f"Refresh failed: {e}")
    
    return output


def get_category_label(key):
    labels = {
        "politics": "政治",
        "military": "军事",
        "economy": "经济",
        "ai": "AI大模型"
    }
    return labels.get(key, key)


if __name__ == "__main__":
    main()
