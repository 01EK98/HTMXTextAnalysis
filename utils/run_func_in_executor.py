import asyncio
from typing import Callable
from functools import wraps


def run_in_executor(func: Callable) -> Callable:
    @wraps(func)
    def func_run_in_executor(*args, **kwargs) -> asyncio.Future:
        loop = asyncio.get_running_loop()
        # by default will run up to 10 processes concurrently
        return loop.run_in_executor(None, lambda: func(*args, **kwargs))

    return func_run_in_executor
