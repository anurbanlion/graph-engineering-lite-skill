@echo off
setlocal

python "%~dp0sync_folder.py" %*
exit /b %ERRORLEVEL%
