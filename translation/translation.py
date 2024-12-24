import re
import time
from enum import Enum
from typing import Callable
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from pydantic import BaseModel

from common.base.meta_singeton import MetaSingleton
from common.env import env
from common.logger import logger
from common.thread import pool
from protocal.request import TranslationRequest

# 每句分片最大字符数
MAX_CHARS_PER_PIECE = 100

def remote_whitespace_char(text: str):
    """移除空格符号"""
    return re.sub(r"\s+", "", text)


class ModelConfig(BaseModel):
    # 模型path/id
    model_path: str
    # 模型预加载推理文本
    preload_infer_text: str
    # 句子切分正则
    split_pattern: str
    # 后处理函数
    post_process_func: Callable = None


class ModelEnum(Enum):
    ZH2EN = ModelConfig(model_path="damo/nlp_csanmt_translation_zh2en", preload_infer_text="你好",
                        split_pattern=r"[。！？；]")
    EN2ZH = ModelConfig(model_path="damo/nlp_csanmt_translation_en2zh", preload_infer_text="hello",
                        split_pattern=r"[.!?;,]", post_process_func=remote_whitespace_char)


class Instance(metaclass=MetaSingleton):
    models = {}
    device = 'cude'
    
    def __init__(self):
        self.device = self.get_device()
        print(f"model device: {self.device}")
        for iterm in ModelEnum:
            self.models[iterm] = pipeline(task=Tasks.translation, model=iterm.value.model_path, device=self.device)
        print("INIT DONE")
    
    def get_device(self) -> str:
        device = 'gpu'
        if env.IS_LINUX:
            device = "cuda"
        return device
    
    async def preload(self):
        future_list = []
        for key, model in self.models.items():
            future = pool.ThreadedEventLoop().submit(self.simple_infer, model, key.value.preload_infer_text)
            future_list.append((key.value.model_path, future))
        for model_name, future in future_list:
            result = future.result()
            print(f"preload: {model_name}, infer: {result}")
    
    async def simple_infer(self, model, text) -> any:
        return model(text)
    
    async def infer(self, request: TranslationRequest) -> str:
        model_name = f"{request.source_lang}2{request.target_lang}".upper()
        if model_name not in ModelEnum.__members__:
            raise ValueError("不支持的语言翻译")
        model_id = ModelEnum[model_name]
        split_pattern = model_id.value.split_pattern
        text_list = self.proprecess_text(request.text, split_pattern)
        start_time = time.time()
        translation_result = ""
        for text in text_list:
            output = self.models[model_id](text)
            translation_result += output['translation']
            
        if model_id.value.post_process_func:
            translation_result = model_id.value.post_process_func(translation_result)
        cost_time = time.time() - start_time
        logger.getlogger().debug(f"{request.text}:翻译结果：{translation_result}, cost_time: {cost_time}")
        return translation_result
    
    def proprecess_text(self, text, split_pattern):
        """
            切分长文本text，按照一句超过20字切分，同时结合短句符号。
            如果短句仍然超过20字，则进一步切分。
            :param text: 输入的文本
            :return: 切分后的短句列表
        """
        # 初步按照短句符号切分
        sentences = re.split(split_pattern, text)
        
        # 移除空白和多余的空格
        sentences = self.splite(text, split_pattern)
        
        # 对每个句子进一步切分，确保不超过MAX_CHARS_PER_PIECE个字
        result = []
        for sentence in sentences:
            # 如果句子长度超过MAX_CHARS_PER_PIECE，按每MAX_CHARS_PER_PIECE字切分
            while len(sentence) > MAX_CHARS_PER_PIECE:
                result.append(sentence[:MAX_CHARS_PER_PIECE])
                sentence = sentence[MAX_CHARS_PER_PIECE:]
            if sentence:
                result.append(sentence)
        
        return result
    
    def splite(self, text, pattern) -> list[str]:
        matches = list(re.finditer(pattern, text))
        # 切分文本：用标点符号的位置来切分
        sentences = []
        start = 0  # 初始位置
        
        for match in matches:
            end = match.end()  # 获取标点符号的结束位置
            sentence = text[start:end]  # 从 start 到 end 获取句子
            sentences.append(sentence.strip())  # 添加到句子列表，并去除多余空白
            start = end  # 更新下一个句子的起始位置
        
        # 如果最后有剩余的部分没有被标点符号切割到，也要加进去
        if start < len(text):
            sentences.append(text[start:].strip())
        
        return sentences
