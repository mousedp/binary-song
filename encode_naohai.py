# -*- coding: utf-8 -*-
"""
二进制歌曲 - 《闹海》编码脚本
=============================
将闹海（不良人主题曲）编码为完整二进制歌曲
四维度 + 风火雷电 = 完整二进制歌曲

用法：python encode_naohai.py
"""

import sys
import os

# 添加各模块路径
BASE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(BASE, '内核', '风火雷电'))
sys.path.insert(0, os.path.join(BASE, '曲'))
sys.path.insert(0, os.path.join(BASE, '歌词'))
sys.path.insert(0, os.path.join(BASE, '人声'))
sys.path.insert(0, os.path.join(BASE, '伴奏'))
sys.path.insert(0, os.path.join(BASE, '外壳'))

from 本源公式 import 本源公式, 风, 火, 雷, 电
from 旋律编码 import 旋律编码器
from 歌词编码 import 歌词编码器
from 伴奏编码 import 生成闹海伴奏
from 闹海旋律 import 闹海主歌片段
from 闹海歌词 import 闹海歌词


def 编码闹海二进制歌曲() -> bytes:
    """
    将《闹海》编码为完整二进制
    """
    print("=" * 50)
    print("二进制歌曲编码引擎 - 《闹海》")
    print("=" * 50)
    
    # 第一维度：曲（旋律）
    print("\n[1/5] 编码旋律...")
    曲数据 = 旋律编码器.encode_melody(闹海主歌片段)
    print(f"   完成: {len(曲数据)} 字节 ({len(闹海主歌片段)} 个音符)")
    
    # 第二维度：歌词
    print("[2/5] 编码歌词...")
    歌词数据 = 歌词编码器.encode(闹海歌词.strip())
    print(f"   完成: {len(歌词数据)} 字节 ({len(闹海歌词.strip())} 字)")
    
    # 第三维度：伴奏（复用传奇伴奏生成逻辑）
    print("[3/5] 编码伴奏...")
    伴奏数据 = 生成闹海伴奏()
    print(f"   完成: {len(伴奏数据)} 字节")
    
    # 第四维度：风火雷电
    print("[4/5] 加载风火雷电本源公式...")
    风火雷电数据 = (
        本源公式.to_binary()
        + 风.to_binary()
        + 火.to_binary()
        + 雷.to_binary()
        + 电.to_binary()
    )
    print(f"   完成: {len(风火雷电数据)} 字节")
    
    # 合成完整二进制歌曲
    print("\n[5/5] 合成完整二进制歌曲...")
    
    # 紧凑二进制格式：1B魔数 + 1B版本 + [1B tag + 2B len + data]...
    # tags: 0x01=旋律 0x02=歌词 0x03=伴奏 0x04=风火雷电 0x05=人声
    import struct
    完整歌曲 = bytes([0xB5, 0x01])  # 魔数0xB5 + 版本1
    for tag, data in [(0x01, 曲数据), (0x02, 歌词数据), (0x03, 伴奏数据), (0x04, 风火雷电数据)]:
        完整歌曲 += bytes([tag]) + struct.pack('>H', len(data)) + data
    
    print(f"\n{'=' * 50}")
    print(f"二进制歌曲《闹海》编码完成！")
    print(f"{'=' * 50}")
    print(f"   歌曲：闹海 - 不良人")
    print(f"   总大小: {len(完整歌曲):,} 字节 ({len(完整歌曲)/1024:.1f} KB)")
    print(f"   维度数: 4 (曲+歌词+伴奏+风火雷电)")
    print(f"{'=' * 50}")
    
    return 完整歌曲


def 保存二进制文件(binary_data: bytes, filename: str):
    """保存为二进制文件"""
    path = os.path.join(BASE, 'output', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(binary_data)
    print(f"\n已保存: {path}")
    return path


if __name__ == '__main__':
    # 编码《闹海》
    song_binary = 编码闹海二进制歌曲()
    
    # 保存到文件
    output_path = 保存二进制文件(song_binary, '闹海.binary')
    
    print(f"\n皮皮鲁出品 - 二进制歌曲项目")
    print(f"   第二首歌：《闹海》完成！")
