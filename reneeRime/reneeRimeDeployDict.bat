@echo on
cd %~dp0
copy /Y .\default.custom.yaml "%APPDATA%\Rime\*"
copy /Y .\installation.yaml "%APPDATA%\Rime\*"
copy /Y .\renee.dict.yaml "%APPDATA%\Rime\*"
copy /Y .\renee.schema.yaml "%APPDATA%\Rime\*"
copy /Y .\renee.ico "%APPDATA%\Rime\*"
copy /Y .\user.yaml "%APPDATA%\Rime\*"
copy /Y .\weasel.custom.yaml "%APPDATA%\Rime\*"

@rem --- Deploy using the dynamic path with a wildcard ---
set "WeaselDir=C:\Program Files\Rime"
for /d %%i in ("%WeaselDir%\weasel*") do "%%i\WeaselDeployer.exe" /deploy
@rem "C:\Program Files\Rime\weasel-0.17.4\WeaselDeployer.exe" /deploy

@rem copy /Y %APPDATA%\Rime\build\renee.*.bin .\*
@rem del %APPDATA%\Rime\renee.dict.yaml
@rem copy /Y %APPDATA%\Rime\build\renee.*.bin ..\rimeCan\*
@rem copy /Y %APPDATA%\Rime\build\renee.schema.yaml ..\rimeCan\*
@pause