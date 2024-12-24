import argparse
import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from controllers.translation_controller import router
from translation import translation
from common.thread import pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 注册路由
    app.include_router(router)
    # 初始化线程池
    thread_pool = pool.ThreadedEventLoop()
    # 初始化翻译器
    translation_obj = translation.Instance()
    await translation_obj.preload()
    yield
    # Clean up the ML models and release the resources
    thread_pool.shutdown()
    pass


app = FastAPI(lifespan=lifespan)

if __name__ == '__main__':
    # 使用命令行参数的处理逻辑
    # 命令行参数解析放在全局作用域
    parser = argparse.ArgumentParser(description="Start FastAPI with SSL.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on.")
    parser.add_argument("--port", type=int, default=11000, help="Port to run the server on.")
    args = parser.parse_args()
    
    
    async def main():
        config = uvicorn.Config(app, host=args.host, port=args.port)
        server = uvicorn.Server(config)
        await server.serve()
    
    
    # 使用 asyncio 运行 main 函数来启动服务
    asyncio.run(main())
