# -*- coding: utf-8 -*-
"""
曲（旋律）维度 - 二进制编码
============================
01234567 = 哆来咪发唆拉西
加间奏留白 + 音调高低
"""

import struct


# 音符映射：数字 → 二进制编码
NOTE_MAP = {
    0: 0b00000000,  # 休止/留白
    1: 0b00000001,  # 哆 (Do)
    2: 0b00000010,  # 来 (Re)
    3: 0b00000011,  # 咪 (Mi)
    4: 0b00000100,  # 发 (Fa)
    5: 0b00000101,  # 唆 (So)
    6: 0b00000110,  # 拉 (La)
    7: 0b00000111,  # 西 (Si)
}

# 八度偏移（高/低音）
OCTAVE_SHIFT = {
    'low': 0b00000000,     # 低音
    'mid': 0b00001000,     # 中音
    'high': 0b00010000,    # 高音
}

# 时值（节拍）
DURATION = {
    'whole': 4.0,      # 全音符
    'half': 2.0,       # 二分音符
    'quarter': 1.0,    # 四分音符
    'eighth': 0.5,     # 八分音符
    'sixteenth': 0.25, # 十六分音符
}


class 旋律编码器:
    """旋律二进制编码器"""
    
    @staticmethod
    def encode_note(note: int, octave: str = 'mid', duration: str = 'quarter') -> bytes:
        """
        编码单个音符为二进制
        
        参数：
            note: 音符编号(0-7)
            octave: 八度(low/mid/high)
            duration: 时值
        """
        value = NOTE_MAP.get(note, 0) | OCTAVE_SHIFT.get(octave, 0)
        dur = DURATION.get(duration, 1.0)
        # 用2字节精确编码，避免对齐padding：高5位=音符(0-7)+八度(0-2), 低字节=时值(1/2/4/8分音符)
        dur_map = {4.0: 0, 2.0: 1, 1.0: 2, 0.5: 3, 0.25: 4}
        dur_code = dur_map.get(dur, 2)
        return struct.pack('BB', value, dur_code)
    
    @staticmethod
    def encode_melody(notes: list) -> bytes:
        """
        编码一段旋律为二进制
        
        参数：
            notes: [(note, octave, duration), ...]
        
        返回：
            二进制字节流
        """
        result = b''
        for n in notes:
            result += 旋律编码器.encode_note(*n)
        return result
    
    @staticmethod
    def decode(binary_data: bytes) -> list:
        """从二进制解码旋律"""
        dur_decode = {0: 4.0, 1: 2.0, 2: 1.0, 3: 0.5, 4: 0.25}
        notes = []
        for i in range(0, len(binary_data), 2):  # 2 bytes per note
            chunk = binary_data[i:i+2]
            if len(chunk) < 2:
                break
            value, dur_code = struct.unpack('BB', chunk)
            note = value & 0b00000111
            octave_raw = (value & 0b00011000) >> 3
            octave_map = {0: 'low', 1: 'mid', 2: 'high'}
            notes.append({
                'note': note,
                'octave': octave_map.get(octave_raw, 'mid'),
                'duration': dur_decode.get(dur_code, 1.0),
            })
        return notes


# ====== 测试歌曲：传奇（王菲）主歌片段 ======
# 只是因为在人群中多看了你一眼
# 旋律简化版（C大调）

传奇主歌片段 = [
    (1, 'mid', 'eighth'),   # 哆
    (1, 'mid', 'eighth'),   # 哆
    (3, 'mid', 'quarter'),  # 咪
    (5, 'mid', 'eighth'),   # 唆
    (3, 'mid', 'eighth'),   # 咪
    (1, 'mid', 'half'),     # 哆（长音）
    (6, 'low', 'quarter'),  # 拉（低音）
    (5, 'mid', 'eighth'),   # 唆
    (3, 'mid', 'quarter'),  # 咪
    (2, 'mid', 'half'),     # 来（长音）
]


if __name__ == '__main__':
    print("=== 曲（旋律）维度 ===")
    
    # 编码传奇片段
    binary = 旋律编码器.encode_melody(传奇主歌片段)
    print(f"传奇主歌片段二进制长度: {len(binary)} 字节")
    
    # 解码验证
    decoded = 旋律编码器.decode(binary)
    print(f"解码后音符数: {len(decoded)}")
    for i, n in enumerate(decoded[:5]):
        print(f"  [{i}] 音符={n['note']} 八度={n['octave']} 时值={n['duration']}")
    
    print("\n✅ 旋律编码器就绪！")
