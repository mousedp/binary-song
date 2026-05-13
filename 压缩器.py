#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""皮皮鲁二进制歌曲压缩器 - 使用ZSTD算法"""
import zstandard as zstd
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("皮皮鲁二进制歌曲压缩器")
print("=" * 60)

# 读取原始文件
input_file = r'D:\QClawData\.qclaw\workspace\binary-song\output\传奇.binary'
with open(input_file, 'rb') as f:
    original_data = f.read()

original_size = len(original_data)
print(f"\n原始文件: {original_size:,} 字节 ({original_size/1024:.1f} KB)")

# 使用ZSTD压缩
cctx = zstd.ZstdCompressor(level=3)
compressed = cctx.compress(original_data)
compressed_size = len(compressed)

print(f"压缩后: {compressed_size:,} 字节 ({compressed_size/1024:.1f} KB)")
print(f"压缩比: {original_size/compressed_size:.2f}x")
print(f"节省: {(1-compressed_size/original_size)*100:.1f}%")

# 保存压缩文件（带.zst扩展名）
output_file = input_file + '.zst'
with open(output_file, 'wb') as f:
    f.write(compressed)

print(f"\n已保存: {output_file}")

# 验证解压
dctx = zstd.ZstdDecompressor()
decompressed = dctx.decompress(compressed)
if decompressed == original_data:
    print("✅ 解压验证通过，数据完整")
else:
    print("❌ 解压验证失败，数据不匹配")

# 同时生成.tar.zst格式（保留文件名）
tar_file = r'D:\QClawData\.qclaw\workspace\binary-song\output\传奇.tar.zst'
with open(tar_file, 'wb') as f:
    f.write(compressed)
print(f"别名: {tar_file}")

print("\n压缩完成！🦐")
print("=" * 60)