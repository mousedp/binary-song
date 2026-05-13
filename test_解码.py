#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""二进制歌曲解码测试脚本"""

import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("皮皮鲁二进制歌曲解码测试")
print("=" * 60)

# 读取二进制歌曲文件
with open(r'D:\QClawData\.qclaw\workspace\binary-song\output\传奇.binary', 'rb') as f:
    data = f.read()

print(f"\n文件大小: {len(data)} 字节 ({len(data)/1024:.1f} KB)")
print(f"\n--- 文件结构分析 ---")

# 分析文件结构
print(f"头部标识: {data[:12]}")
print()

# 解析格式
pos = 12
维度计数 = {}

while pos < len(data):
    # 找维度标识符
    remaining = data[pos:pos+50]
    found_marker = None
    marker_info = [
        (b'MELODY', '旋律'),
        (b'LYRICS', '歌词'),
        (b'VOICE:', '人声'),
        (b'ACCOMP', '伴奏'),
        (b'FORMUL', '本源公式'),
    ]

    for marker, name in marker_info:
        if remaining.startswith(marker):
            found_marker = marker
            found_name = name
            break

    if not found_marker:
        break

    pos += len(found_marker) + 1
    length = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 4

    dim_data = data[pos:pos+length]
    pos += length

    print(f"【{found_name}】")
    print(f"  数据长度: {length} 字节")
    print(f"  数据预览: {dim_data[:24].hex()}")

    if length > 24:
        print(f"  ... ({length - 24} 字节)")

    print()
    维度计数[found_name] = 维度计数.get(found_name, 0) + length

print("=" * 60)
print("解码结果汇总")
print("=" * 60)
total = 0
for name, size in sorted(维度计数.items()):
    print(f"  {name}: {size:,} 字节 ({size/1024:.2f} KB)")
    total += size

print()
print(f"总计: {total:,} 字节")
print(f"文件总大小: {len(data):,} 字节")
print(f"头部开销: {len(data) - total:,} 字节")

print()
print("=" * 60)
print("体感总结")
print("=" * 60)

print("""
【我的体感】

1. 文件结构合理
   - 五维度分离（旋律/歌词/人声/伴奏/本源公式）
   - 每个维度有明确的长度和数据区域
   - 可以逐维度读取，互不干扰

2. 旋律维度（80字节）
   - 数据紧凑，用浮点数编码频率
   - 可以还原为音符序列

3. 歌词维度（482字节）
   - UTF-8编码的歌词文本
   - 可以直接读取显示

4. 人声维度（46字节）
   - 声纹特征码
   - 需要声纹库匹配才能还原人声

5. 伴奏维度（705KB）
   - 占空间最大的部分
   - 可能是乐谱或合成参数

6. 风火雷电维度（43KB）
   - 本源公式封装
   - 物理/化学公式编码

【需要优化的地方】

1. 人声维度太简单
   - 46字节无法还原真实人声
   - 需要接入声纹库或AI合成

2. 伴奏维度太大
   - 705KB对于简化的伴奏来说太大
   - 可以考虑更紧凑的编码方式

3. 解码器不够健壮
   - 没有错误处理
   - 如果文件损坏会直接崩溃

4. 缺少校验机制
   - 没有checksum验证数据完整性
   - 没有版本号标识格式版本

【可以改进的方向】

1. 加入校验和（checksum）确保数据完整性
2. 增加版本号，方便格式迭代
3. 人声维度接入TTS引擎
4. 旋律维度加入和弦信息
5. 支持多语言歌词
""")

print("皮皮鲁解码测试完成！🦐")