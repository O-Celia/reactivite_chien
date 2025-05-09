@echo off
cd /d "%~dp0"

set WINPYTHONPATH="%~dp0WPy64-31241\python-3.12.4.amd64\python.exe"

WPy64-31241\python-3.12.4.amd64\python.exe -m pip install -r app\requirements.txt

start "Backend" cmd /k "cd /d %~dp0app && %WINPYTHONPATH% -m uvicorn main:app --reload"

timeout /t 5 >nul

cd /d "%~dp0streamlit_app"

%WINPYTHONPATH% -m streamlit run main_app.py

pause
