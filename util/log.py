#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from enum import IntEnum

class Log:
    class Level(IntEnum):
        ERROR = 1
        WARN = 2
        INFO = 3
        TRACE = 4

    LOG_LEVEL = Level.WARN

    @staticmethod
    def set_level(level):
        if level >= Log.LOG_LEVEL:
            Log.LOG_LEVEL = level

    @staticmethod
    def log(level, *args, **kwargs):
        if level <= Log.LOG_LEVEL:
            print(*args, file=sys.stderr, **kwargs)

        if level <= Log.Level.ERROR:
            sys.exit(1)

    @staticmethod
    def error(*args, **kwargs):
        Log.log(Log.Level.ERROR, *args, **kwargs)

    @staticmethod
    def warn(*args, **kwargs):
        Log.log(Log.Level.WARN, *args, **kwargs)

    @staticmethod
    def info(*args, **kwargs):
        Log.log(Log.Level.INFO, *args, **kwargs)

    @staticmethod
    def trace(*args, **kwargs):
        Log.log(Log.Level.TRACE, *args, **kwargs)
