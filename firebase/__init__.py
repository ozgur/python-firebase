import atexit

from .async import process_pool
from firebase import *

__version__ = '1.1'
VERSION = tuple(map(int, __version__.split('.')))

@atexit.register
def close_process_pool():
    """
    Clean up function that closes and terminates the process pool
    defined in the ``async`` file.
    """
    process_pool.close()
    process_pool.join()
    process_pool.terminate()
