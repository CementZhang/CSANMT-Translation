import json
import os
import socket
from enum import Enum

HEADER_TYPE = 'play-type'
HEADER_TYPE_LOCAL = 'local'
HEADER_ARS_RRCIEVE_TIME = 'asr-recieve-time'

# wave 头的长度
WAVE_HEADER_BYTES_LEN = 42


class AsrStatue(Enum):
    """asr 识别结果状态"""
    success = 0  # 识别完成
    error = 1  # 识别错误
    upload_complate = 2  # 上传完成
    recording = -1  # 录制中


def get_host_name():
    # 获取当前容器ID
    return os.getenv('HOSTNAME', socket.gethostname())


# 无效声音
ALL_EQUAL_INVALID_WORD_SET = {
    '嗯', '嗯嗯', '恩', '一有', '对个', '哎', '有', '对', '啊', '好'
}

# 无效音频时长
CONTAIN_EQUEL_INVALIAD_AUDIO_DURATION = 0.5
# 无效音频单词集合
CONTAIN_EQUEL_INVALID_WORD_SET = {
    "a" : 0.2,
    "yy": 0.2,
    "dd": 0.2,
    "dy": 0.2
}

# 默认贞率
DEFAULT_AUDIO_FS = 16000

AUDIO_FS = 8000


def check_valiad_asr_word(asr_word: str) -> bool:
    """
    检测用户输出语音是否有效
    
    :param asr_word: 识别的用户问题
    :param audio_duration: 音频时长
    """
    if not asr_word:
        return False
    
    # 如果完全匹配 ALL_EQUAL_INVALIAD_WORD_SET 的某个词，返回 False
    if asr_word in ALL_EQUAL_INVALID_WORD_SET:
        return False
    
    for item, rate in CONTAIN_EQUEL_INVALID_WORD_SET.items():
        if check_invalid_ratio(asr_word, item, rate):
            return False
    
    # 通过所有条件则返回 True
    return True


def check_invalid_ratio(check_text: str, invalid_word: str, threshold: float = 0.5) -> bool:
    """
    计算无效字符或单词在整个语音识别结果中的占比，判断是否为无效输入。

    :param asr_result: 语音识别的字符串结果
    :param invalid_word: 无效字符或无效单词
    :param threshold: 占比阈值，默认0.5即50%
    :return: 如果占比大于阈值返回True，否则返回False
    """
    check_text = check_text.strip()  # 去除首尾空格
    total_len = len(check_text)  # 计算总长度
    
    if total_len == 0:
        return False  # 空字符串不处理
    
    # 计算无效词汇的总长度
    invalid_len = check_text.count(invalid_word) * len(invalid_word)
    
    # 计算无效字符占比
    ratio = invalid_len / total_len
    
    return ratio > threshold


def get_audio_duration(audio: bytes, audio_fs=AUDIO_FS):
    """calc audio len  through audoi—fs"""
    bytes_len = len(audio)
    if not bytes_len:
        return 0
    return bytes_len / (audio_fs * 2)


def json_safe_loads(json_str: str, default=None) -> dict:
    """json str no execept loads"""
    if not json_str:
        return default
    try:
        return json.loads(json_str)
    except Exception as e:
        return default
    
    