# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from threading import Thread


class AsyncLoader(Thread):
    def __init__(self, func, callback, *args, **kwargs):
        super(AsyncLoader, self).__init__(*args, **kwargs)
        self.daemon = True
        self.quit = False
        self.func = func
        self.func_args = kwargs.pop('args')
        self.callback = callback

    def run(self):
        data = self.func(*self.func_args)
        self.callback(data=data)
