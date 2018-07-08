# vim_startuptime
Analyzer of vim start-up time (python3)  

## download
Execute "git clone" command.  
```bash
$ git clone https://github.com/szkny/vim_startuptime.git
```
Or download zip file.  
```bash:bash
$ cd [Path to "vim_startuptime.zip"]
$ unzip vim_startuptime.zip
```

## usage
Go to directory where "vim_startuptime" executable exists.  
Then, execute vim_startuptime.
```bash:bash
$ python ./vim_startuptime.py

nvim start-up time (20 loops) : 190.505 +/- 16.163 [msec]
        --- PROCESS ---
        sourcing init.vim                        70.315 +/- 4.660
        opening buffers                          56.086 +/- 5.451
        sourcing filetype.vim                    32.283 +/- 1.606
        sourcing mapping.vim                      9.840 +/- 1.164
        loading plugins                           7.885 +/- 0.743
        reading ShaDa                             5.858 +/- 0.745
        sourcing delimitMate.vim                  5.138 +/- 0.330
        BufEnter autocommands                     4.843 +/- 0.775
        sourcing tcomment.vim                     4.061 +/- 0.231
        clearing screen                           3.421 +/- 0.881
        sourcing molokai.vim                      3.254 +/- 0.360
        sourcing syntax.vim                       3.048 +/- 0.649
        sourcing airline.vim                      2.804 +/- 0.212
        sourcing webdevicons.vim                  2.748 +/- 0.380
        sourcing UltiSnips.vim                    2.627 +/- 1.118
                ...                                    ...
```
![vim_startuptime images](https://github.com/szkny/vim_startuptime/wiki/images/vim_start-up_time.png)
