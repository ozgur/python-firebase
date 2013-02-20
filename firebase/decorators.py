import requests
from functools import wraps


def http_connection(timeout):
    """
    Decorator function that injects a requests.Session instance into
    the decorated function's actual parameters if not given.
    """
    def wrapper(f):
        def wrapped(*args, **kwargs):
            if 'connection' not in kwargs or not kwargs['connection']:
                kwargs['connection'] = requests.Session(
                    timeout=timeout, headers={'Content-type': 'application/json'})
            return f(*args, **kwargs)
        return wraps(f)(wrapped)
    return wrapper
