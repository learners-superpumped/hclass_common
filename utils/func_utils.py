import time
import logging
import asyncio

logger = logging.getLogger(__name__)


def retries(times: int, sleep_time: float = 4, use_compounds: bool = False):
    def func_wrapper(f):
        def wrapper(*args, **kwargs):        
            error_message = ""
            last_error = None
            for current_time in range(kwargs.get('retry_times', times)):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    logger.error(f"{current_time} try failed")
                    last_error = e
                    error_message += str(e)
                    if use_compounds:
                        total_sleep_time = (current_time + 1) * sleep_time
                    else:
                        total_sleep_time = sleep_time
                    time.sleep(total_sleep_time)
                    pass
            raise last_error
        return wrapper
    return func_wrapper