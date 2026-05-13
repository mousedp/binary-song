# -*- coding: utf-8 -*-
"""
歌词维度 - 中文字符二进制编码
==============================
标准字符集：Unicode/GBK
歌词也有音调高低需要处理
"""


class 歌词编码器:
    """歌词二进制编码器"""
    
    # 中文音调映射（拼音声调）
    TONE_MAP = {
        'ā': 1, 'á': 2, 'ǎ': 3, 'à': 4,  # a的四声
        'ē': 1, 'é': 2, 'ě': 3, 'è': 4,
        'ī': 1, 'í': 2, 'ǐ': 3, 'ì': 4,
        'ō': 1, 'ó': 2, 'ǒ': 3, 'ò': 4,
        'ū': 1, 'ú': 2, 'ǔ': 3, 'ù': 4,
        'ǖ': 1, 'ǘ': 2, 'ǚ': 3, 'ǜ': 4,
    }
    
    @staticmethod
    def encode(text: str) -> bytes:
        """
        将歌词文本编码为二进制
        
        格式：每个字符 → UTF-8字节 + 声调标记(1字节)
        """
        result = b''
        for char in text:
            # UTF-8 编码
            utf8_bytes = char.encode('utf-8')
            
            # 声调检测
            tone = 歌词编码器.TONE_MAP.get(char, 0)
            
            result += utf8_bytes + bytes([tone])
        
        return result
    
    @staticmethod
    def decode(binary_data: bytes) -> str:
        """从二进制解码歌词文本"""
        text = ''
        i = 0
        while i < len(binary_data):
            try:
                # 找UTF-8字符边界
                if binary_data[i] < 0x80:
                    # ASCII
                    char = chr(binary_data[i])
                    i += 1
                elif (binary_data[i] & 0xE0) == 0xC0:
                    char = bytes(binary_data[i:i+2]).decode('utf-8')
                    i += 2
                elif (binary_data[i] & 0xF0) == 0xE0:
                    char = bytes(binary_data[i:i+3]).decode('utf-8')
                    i += 3
                else:
                    char = bytes(binary_data[i:i+4]).decode('utf-8')
                    i += 4
                
                # 跳过声调字节
                i += 1
                text += char
            except Exception:
                break
        return text


# ====== 测试歌曲：传奇（王菲）歌词 ======

传奇歌词 = """只是因为在人群中多看了你一眼
再也没能忘掉你容颜
梦想着偶然能有一天相见
从此我开始孤单思念

想你时你在天边
想你时你在眼前
想你时你在脑海
想你时你在心田

宁愿相信我们前世有约
今生的爱情故事不会再改变
宁愿用这一生等你发现
我一直在你身旁从未走远"""


if __name__ == '__main__':
    print("=== 歌词维度 ===")
    
    # 编码
    binary = 歌词编码器.encode(传奇歌词)
    print(f"传奇歌词二进制长度: {len(binary)} 字节")
    
    # 解码验证
    decoded = 歌词编码器.decode(binary)
    print(f"解码后文字长度: {len(decoded)} 字符")
    print(f"前20字: {decoded[:20]}...")
    
    print("\n✅ 歌词编码器就绪！")
