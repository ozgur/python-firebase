# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from threading import Thread


class AsyncLoader(Thread):
    def __init__(self, func, func_args, callback, *args, **kwargs):
        super(DataAsyncLoader, self).__init__(*args, **kwargs)
        self.daemon = True
        self.quit = False
        self.func = func
        self.func_args = func_args
        self.callback = callback

    def run(self):
        data = func(self.func_args)
        self.callback(data=data)
