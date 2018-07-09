#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 7th 00:49:17 2018
    @file  : vim_startuptime.py
    @author: Suzuki
    @brief : vim startup time analyzer.
"""
from modules.vim_performance import VimPerformance
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


if __name__ == '__main__':
    obj = VimPerformance(vim='nvim')
    # obj.measure(100)
    # obj.aggregate()
    # obj.pie()
    obj.plot(kind='hist')
    # obj.hist()
