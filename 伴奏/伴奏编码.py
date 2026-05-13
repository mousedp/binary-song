# -*- coding: utf-8 -*-
"""
伴奏维度 - 乐器音频二进制编码
================================
伴奏库：笛子、古筝、钢琴等
有名歌曲才有完整伴奏库
"""

import struct


class 乐器类型:
    """乐器枚举"""
    笛子 = 0x01
    古筝 = 0x02
    钢琴 = 0x03
    小提琴 = 0x04
    吉他 = 0x05
    二胡 = 0x06
    琵琶 = 0x07
    架子鼓 = 0x08
    贝斯 = 0x09
    合成器 = 0x0A


class 伴奏编码器:
    """伴奏二进制编码器"""
    
    @staticmethod
    def encode_instrument(乐器: int, 音频数据: bytes) -> bytes:
        """
        编码单个乐器轨道
        
        格式：[乐器ID(1B)] + [长度(4B)] + [音频数据]
        """
        return struct.pack('>BI', 乐器, len(音频数据)) + 音频数据
    
    @staticmethod
    def encode_accompaniment(tracks: list) -> bytes:
        """
        编码完整伴奏（多轨合成）
        
        参数：
            tracks: [(乐器ID, 音频数据), ...]
        
        返回：
            完整伴奏二进制包
        """
        header = struct.pack('>H', len(tracks))  # 轨道数
        body = b''
        for 乐器, 数据 in tracks:
            body += 伴奏编码器.encode_instrument(乐器, 数据)
        return header + body
    
    @staticmethod
    def generate_sine_wave(freq: float, duration: float,
                           sample_rate: int = 44100,
                           amplitude: float = 0.5) -> bytes:
        """
        生成正弦波音频数据（模拟乐器音色）
        
        用于测试/演示，实际使用时替换为真实音频文件
        
        参数：
            freq: 频率(Hz)
            duration: 时长(秒)
            sample_rate: 采样率
            amplitude: 振幅(0-1)
        """
        import math
        num_samples = int(sample_rate * duration)
        data = b''
        for i in range(num_samples):
            t = i / sample_rate
            value = amplitude * math.sin(2 * math.pi * freq * t)
            # 转为16位PCM
            sample = int(value * 32767)
            data += struct.pack('<h', sample)
        return data


# ====== 测试歌曲：传奇（王菲）伴奏 ======
# 简化版：钢琴+弦乐

def 生成传奇伴奏() -> bytes:
    """生成传奇的简化伴奏（用于测试）"""
    
    # C大调音符频率 (Hz)
    NOTES = {
        'C4': 261.63, 'D4': 293.66, 'E4': 329.63,
        'F4': 349.23, 'G4': 392.00, 'A4': 440.00,
        'B4': 493.88, 'C5': 523.25,
    }
    
    # 主歌和弦进行（传奇片段）
    chords = [
        ('C4', 1.0),
        ('G4', 0.5),
        ('A4', 0.5),
        ('E4', 2.0),
        ('F4', 1.0),
        ('C4', 1.0),
        ('D4', 2.0),
    ]
    
    tracks = []
    for freq_name, dur in chords:
        freq = NOTES.get(freq_name, 440.0)
        audio = 伴奏编码器.generate_sine_wave(
            freq=freq,
            duration=dur,
            amplitude=0.3
        )
        tracks.append((乐器类型.钢琴, audio))
    
    return 伴奏编码器.encode_accompaniment(tracks)


if __name__ == '__main__':
    print("=== 伴奏维度 ===")
    
    # 生成传奇伴奏
    binary = 生成传奇伴奏()
    print(f"传奇伴奏二进制长度: {len(binary)} 字节")
    
    print(f"\n支持的乐器:")
    for name in dir(乐器类型):
        if not name.startswith('_'):
            val = getattr(乐器类型, name)
            if isinstance(val, int):
                print(f"  {name}: 0x{val:02X}")
    
    print("\n✅ 伴奏编码器就绪！")
