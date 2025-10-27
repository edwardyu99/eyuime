@rem @echo off
@rem cd %~dp0
cd /d "%~dp0"
echo Current directory is now: %CD%
@rem cd %APPDATA%\Rime\

if not exist %APPDATA%\Rime\ mkdir %APPDATA%\Rime\
if not exist %APPDATA%\Rime\build\ mkdir %APPDATA%\Rime\build\

inuse .\renee.table.bin %APPDATA%\Rime\build\* /Y 

copy /Y .\renee.table.bin %APPDATA%\Rime\build\*

copy /Y .\renee.prism.bin %APPDATA%\Rime\build\*
copy /Y .\renee.reverse.bin %APPDATA%\Rime\build\*
copy /Y .\renee.schema.yaml %APPDATA%\Rime\build\*
copy /Y .\renee.ico %APPDATA%\Rime\build\*
copy /Y .\default.custom.yaml %APPDATA%\Rime\build\*
copy /Y .\weasel.custom.yaml %APPDATA%\Rime\build\*
@rem if not exist "C:\Program Files (x86)\Rime\weasel-0.16.3\WeaselDeployer.exe"   %APPDATA%\Rime\weasel-0.16.3.0-installer.exe
@rem if not exist "C:\Program Files (x86)\Rime\weasel-0.17.4\WeaselDeployer.exe"   %APPDATA%\Rime\weasel-0.17.4.0-installer.exe

cd %APPDATA%\Rime\
@rem "C:\Program Files\Rime\weasel-0.17.4\WeaselServer.exe"
"C:\Program Files\Rime\weasel-0.17.4\WeaselDeployer.exe" /deploy

@pause