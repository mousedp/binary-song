#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""二进制歌曲解码器 - 修复版"""
import struct, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\QClawData\.qclaw\workspace\binary-song\output\传奇.binary', 'rb') as f:
    d = f.read()

print("=" * 60)
print("皮皮鲁二进制歌曲解码报告（修复版）")
print("=" * 60)

# 分析真实格式
# 从hex dump看: BinarySong|| 开头
# 然后是管道分隔符
# 然后是 MELODY: 标记

pos = 0
print(f"文件总大小: {len(d):,} 字节")
print(f"\n--- 头部分析 ---")
print(f"头部: {d[:12]}")

# 找到第一个维度标记
first_pipe = d.find(b'|', 12)
print(f"第一个管道 at {first_pipe}")

# 逐字节搜索所有位置
print("\n--- 关键字节位置 ---")
for i in range(12, 30):
    b = d[i]
    c = chr(b) if 32 <= b < 127 else '.'
    print(f"  pos {i}: 0x{b:02x} = {b} = '{c}'")

# 解析五维度
dims = [
    (b'MELODY:', '旋律'),
    (b'LYRICS:', '歌词'),
    (b'VOICE:', '人声'),
    (b'ACCOMP:', '伴奏'),
    (b'FORMULA:', '本源公式')
]

print("\n--- 维度解析 ---")
pos = 12
维度列表 = []

while pos < len(d):
    found = None
    for marker, name in dims:
        if d[pos:pos+len(marker)] == marker:
            found = (marker, name)
            break
    if not found:
        print(f"未找到维度标记，停在 pos={pos}, byte=0x{d[pos]:02x}")
        break
    
    marker, name = found
    marker_len = len(marker)
    print(f"\n【{name}】pos={pos}, marker={marker}")
    
    # 打印marker后的所有字节
    print(f"  marker后20字节: {d[pos+marker_len:pos+marker_len+20].hex()}")
    
    # 读取长度
    length = struct.unpack('<I', d[pos+marker_len:pos+marker_len+4])[0]
    print(f"  长度值: {length}")
    
    dim_data = d[pos+marker_len+4:pos+marker_len+4+length]
    pos += marker_len + 4 + length
    
    维度列表.append((name, length, dim_data))

print(f"\n成功解析维度数: {len(维度列表)}")

# 详细分析每个维度
print("\n" + "=" * 60)
for name, length, dim_data in 维度列表:
    print(f"\n【{name}】{length:,} 字节")
    if name == '歌词':
        text = dim_data.decode('utf-8', errors='ignore')
        lines = [l for l in text.split('\x00') if l.strip()]
        print(f"  歌词内容:")
        for l in lines:
            print(f"    {l}")
    elif name == '旋律':
        notes = []
        for i in range(0, len(dim_data), 8):
            if i+8 <= len(dim_data):
                freq = struct.unpack('<d', dim_data[i:i+8])[0]
                if freq > 0:
                    notes.append(round(freq, 1))
        print(f"  音符频率列表(前15个): {notes[:15]}")
        print(f"  音符数量: {len(notes)}")
    elif name == '人声':
        print(f"  声纹特征: {dim_data.hex()}")
    elif name == '伴奏':
        print(f"  伴奏数据: {dim_data[:40].hex()}")
    elif name == '本源公式':
        print(f"  公式数据: {dim_data[:40].hex()}")

print("\n" + "=" * 60)
print("体感报告")
print("=" * 60)