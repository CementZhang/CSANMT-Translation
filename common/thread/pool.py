from common.logger import logger
import asyncio
from concurrent.futures import ThreadPoolExecutor
from threading import local
from typing import Callable
from ..base.meta_singeton import MetaSingleton
# 初始化线程池的工作线程数量
thread_max_work = 5


class ThreadedEventLoop(metaclass=MetaSingleton):
    def __init__(self, max_workers: int = thread_max_work):
        """
        初始化线程池和事件循环
        :param max_workers: 最大线程数
        """
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers, initializer=self._initialize_thread)

        # 使用线程本地存储事件循环
        self._thread_local = local()

    def _initialize_thread(self):
        """
        为线程池中的每个线程初始化事件循环
        """
        if not hasattr(self._thread_local, "loop"):
            self._thread_local.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._thread_local.loop)

    def _get_event_loop(self):
        """
        获取当前线程的事件循环
        """
        if not hasattr(self._thread_local, "loop"):
            raise RuntimeError("Event loop is not initialized for this thread.")
        return self._thread_local.loop

    def submit(self, afunc: Callable, *args):
        """
        提交任务到线程池, 不需要等待; 如果需要结果future=submit,result = future.result()同时future.result()为阻塞执行
        :param afunc: 异步函数
        :param args: 异步函数参数
        :returns Future
        
        """
        return self.executor.submit(self._run_in_thread, afunc, *args)

    def _run_in_thread(self, func: Callable, *args):
        """
        在当前线程的事件循环中运行异步任务
        """
        loop = self._get_event_loop()
        try:
            return loop.run_until_complete(func(*args))
        except Exception as e:
            # 使用自己的日志记录
            logger.log_exception('', e)

    def shutdown(self, wait: bool = True):
        """
        关闭线程池和事件循环
        """
        print("close athread loop")
        self.executor.shutdown(wait=wait)
        if hasattr(self._thread_local, "loop"):
            self._thread_local.loop.close()
