from typing import Optional
from pydantic import BaseModel, Field


# 定义请求体模型
class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, description="要翻译的文本，长度在1到100之间")
    source_lang: str = Field(..., pattern="^(zh|en|fr)$", description="源语言，只能是 'zh', 'en', 或 'fr'")
    target_lang: str = Field(..., pattern="^(zh|en|fr)$", description="目标语言，只能是 'zh', 'en', 或 'fr'")

  
    
