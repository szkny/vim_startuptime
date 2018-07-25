#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24th 22:46:56 2018
    @file  : vim_startuptime.py
    @author: suzukisohei
    @brief : vim startup time analyzer.
             [USAGE] python vim_startuptime.py {VIM_ARGS}
"""
from modules.vim_performance import VimPerformance
from sys import argv
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


## ToDo:
# - debug (see issue)


if __name__ == '__main__':
    """ VimPerformance's param: vim='vim'(default) or if $EDITOR (environment variable) exists, use it.
    """
    obj = VimPerformance(vim='nvim')
    obj.clean()
    obj.measure(10, vim_args=argv[1:])
    """ plot's param: kind='pie'(default) or 'hist' or 'line'
    """
    obj.plot(kind='pie')
