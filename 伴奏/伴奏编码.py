# -*- coding: utf-8 -*-
"""
伴奏维度 - MIDI事件编码（非PCM波形）
=====================================
之前用44100Hz PCM波形，7个和弦就705KB，太蠢了。
正确做法：存MIDI事件（音高+时长+力度），播放时再合成波形。
一个和弦事件 = 1字节乐器 + 1字节音高 + 2字节时长(ms) + 1字节力度 = 5字节
"""

import struct


class 乐器类型:
    """乐器枚举（精简版：只留最经典的）"""
    唢呐 = 0x01    # 必选：中国民乐灵魂
    鼓   = 0x02    # 次选：节奏骨架
    笛子 = 0x03
    古筝 = 0x04
    钢琴 = 0x05


# 音高编号（MIDI标准，C4=60）
PITCH_MAP = {
    'C3': 48, 'D3': 50, 'E3': 52, 'F3': 53, 'G3': 55, 'A3': 57, 'B3': 59,
    'C4': 60, 'D4': 62, 'E4': 64, 'F4': 65, 'G4': 67, 'A4': 69, 'B4': 71,
    'C5': 72, 'D5': 74, 'E5': 76, 'F5': 77, 'G5': 79, 'A5': 81, 'B5': 83,
    'C6': 84,
}


class 伴奏编码器:
    """伴奏二进制编码器（MIDI事件模式）"""

    @staticmethod
    def encode_event(乐器: int, 音高: int, 时长ms: int, 力度: int = 80) -> bytes:
        """
        编码单个伴奏事件
        
        格式：[乐器ID(1B)] + [音高(1B)] + [时长ms(2B)] + [力度(1B)] = 5字节
        
        参数：
            乐器: 乐器ID
            音高: MIDI音高编号(0-127)
            时长ms: 持续时间(毫秒)
            力度: 力度(0-127)
        """
        return struct.pack('BBHb', 乐器, 音高, 时长ms, 力度)

    @staticmethod
    def encode_accompaniment(events: list) -> bytes:
        """
        编码完整伴奏（事件流）
        
        参数：
            events: [(乐器, 音高, 时长ms, 力度), ...]
        
        返回：
            伴奏二进制包
        """
        header = struct.pack('>H', len(events))  # 事件数
        body = b''
        for 乐器, 音高, 时长, 力度 in events:
            body += 伴奏编码器.encode_event(乐器, 音高, 时长, 力度)
        return header + body

    @staticmethod
    def decode(data: bytes) -> list:
        """从二进制解码伴奏事件"""
        count = struct.unpack('>H', data[:2])[0]
        events = []
        for i in range(count):
            offset = 2 + i * 5
            if offset + 5 > len(data):
                break
            乐器, 音高, 时长, 力度 = struct.unpack('BBHb', data[offset:offset+5])
            events.append({
                'instrument': 乐器,
                'pitch': 音高,
                'duration_ms': 时长,
                'velocity': 力度,
            })
        return events


def 生成传奇伴奏() -> bytes:
    """生成传奇伴奏：钢琴+唢呐（2种乐器）"""
    chords = [
        # 钢琴铺底
        (乐器类型.钢琴, 'C4', 2000, 65),
        (乐器类型.钢琴, 'A4', 2000, 60),
        (乐器类型.钢琴, 'F4', 2000, 65),
        (乐器类型.钢琴, 'G4', 2000, 60),
        # 唢呐主旋律点缀
        (乐器类型.唢呐, 'E5', 800, 90),
        (乐器类型.唢呐, 'G5', 400, 85),
        (乐器类型.唢呐, 'A5', 1200, 95),
    ]
    events = []
    for 乐器, 音名, 时长, 力度 in chords:
        音高 = PITCH_MAP.get(音名, 60)
        events.append((乐器, 音高, 时长, 力度))
    return 伴奏编码器.encode_accompaniment(events)


def 生成闹海伴奏() -> bytes:
    """生成闹海伴奏：唢呐+鼓（2种乐器）"""
    chords = [
        # 唢呐破空开场
        (乐器类型.唢呐, 'C5', 600, 95),
        (乐器类型.唢呐, 'E5', 400, 90),
        (乐器类型.唢呐, 'G5', 800, 100),
        (乐器类型.唢呐, 'A5', 200, 85),
        (乐器类型.唢呐, 'G5', 600, 90),
        # 鼓点节奏
        (乐器类型.鼓, 'C3', 500, 100),
        (乐器类型.鼓, 'C3', 500, 80),
    ]
    events = []
    for 乐器, 音名, 时长, 力度 in chords:
        音高 = PITCH_MAP.get(音名, 60)
        events.append((乐器, 音高, 时长, 力度))
    return 伴奏编码器.encode_accompaniment(events)


if __name__ == '__main__':
    print("=== 伴奏维度（MIDI事件模式）===")
    binary = 生成传奇伴奏()
    print("传奇伴奏二进制长度: {} 字节".format(len(binary)))
    events = 伴奏编码器.decode(binary)
    print("事件数: {}".format(len(events)))
    for i, e in enumerate(events):
        print("  [{}] 乐器={} 音高={} 时长={}ms 力度={}".format(
            i, e['instrument'], e['pitch'], e['duration_ms'], e['velocity']))
