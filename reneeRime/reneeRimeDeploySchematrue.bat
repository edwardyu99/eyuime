@echo off
cd %~dp0
copy /Y .\renee.schema_comptrue.yaml %APPDATA%\Rime\renee.schema.yaml
"C:\Program Files (x86)\Rime\weasel-0.14.3\WeaselDeployer.exe" /deploy
