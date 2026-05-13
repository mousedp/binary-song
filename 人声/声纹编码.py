# -*- coding: utf-8 -*-
"""
人声维度 - 哈希声纹二进制编码
==============================
人声本质 = 哈希声纹
有名的人有声纹库（明星/名人）
用SHA-256哈希模拟声纹特征
"""

import hashlib
import struct


class 声纹编码器:
    """人声声纹哈希编码器"""
    
    @staticmethod
    def extract_voiceprint(audio_sample: bytes) -> bytes:
        """
        从音频样本提取声纹哈希
        
        参数：
            audio_sample: 音频原始字节
        
        返回：
            SHA-256 声纹哈希（32字节）
        """
        return hashlib.sha256(audio_sample).digest()
    
    @staticmethod
    def encode_singer(歌手名: str, 特征数据: bytes = b'') -> bytes:
        """
        编码歌手声纹为二进制
        
        参数：
            歌手名: 歌手名称（用于生成基础声纹）
            特征数据: 额外音色特征
        
        返回：
            完整声纹二进制包
        """
        # 歌手名 → 基础哈希
        base_hash = hashlib.sha256(歌手名.encode('utf-8')).digest()
        
        # 混合特征数据
        if 特征数据:
            combined = bytes(a ^ b for a, b in zip(base_hash, 特征数据 * (len(base_hash) // len(特征数据) + 1)))
            final_hash = hashlib.sha256(combined).digest()
        else:
            final_hash = base_hash
        
        # 封装：[长度(4B)] + [歌手名UTF-8] + [声纹哈希(32B)] + [校验(4B)]
        name_bytes = 歌手名.encode('utf-8')
        checksum = sum(final_hash) & 0xFFFFFFFF
        
        result = struct.pack('>I', len(name_bytes))
        result += name_bytes
        result += final_hash
        result += struct.pack('>I', checksum)
        
        return result
    
    @staticmethod
    def decode(binary_data: bytes) -> dict:
        """从二进制解码声纹信息"""
        name_len = struct.unpack('>I', binary_data[:4])[0]
        name = binary_data[4:4+name_len].decode('utf-8')
        voiceprint = binary_data[4+name_len:4+name_len+32]
        checksum = struct.unpack('>I', binary_data[4+name_len+32:4+name_len+36])[0]
        
        return {
            '歌手': name,
            '声纹': voiceprint.hex(),
            '校验': hex(checksum),
        }


# ====== 明星声纹库 ======

# 预定义一些著名歌手的声纹（基于名字的确定性哈希）
声纹库 = {
    '王菲': 声纹编码器.encode_singer('王菲'),
    '李宗盛': 声纹编码器.encode_singer('李宗盛'),
    '那英': 声纹编码器.encode_singer('那英'),
    '张学友': 声纹编码器.encode_singer('张学友'),
}


if __name__ == '__main__':
    print("=== 人声维度 ===")
    
    # 编码王菲声纹
    wp_binary = 声纹库['王菲']
    print(f"王菲声纹二进制长度: {len(wp_binary)} 字节")
    
    # 解码验证
    info = 声纹解码器.decode(wp_binary) if False else None
    
    # 直接解码
    decoded = 声纹编码器.decode(wp_binary)
    print(f"解码结果: {decoded}")
    
    print(f"\n声纹库共 {len(声纹库)} 位歌手")
    for singer in 声纹库:
        print(f"  - {singer}: {len(声纹库[singer])} 字节")
    
    print("\n✅ 人声声纹编码器就绪！")
