@echo off
cd %~dp0
copy /Y .\renee.dict.yaml %APPDATA%\Rime\renee.dict.yaml
copy /Y .\renee.schema_compfalse.yaml %APPDATA%\Rime\renee.schema.yaml
"C:\Program Files (x86)\Rime\weasel-0.14.3\WeaselDeployer.exe" /deploy
copy /Y %APPDATA%\Rime\build\renee.*.bin .\*
del %APPDATA%\Rime\renee.dict.yaml
@pause