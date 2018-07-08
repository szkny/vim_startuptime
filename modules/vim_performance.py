#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 8th 09:52:54 2018
    @file  : vim_performance.py
    @author: Suzuki
    @brief : vim startup time analyzer.
"""
import os
import re
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
from modules.keyevent import KeyEvent
# from multiprocessing import Process, Lock


class VimPerformance():
    """ measure vim performance """

    def __init__(self, vim=None):
        if vim is None:
            for k, v in os.environ.items():
                if k == 'EDITOR':
                    vim = v
            if vim is None:
                vim = 'vim'
        self.vim = vim
        self.outputs = []
        self.__canvas_set()
        self.process_time = {}
        self.df = None
        self.df_ave = None
        self.ls = []

    def measure(self, nloop=1, output_dir='./results'):
        print('measuring %s start-up time..' % self.vim)
        for i in range(nloop):
            self.__measure()

    def __measure(self, output_dir='./results'):
        """
        measure startup time of vim.
        and create profile.txt into "output_dir"
        """
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        if output_dir[-1] == '/':
            output = output_dir + 'profile1.txt'
        else:
            output = output_dir + '/profile1.txt'
        while os.path.exists(output):
            if output[-4:] == '.txt':
                filenum = 0
                operator = 0
                while 1:
                    try:
                        filenum = int(output[-5 - operator:-4])
                    except ValueError:
                        operator -= 1
                        break
                    operator += 1
                filenum += 1
                output = output[:-5 - operator] + '%d.txt' % filenum
        command = self.vim + ' --startuptime %s -c "q"' % output
        os.system(command)
        self.outputs += [output]

    def aggregate(self, outputs=None, status=False):
        """
        aggregate start-up time from profile.txt
        """
        print('aggregating %s start-up time..' % self.vim)
        if outputs is None:
            self.outputs = glob('./results/*.txt')
            if self.outputs == []:
                print('[warning] output file is not found.'
                      ' you shold run VimPerformance.measure() at first.')
                return
        elif type(outputs) is not list:
            self.outputs = [outputs]
        self.process_time = {}
        for _file in self.outputs:
            process_count = {}
            if os.path.exists(_file):
                with open(_file, encoding='utf-8') as f:
                    ### load file 'profile*.txt ###
                    for line in f.readlines():
                        readtime = re.findall('[0-9.e]{7}', line)
                        length = len(readtime)
                        if length >= 2:
                            process_name = ' '.join(line.split()[length:])
                            if line.split()[length] == 'sourcing':
                                process_name = 'sourcing ' + os.path.basename(process_name)
                            ### count same process ###
                            if process_name in process_count.keys():
                                process_count[process_name] += 1
                            else:
                                process_count.update({process_name: 1})
                            ### aggregate process time ###
                            if process_name in self.process_time.keys():
                                if process_count[process_name] == 1:
                                    self.process_time[process_name] += [float(readtime[1])]
                                elif process_count[process_name] >= 2:
                                    self.process_time[process_name][-1] += float(readtime[1])
                            else:
                                self.process_time.update({process_name: [float(readtime[1])]})
                            cumulative_time = float(readtime[0])
                    ### append to list of total start-up time ###
                    if 'total time' in self.process_time.keys():
                        self.process_time['total time'] += [cumulative_time]
                    else:
                        self.process_time.update({'total time': [cumulative_time]})
            else:
                print('[warning] file not found: ' + _file)
        ### convert to pandas DataFrame & sort ###
        self.df = pd.DataFrame()
        for column in self.process_time.keys():
            self.df[column] = self.process_time[column]
        self.df_ave = self.df.mean().sort_values(ascending=False)
        self.ls = list(self.df.keys())
        if status is True:
            self.status()

    def status(self):
        if len(self.ls) == 0:
            print('[warning] process is empty.'
                  ' you shold run VimPerformance.aggregate().')
            return
        print('{EDITOR} start-up time ({FILE_NUMBER} loops) :'
              ' {AVE:.3f} +/- {STD:.3f} [msec]'.format(
                  EDITOR=self.vim,
                  FILE_NUMBER=len(self.outputs),
                  AVE=self.df['total time'].mean(),
                  STD=self.df['total time'].std())
              )
        print('\t--- PROCESS ---')
        for k in self.df_ave.keys():
            if k == 'total time':
                continue
            print('\t{KEY:<35s}\t{VALUE:7.3f} +/- {STD:<7.3f}'.format(
                KEY=k,
                VALUE=self.df_ave[k],
                STD=self.df[k].std()))

    def list(self):
        self.ls = list(self.df.keys())
        return self.ls

    def hist(self, column='total time'):
        if column in self.ls:
            self.df[column].hist(bins=100, alpha=0.5, normed=True)
            self.df[column].plot(kind='kde', style='r--')
            KeyEvent()
            plt.title('%s start-up time (total: %7.1f msec)' % (self.vim, self.df['total time'].mean()))
            plt.xlabel('msec')
            plt.show()
        else:
            print('[warning] no such column: ' + column)

    def plot(self, kind=None, **kwargs):
        if kind == 'pie':
            self.pie(**kwargs)
        elif kind == 'hist':
            self.hist(**kwargs)
        else:
            if len(self.ls) == 0:
                print('[warning] process is empty.'
                      ' you shold run VimPerformance.aggregate().')
                return
            for column in self.ls:
                self.df[column].plot(label=column)
            KeyEvent()
            plt.title('%s start-up time (total: %7.1f msec)' % (self.vim, self.df['total time'].mean()))
            plt.xlabel('No.')
            plt.ylabel('msec')
            plt.legend(bbox_to_anchor=(1.00, 0.9, 0.5, .100), ncol=3, fontsize=5)
            plt.show()

    def pie(self, number=7):
        if len(self.ls) == 0:
            print('[warning] process is empty.'
                  ' you shold run VimPerformance.aggregate().')
            return
        tmp_df = self.df_ave[1:number]
        tmp_df['others'] = self.df_ave[number + 1:].sum()
        tmp_df.plot(kind='pie',
                    autopct="%1.1f%%",
                    pctdistance=0.7,
                    counterclock=False,
                    startangle=90)
        KeyEvent()
        plt.title('%s start-up time (total: %7.1f msec)' % (self.vim, self.df['total time'].mean()))
        plt.show()

    def __canvas_set(self):
        fig = plt.figure(figsize=(7, 5))
        fig.canvas.set_window_title('vim start-up time')
        fig.patch.set_facecolor("white")
        fig.patch.set_alpha(1)
        sub = fig.add_subplot(111)
        sub.patch.set_facecolor("white")
        sub.patch.set_alpha(1)
        sub.set_axisbelow(True)
        plt.style.use('ggplot')
