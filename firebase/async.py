from multiprocessing.pool import Pool

import traceback

from lazy import LazyLoadProxy


class ExceptionAwareCallable(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        try:
            return self.func(*args, **kwargs)
        except:
            multiprocessing.get_logger().error(traceback.format_exc())
            raise


class ExceptionAwarePool(Pool):
    def apply_async(self, func, args=(), kwds={}, callback=None):
        return super(ExceptionAwarePool, self).apply_async(
            ExceptionAwareCallable(func), args, kwds, callback)


_process_pool = None

def get_process_pool(size=5):
    global _process_pool
    if _process_pool is None:
        _process_pool = ExceptionAwarePool(processes=size)
    return _process_pool

process_pool = LazyLoadProxy(get_process_pool)
