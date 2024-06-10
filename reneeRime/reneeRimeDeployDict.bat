@echo off
cd %~dp0
copy /Y .\renee.dict.yaml %APPDATA%\Rime\renee.dict.yaml
@rem copy /Y .\renee.schema.yaml %APPDATA%\Rime\renee.schema.yaml
copy /Y .\renee.schema.yaml %APPDATA%\Rime\renee.schema.yaml
"C:\Program Files (x86)\Rime\weasel-0.16.1\WeaselDeployer.exe" /deploy
copy /Y %APPDATA%\Rime\build\renee.*.bin .\*
del %APPDATA%\Rime\renee.dict.yaml
copy /Y %APPDATA%\Rime\build\renee.*.bin ..\rimeCan\*
copy /Y %APPDATA%\Rime\build\renee.schema.yaml ..\rimeCan\*
@pause