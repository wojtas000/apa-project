import time
import logging
import asyncio

from functools import wraps

logger = logging.getLogger(__name__)

def timeit(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        end_time = time.perf_counter()
        logger.debug(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        logger.debug(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper
