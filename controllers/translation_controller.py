from fastapi import APIRouter
from common.response.yyn import return_ok
from translation import translation
from protocal.request import TranslationRequest
router = APIRouter()


@router.post("/translation")
async def chat(request: TranslationRequest):
    result = await translation.Instance().infer(request)
    return return_ok(result)


