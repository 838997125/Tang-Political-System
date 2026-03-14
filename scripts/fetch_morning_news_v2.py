#!/usr/bin/env python3
"""
早朝新闻采集脚本 V2
由于网络限制，使用模拟数据或本地缓存
"""
import json
import pathlib
import datetime
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
DATA = REPO / "data"
DATA.mkdir(exist_ok=True)

# 示例新闻数据（实际使用时可以从 RSS 或 API 获取）
SAMPLE_NEWS = {
    "politics": [
        {"title": "示例政治新闻1", "summary": "这是政治新闻摘要", "source": "新华网", "url": "https://example.com/1", "image_url": "", "published": "today"},
        {"title": "示例政治新闻2", "summary": "这是政治新闻摘要", "source": "人民网", "url": "https://example.com/2", "image_url": "", "published": "today"},
    ],
    "military": [
        {"title": "示例军事新闻1", "summary": "这是军事新闻摘要", "source": "央视军事", "url": "https://example.com/3", "image_url": "", "published": "today"},
    ],
    "economy": [
        {"title": "示例经济新闻1", "summary": "这是经济新闻摘要", "source": "财经网", "url": "https://example.com/4", "image_url": "", "published": "today"},
    ],
    "ai": [
        {"title": "示例AI新闻1", "summary": "这是AI新闻摘要", "source": "机器之心", "url": "https://example.com/5", "image_url": "", "published": "today"},
    ]
}


def main():
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    
    print(f"[{time_str}] Generating morning news template...")
    print("Note: Due to network restrictions, using sample data.")
    print("Please replace with real news from RSS or other sources.")
    
    categories = [
        {"key": "politics", "label": "政治", "items": SAMPLE_NEWS["politics"]},
        {"key": "military", "label": "军事", "items": SAMPLE_NEWS["military"]},
        {"key": "economy", "label": "经济", "items": SAMPLE_NEWS["economy"]},
        {"key": "ai", "label": "AI大模型", "items": SAMPLE_NEWS["ai"]},
    ]
    
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


if __name__ == "__main__":
    main()
