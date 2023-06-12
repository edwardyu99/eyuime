cd %APPDATA%\Rime\

taskkill /F /IM WeaselServer.exe"
start "" /D "C:\Program Files (x86)\Rime\weasel-0.15.0\" "WeaselServer.exe" /B
@rem Restart-Service -Name service.exe
"C:\Program Files (x86)\Rime\weasel-0.15.0\WeaselDeployer.exe" /deploy
@rem shutdown /l
pause