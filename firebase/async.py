import threading
from .lazy import LazyLoadProxy

__all__ = ['process_pool']

_process_pool = None
_singleton_lock = threading.Lock()


def get_process_pool(size=5):
    global _process_pool
    global _singleton_lock

    if _process_pool is not None:
        return _process_pool

    # initialize process_pool thread safe way
    with _singleton_lock:
        if _process_pool is None:
            import atexit
            import multiprocessing
            _process_pool = multiprocessing.Pool(processes=size)

            # atexit will work only if multiprocessing pool is initialized.
            @atexit.register
            def close_process_pool():
                """
                Clean up function that closes and terminates the process pool
                """
                _process_pool.close()
                _process_pool.join()
                _process_pool.terminate()

    return _process_pool


process_pool = LazyLoadProxy(get_process_pool)