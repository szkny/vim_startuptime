#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 8th 09:52:54 2018
    @file  : vim_performance.py
    @author: Suzuki
    @brief : utility class for vim startup time analyzer.
"""
import os
import re
import pandas as pd
from glob import glob
from tqdm import tqdm
from prettytable import PrettyTable


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
        self.vim_args = ''
        self.outputs = []
        self.output_dir = './results'
        self.process_time = {}
        self.df = None
        self.df_ave = None
        self.ls = []

    def parse_vimargs(self, vim_args):
        if vim_args is not None:
            if type(vim_args) is list:
                self.vim_args = ' '.join(vim_args)
            if type(vim_args) is str:
                self.vim_args = vim_args
        return self.vim_args

    def measure(self, nloop=1, output_dir='./results', vim_args=None):
        print('measuring %s start-up time..' % self.vim)
        self.output_dir = output_dir
        self.parse_vimargs(vim_args)
        for i in tqdm(range(nloop)):
            self.__measure()
        self.status()

    def __measure(self):
        """
        measure startup time of vim.
        and create profile.txt into "output_dir"
        """
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        if self.output_dir[-1] != '/':
            output_dir = self.output_dir + '/'
        number = 1
        output = output_dir + 'profile%d.txt' % number
        while os.path.exists(output):
            number += 1
            output = output_dir + 'profile%d.txt' % number
        command = self.vim + \
            ' {VIM_ARGS} --startuptime {OUTPUT} -c "quitall!" >/dev/null' \
            .format(
                VIM_ARGS=self.vim_args,
                OUTPUT=output
            )
        os.system(command)
        self.outputs += [output]

    def aggregate(self, outputs=None, status=True):
        """
        aggregate start-up time from profile.txt
        data store into self.df and self.df_ave
        """
        print('aggregating %s start-up time..' % self.vim)
        if outputs is None:
            self.outputs = glob('./results/*.txt')
            if self.outputs == []:
                print('[warning] output file is not found.'
                      ' you shold run VimPerformance.measure() at first.')
                return
        elif type(outputs) is list:
            self.outputs = outputs
        elif type(outputs) is str:
            self.outputs = [outputs]
        self.process_time = {}
        for _file in self.outputs:
            process_count = {}
            if os.path.exists(_file):
                with open(_file, encoding='utf-8') as f:
                    # load file 'profile*.txt
                    for line in f.readlines():
                        readtime = re.findall('[0-9.e]{7}', line)
                        length = len(readtime)
                        if length >= 2:
                            process_name = ' '.join(line.split()[length:])
                            if line.split()[length] == 'sourcing':
                                process_name = 'sourcing ' + \
                                    os.path.basename(process_name)
                            # count same process
                            if process_name in process_count.keys():
                                process_count[process_name] += 1
                            else:
                                process_count.update({process_name: 1})
                            # aggregate process time
                            if process_name in self.process_time.keys():
                                if process_count[process_name] == 1:
                                    self.process_time[process_name] += [
                                        float(readtime[1])]
                                elif process_count[process_name] >= 2:
                                    self.process_time[process_name][-1] += float(
                                        readtime[1])
                            else:
                                self.process_time.update(
                                    {process_name: [float(readtime[1])]})
                            cumulative_time = float(readtime[0])
                    # append to list of total start-up time
                    if 'total time' in self.process_time.keys():
                        self.process_time['total time'] += [cumulative_time]
                    else:
                        self.process_time.update(
                            {'total time': [cumulative_time]})
            else:
                print('[warning] file not found: ' + _file)
        # convert to pandas DataFrame & sort
        self.df = pd.DataFrame()
        for column in self.process_time.keys():
            self.df[column] = self.process_time[column]
        self.df_ave = self.df.mean().sort_values(ascending=False)
        self.ls = list(self.df.keys())
        if status is True:
            self.status()

    def status(self, table_head=10):
        if len(self.ls) == 0:
            """ case of measuring data empty. """
            self.aggregate(status=False)
            if len(self.ls) == 0:
                return
        print('{EDITOR} start-up time ({FILE_NUMBER} loops) :'
              ' {AVE:.3f} +/- {STD:.3f} [msec]'.format(
                  EDITOR=self.vim,
                  FILE_NUMBER=len(self.outputs),
                  AVE=self.df['total time'].mean(),
                  STD=self.df['total time'].std())
              )
        if self.vim_args != '':
            print('(%s args : %s)' % (self.vim, self.vim_args))
        table = PrettyTable(['PROCESS', 'TIME'])
        counter = 0
        for process_name in self.df_ave.keys():
            if process_name == 'total time':
                continue
            value = '%7.3f +/- %.3f' \
                    % (self.df_ave[process_name], self.df[process_name].std())
            table.add_row([process_name, value])
            counter += 1
            if counter == table_head:
                break
        table.add_row(['...', '...'])
        print(table)

    def list(self):
        self.ls = list(self.df.keys())
        return self.ls

    def clean(self):
        if self.output_dir[-1] == '/':
            expression = self.output_dir + 'profile*.txt'
        else:
            expression = self.output_dir + '/profile*.txt'
        file_list = glob(expression)
        if len(file_list) > 0:
            print('cleaning caches in "%s" ..' % self.output_dir)
            os.system('rm ' + expression)


if __name__ == '__main__':
    obj = VimPerformance()
    obj.measure(nloop=10, output_dir='../results')
    obj.aggregate(outputs=glob('../results/*.txt'))
