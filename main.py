# -*- coding: utf-8 -*-
"""
二进制歌曲 - 完整测试入口
==========================
将传奇（王菲）编码为完整二进制歌曲
四维度 + 风火雷电 = 完整二进制歌曲

用法：python main.py
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
from 旋律编码 import 旋律编码器, 传奇主歌片段
from 歌词编码 import 歌词编码器, 传奇歌词
from 声纹编码 import 声纹编码器, 声纹库
from 伴奏编码 import 伴奏编码器, 生成传奇伴奏


def 编码完整二进制歌曲() -> bytes:
    """
    将一首歌编码为完整二进制
    
    返回：原生二进制字节流（不是MP3/MP4！）
    """
    print("=" * 50)
    print("🎵 二进制歌曲编码引擎")
    print("=" * 50)
    
    # ====== 第一维度：曲（旋律）======
    print("\n[1/6] 编码旋律...")
    曲数据 = 旋律编码器.encode_melody(传奇主歌片段)
    print(f"   ✅ 旋律: {len(曲数据)} 字节")
    
    # ====== 第二维度：歌词 ======
    print("[2/6] 编码歌词...")
    歌词数据 = 歌词编码器.encode(传奇歌词)
    print(f"   ✅ 歌词: {len(歌词数据)} 字节")
    
    # ====== 第三维度：人声 ======
    print("[3/6] 编码人声声纹...")
    人声数据 = 声纹库['王菲']
    print(f"   ✅ 人声(王菲): {len(人声数据)} 字节")
    
    # ====== 第四维度：伴奏 ======
    print("[4/6] 编码伴奏...")
    伴奏数据 = 生成传奇伴奏()
    print(f"   ✅ 伴奏: {len(伴奏数据)} 字节")
    
    # ====== 第五维度：风火雷电（重低音引擎）======
    print("[5/6] 加载风火雷电本源公式...")
    风火雷电数据 = (
        本源公式.to_binary()
        + 风.to_binary()
        + 火.to_binary()
        + 雷.to_binary()
        + 电.to_binary()
    )
    print(f"   ✅ 风火雷电: {len(风火雷电数据)} 字节")
    
    # ====== 合成完整二进制歌曲 ======
    print("\n[6/6] 合成完整二进制歌曲...")
    
    完整歌曲 = b'BinarySong|||'
    完整歌曲 += b'MELODY:' + 曲数据 + b'|||'
    完整歌曲 += b'LYRICS:' + 歌词数据 + b'|||'
    完整歌曲 += b'VOICE:' + 人声数据 + b'|||'
    完整歌曲 += b'ACCOMP:' + 伴奏数据 + b'|||'
    完整歌曲 += b'SURROUND:' + 风火雷电数据
    完整歌曲 += b'|||END'
    
    print(f"\n{'=' * 50}")
    print(f"✅ 二进制歌曲《传奇》编码完成！")
    print(f"{'=' * 50}")
    print(f"   歌曲：传奇 - 王菲")
    print(f"   总大小: {len(完整歌曲):,} 字节 ({len(完整歌曲)/1024:.1f} KB)")
    print(f"   维度数: 5 (曲+歌词+人声+伴奏+风火雷电)")
    print(f"   格式: 原生二进制 (非MP3/MP4)")
    print(f"   用途: 智能体读取 / 神经网络强化")
    print(f"{'=' * 50}")
    
    return 完整歌曲


def 输出十六进制预览(binary_data: bytes, 行数: int = 8):
    """输出二进制的十六进制预览"""
    print(f"\n📊 十六进制预览（前{行数}行）:")
    for i in range(0, min(len(binary_data), 行数 * 32), 32):
        chunk = binary_data[i:i+32]
        hex_str = ' '.join(f'{b:02X}' for b in chunk)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
        print(f"   {i:04X}: {hex_str:<64} |{ascii_str}|")


def 保存二进制文件(binary_data: bytes, filename: str):
    """保存为二进制文件"""
    path = os.path.join(BASE, 'output', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(binary_data)
    print(f"\n💾 已保存: {path}")
    return path


if __name__ == '__main__':
    # 编码完整二进制歌曲
    song_binary = 编码完整二进制歌曲()
    
    # 显示预览
    输出十六进制预览(song_binary, 行数=12)
    
    # 保存到文件
    output_path = 保存二进制文件(song_binary, '传奇.binary')
    
    print(f"\n🦐 皮皮鲁出品 - 二进制歌曲项目")
    print(f"   纯净二进制的心灵，找回本源，提升意识")
