#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""搜索现成的歌声声纹库、人声数据集"""

import sys
import json
import urllib.request
import urllib.parse

def 搜索_github(关键词, 最多=10):
    """搜索GitHub仓库"""
    query = urllib.parse.quote(关键词)
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={最多}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/vnd.github.v3+json')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            print(f"\n=== GitHub搜索结果：{关键词} ===")
            for i, repo in enumerate(data['items'][:最多], 1):
                print(f"{i}. {repo['full_name']}")
                print(f"   URL: {repo['html_url']}")
                print(f"   描述: {repo.get('description', '无描述')}")
                print(f"   Stars: {repo['stargazers_count']}")
                print()
    
    except Exception as e:
        print(f"搜索失败: {e}")

def 搜索_歌声数据集():
    """搜索歌声相关的数据集"""
    print("开始搜索现成的歌声数据集、声纹库...")
    
    # 搜索关键词列表
    关键词列表 = [
        "singing voice dataset",
        "vocal timbre library",
        "singing voice separation",
        "acapella dataset",
        "karaoke vocal library"
    ]
    
    for 关键词 in 关键词列表:
        搜索_github(关键词, 最多=3)
        print("-" * 50)

if __name__ == "__main__":
    搜索_歌声数据集()
    print("\n搜索完成。")
