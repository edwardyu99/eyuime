@rem @echo off
cd %~dp0
@rem cd %APPDATA%\Rime\

if not exist %APPDATA%\Rime\ mkdir %APPDATA%\Rime\
if not exist %APPDATA%\Rime\build\ mkdir %APPDATA%\Rime\build\

inuse .\renee.table.bin %APPDATA%\Rime\build\* /Y 

copy /Y .\renee.table.bin %APPDATA%\Rime\build\*

copy /Y .\renee.prism.bin %APPDATA%\Rime\build\*
copy /Y .\renee.reverse.bin %APPDATA%\Rime\build\*
copy /Y .\renee.schema.yaml %APPDATA%\Rime\build\*
if not exist "C:\Program Files (x86)\Rime\weasel-0.14.3\WeaselDeployer.exe"   %APPDATA%\Rime\weasel-0.14.3.0-installer.exe
"C:\Program Files (x86)\Rime\weasel-0.14.3\WeaselDeployer.exe" /deploy


pause