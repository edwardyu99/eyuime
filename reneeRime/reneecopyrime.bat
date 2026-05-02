@echo off
setlocal
cd /d "%~dp0"

REM 確保 Rime 資料夾結構完整
if not exist "%APPDATA%\Rime" mkdir "%APPDATA%\Rime"
if not exist "%APPDATA%\Rime\build" mkdir "%APPDATA%\Rime\build"

REM 確保 package.yaml 存在於 Rime 根目錄
if exist "package.yaml" copy /Y "package.yaml" "%APPDATA%\Rime\"

echo [余氏輸入法] 安裝程序已完成環境配置。
endlocal

