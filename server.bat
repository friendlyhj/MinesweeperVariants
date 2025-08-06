chcp 65001
@echo off
setlocal

REM 执行 Python 脚本并传入所有命令行参数
.venv\Scripts\python.exe web.py %*

pause
