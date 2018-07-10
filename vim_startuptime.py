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


## ToDo:
# - debug (see issue)
# - prettytable -> status table


if __name__ == '__main__':
    """ VimPerformance's param: vim='vim'(default) or if $EDITOR (environment variable) exists, use it.
    """
    obj = VimPerformance(vim='nvim')
    obj.clean()
    obj.measure(100)
    obj.status()
    """ plot's param: kind='pie'(default) or 'hist' or 'line'
    """
    obj.plot(kind='hist')
