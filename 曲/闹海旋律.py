# -*- coding: utf-8 -*-
"""
闹海（不良人）主歌旋律
简化版二进制编码
"""

# 闹海主歌片段
# 基于不良人动画主题曲的简化旋律
闹海主歌片段 = [
    # 第一句：闹海翻江，威震四方
    (3, 'mid', 'quarter'),   # 咪
    (5, 'mid', 'quarter'),   # 唆
    (6, 'mid', 'eighth'),    # 拉
    (5, 'mid', 'eighth'),    # 唆
    (3, 'mid', 'half'),      # 咪（长音）
    
    # 第二句：英雄本色，不惧风浪
    (1, 'mid', 'quarter'),   # 哆
    (3, 'mid', 'quarter'),   # 咪
    (5, 'mid', 'eighth'),    # 唆
    (3, 'mid', 'eighth'),    # 咪
    (2, 'mid', 'half'),      # 来（长音）
    
    # 副歌部分
    (6, 'mid', 'quarter'),   # 拉
    (5, 'mid', 'quarter'),   # 唆
    (3, 'mid', 'eighth'),    # 咪
    (5, 'mid', 'eighth'),    # 唆
    (6, 'mid', 'half'),      # 拉（长音）
    
    # 结尾
    (5, 'mid', 'quarter'),   # 唆
    (3, 'mid', 'quarter'),   # 咪
    (1, 'mid', 'half'),      # 哆（长音结束）
]

if __name__ == '__main__':
    print(f"闹海主歌片段音符数: {len(闹海主歌片段)}")
