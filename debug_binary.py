#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\QClawData\.qclaw\workspace\binary-song\output\传奇.binary', 'rb') as f:
    d = f.read()

print(f"文件总大小: {len(d)} 字节")
print()

# 逐字节分析前200字节
print("=== 前200字节分析 ===")
for i in range(0, min(200, len(d)), 16):
    hex_part = ' '.join(f'{b:02x}' for b in d[i:i+16])
    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in d[i:i+16])
    print(f"{i:04x}: {hex_part:<48} | {ascii_part}")

print()
print("=== 搜索维度标记 ===")
dims = {b'MELODY': '旋律', b'LYRICS': '歌词', b'VOICE:': '人声', b'ACCOMP': '伴奏', b'FORMUL': '本源公式'}
pos = 12
while pos < len(d):
    found = None
    for marker, name in dims.items():
        if d[pos:pos+len(marker)] == marker:
            found = (marker, name)
            break
    if found:
        marker, name = found
        sep = d[pos+len(marker)]
        length = struct.unpack('<I', d[pos+len(marker)+1:pos+len(marker)+5])[0]
        dim_data = d[pos+len(marker)+5:pos+len(marker)+5+length]
        print(f"【{name}】位置:{pos}, 分隔符:0x{sep:02x}, 长度:{length}, 数据前20字节:{dim_data[:20].hex()}")
        pos += len(marker) + 5 + length
    else:
        break