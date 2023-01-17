# vim_startuptime
Analyzer of vim start-up time (python3)  

## download
Execute "git clone" command.  
```bash
$ git clone https://github.com/szkny/vim_startuptime.git
```
Or download zip file.  
```bash:bash
$ cd [Path to directory "vim_startuptime.zip" exists]
$ unzip vim_startuptime.zip
```

## install

Change directory where "requirements.txt" (or "Pipfile") executable exists.  
You should install requirement python modules by "pip" or "pipenv" command.  

- pip

```bash
$ pip install -r requirements.txt
```

- pipenv

```bash
$ pipenv install
```

## usage
Change to directory where "vim_startuptime.py" python code exists.  
Then, execute python script.  
```bash
$ python ./vim_startuptime.py

nvim start-up time (300 loops) : 190.694 +/- 30.688 [msec]
+--------------------------+--------------------+
|         PROCESS          |        TIME        |
+--------------------------+--------------------+
|    sourcing init.vim     |  71.734 +/- 10.502 |
|     opening buffers      |  53.516 +/- 10.600 |
|  sourcing filetype.vim   |  32.099 +/- 3.639  |
|   sourcing mapping.vim   |  10.838 +/- 3.203  |
|     loading plugins      |   8.382 +/- 3.786  |
|      reading ShaDa       |   6.517 +/- 1.056  |
| sourcing delimitMate.vim |   5.395 +/- 1.019  |
|  BufEnter autocommands   |   4.798 +/- 1.142  |
|  sourcing tcomment.vim   |   4.318 +/- 0.899  |
|   sourcing molokai.vim   |   3.346 +/- 0.627  |
|           ...            |        ...         |
+--------------------------+--------------------+
```

Otherwise, if you have installed by pipenv, you could run like this,  
```bash
$ pipenv run python ./vim_startuptime.py
```
