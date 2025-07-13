chcp 65001
@echo off
setlocal

REM 检查是否存在 .venv 下的 python 解释器
if exist ".venv\Scripts\python.exe" (
    set PYTHON_EXEC=.venv\Scripts\python.exe
) else (
    echo 未找到虚拟环境，请先执行：
    echo     python -m venv .venv
    echo     .venv\Scripts\activate
    echo     pip install -r requirements.txt
    exit /b 1
)

REM 执行 Python 脚本并传入所有命令行参数
%PYTHON_EXEC% img.py %*

endlocal
