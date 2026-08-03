@echo off
setlocal

node "%~dp0sync-folder.mjs" %*
exit /b %ERRORLEVEL%
