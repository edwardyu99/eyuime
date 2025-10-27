@echo off
@rem cd %~dp0
cd /d "%~dp0"
echo Current directory is now: %CD%
@rem cd %APPDATA%\Rime\

if not exist %APPDATA%\Rime\ mkdir %APPDATA%\Rime\
if not exist %APPDATA%\Rime\build\ mkdir %APPDATA%\Rime\build\

@rem copy /Y .\renee.schema.yaml %APPDATA%\Rime\build\*
copy /Y .\renee.ico %APPDATA%\Rime\build\*
copy /Y .\renee.dict.head.yaml %APPDATA%\Rime\renee.dict.yaml
@rem copy /Y .\default.custom.yaml %APPDATA%\Rime\*
@rem copy /Y .\installation.yaml %APPDATA%\Rime\*
@rem copy /Y .\weasel.custom.yaml %APPDATA%\Rime\*
@rem copy /Y .\user.yaml %APPDATA%\Rime\*

@rem --- Deploy using the dynamic path with a wildcard ---
set "WeaselDir=C:\Program Files\Rime"
for /d %%i in ("%WeaselDir%\weasel*") do "%%i\WeaselDeployer.exe" /deploy
@rem "C:\Program Files\Rime\weasel-0.17.4\WeaselDeployer.exe" /deploy
copy /Y .\renee.prism.bin %APPDATA%\Rime\build\*
copy /Y .\renee.reverse.bin %APPDATA%\Rime\build\*
@rem inuse .\renee.table.bin %APPDATA%\Rime\build\* /Y 
copy /Y .\renee.table.bin %APPDATA%\Rime\build\*




@pause