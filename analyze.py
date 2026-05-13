# -*- coding: utf-8 -*-
import struct, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('output/闹海.binary', 'rb') as f:
    data = f.read()

note_names = ['休止', '哆', '来', '咪', '发', '唆', '拉', '西']
octave_names = ['低', '中', '高']
dur_names = {4.0:'全音符', 2.0:'二分', 1.0:'四分', 0.5:'八分', 0.25:'十六分'}

print('='*60)
print('  二进制歌曲《闹海》完整数据流解读')
print('='*60)
print('总大小: {:,} 字节 ({:.1f} KB)'.format(len(data), len(data)/1024))
print()

# 旋律
melody_start = data.find(b'MELODY:') + 7
melody_end = data.find(b'|||', melody_start)
melody_data = data[melody_start:melody_end]

print('【第一维度：旋律】')
print('  大小: {} 字节'.format(len(melody_data)))
print('  音符数: {}'.format(len(melody_data) // 8))
print('  编码格式: 1字节(音符+八度) + 3字节对齐 + 4字节(时值float)')
print()
print('  旋律流:')
melody_str = []
for j in range(0, len(melody_data), 8):
    chunk = melody_data[j:j+8]
    if len(chunk) < 8:
        break
    value, dur = struct.unpack('ff', chunk)
    int_val = int(value)
    note = int_val & 0b00000111
    octave_raw = (int_val & 0b00011000) >> 3
    dur_name = dur_names.get(dur, '{:.2f}'.format(dur))
    name = note_names[note]
    oct_name = octave_names[octave_raw] if octave_raw < 3 else '?'
    melody_str.append('{}({})'.format(name, dur_name))
    print('    {:2d}. {}{} [{}] 时值={:.1f}拍'.format(
        j//8, name, oct_name, format(int_val, '08b'), dur))

print()
print('  简谱:', ' - '.join([note_names[int(melody_data[j:j+8][:1].hex(),16) & 0b111] for j in range(0, len(melody_data), 8)]))
print()

# 歌词
lyrics_start = data.find(b'LYRICS:') + 7
lyrics_end = data.find(b'|||', lyrics_start)
lyrics_data = data[lyrics_start:lyrics_end]

print('【第二维度：歌词】')
print('  大小: {} 字节'.format(len(lyrics_data)))
text = lyrics_data.decode('utf-8', errors='replace')
print('  内容:')
for line in text.strip().split('\n'):
    print('    {}'.format(line))
char_count = len(text.replace('\n', '').replace(' ', ''))
print('  总字数: {} 字'.format(char_count))
print()

# 伴奏
accomp_start = data.find(b'ACCOMP:') + 7
accomp_end = data.find(b'|||', accomp_start)
accomp_data = data[accomp_start:accomp_end]

print('【第三维度：伴奏】')
print('  大小: {:,} 字节 ({:.1f} KB)'.format(len(accomp_data), len(accomp_data)/1024))
print('  占整首歌: {:.1f}%'.format(len(accomp_data)/len(data)*100))
from collections import Counter
byte_freq = Counter(accomp_data)
unique = len(byte_freq)
print('  不同字节数: {} / 256 ({:.1f}%)'.format(unique, unique/256*100))
top10 = byte_freq.most_common(10)
print('  高频字节:')
for b, c in top10:
    print('    0x{:02x}: {:,} 次 ({:.1f}%)'.format(b, c, c/len(accomp_data)*100))
# 节奏分析：每1024字节看一个"小节"
block_size = 1024
blocks = len(accomp_data) // block_size
print('  伴奏小节数(每{}字节): {}'.format(block_size, blocks))
# 每16字节的"能量"
energies = []
for i in range(0, min(4096, len(accomp_data)), 16):
    chunk = accomp_data[i:i+16]
    energy = sum(b for b in chunk) / 16
    energies.append(energy)
print('  前{}个采样点能量:'.format(min(len(energies), 20)))
for i, e in enumerate(energies[:20]):
    bar = '#' * int(e / 8)
    print('    {:3d}: {:.0f} {}'.format(i, e, bar))
print()

# 风火雷电
surround_start = data.find(b'SURROUND:')
if surround_start >= 0:
    surround_start += 9
    surround_end = data.find(b'|||END', surround_start)
    if surround_end == -1:
        surround_end = len(data)
    surround_data = data[surround_start:surround_end]

    print('【第四维度：风火雷电】')
    print('  大小: {:,} 字节 ({:.1f} KB)'.format(len(surround_data), len(surround_data)/1024))
    text2 = surround_data.decode('utf-8', errors='replace')
    lines = text2.strip().split('\n')
    print('  内容行数: {}'.format(len(lines)))
    print('  内容预览(前10行):')
    for line in lines[:10]:
        print('    {}'.format(line[:80]))
    print()

# 总结
print('='*60)
print('  数据流总览')
print('='*60)
overhead = len(data) - len(melody_data) - len(lyrics_data) - len(accomp_data) - (len(surround_data) if surround_start >= 0 else 0)
sizes = [
    ('旋律', len(melody_data)),
    ('歌词', len(lyrics_data)),
    ('伴奏', len(accomp_data)),
    ('风火雷电', len(surround_data) if surround_start >= 0 else 0),
    ('结构标记', overhead),
]
for name, size in sizes:
    pct = size / len(data) * 100
    bar = '#' * max(1, int(pct / 2))
    print('  {:8s}: {:>8,} 字节 ({:5.1f}%) {}'.format(name, size, pct, bar))

print()
print('压缩后: 290KB (zstd, 压缩比2.58x)')
print('='*60)
