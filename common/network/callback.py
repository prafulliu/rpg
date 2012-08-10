# -*- coding: utf-8 -*-
class Callback():
    def __init__(self):
        self._callback = {}

    def hook_command(self, cmd, cb_f):
        self._callback[cmd] = cb_f

    def get_callback(self, cmd):
        return self._callback[cmd]
