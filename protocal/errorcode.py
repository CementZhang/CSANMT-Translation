import enum


class Error(enum.Enum):
    """name，  value(错误码，错误内容)"""
    ASR_RECOG = 1000, "识别失败"
