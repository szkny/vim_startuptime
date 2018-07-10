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

nvim start-up time (100 loops) : 268.656 +/- 31.010 [msec]
+----------------------------------+--------------------+
|             PROCESS              |        TIME        |
+----------------------------------+--------------------+
|        sourcing init.vim         | 111.597 +/- 13.402 |
|         opening buffers          |  61.385 +/- 7.794  |
|   sourcing plugin_setting.vim    |  14.665 +/- 1.162  |
|         loading plugins          |  14.335 +/- 1.847  |
|       sourcing mapping.vim       |  14.171 +/- 1.170  |
|      sourcing filetype.vim       |  12.952 +/- 3.027  |
|          reading ShaDa           |   9.660 +/- 1.229  |
|       sourcing syntax.vim        |   8.218 +/- 1.770  |
|       sourcing molokai.vim       |   8.210 +/- 1.464  |
|      sourcing UltiSnips.vim      |   6.525 +/- 1.289  |
|     sourcing delimitMate.vim     |   5.887 +/- 1.555  |
|       sourcing rplugin.vim       |   4.836 +/- 0.890  |
|      sourcing tcomment.vim       |   4.647 +/- 1.120  |
|       sourcing synload.vim       |   4.567 +/- 0.997  |
|      BufEnter autocommands       |   4.487 +/- 1.094  |
              ...                            ...
```

## screenshots

- pie graph

![images0](https://github.com/szkny/vim_startuptime/wiki/images/vim_start-up_time_0.png)

- line graph

![images1](https://github.com/szkny/vim_startuptime/wiki/images/vim_start-up_time_1.png)

- histogram

![images2](https://github.com/szkny/vim_startuptime/wiki/images/vim_start-up_time_2.png)
