@echo off
cd %APPDATA%\Rime\

@rem taskkill /F /IM WeaselServer.exe"
@rem start "" /D "C:\Program Files (x86)\Rime\weasel-0.16.3\" "WeaselServer.exe" /B
@rem Restart-Service -Name service.exe
@rem --- Deploy using the dynamic path with a wildcard ---
set "WeaselDir=C:\Program Files\Rime"
for /d %%i in ("%WeaselDir%\weasel*") do "%%i\WeaselDeployer.exe" /deploy
@rem "C:\Program Files\Rime\weasel-0.17.4\WeaselDeployer.exe" /deploy

del %APPDATA%\Rime\renee.dict.yaml

@rem shutdown /l
@rem pause