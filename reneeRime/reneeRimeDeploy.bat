cd %APPDATA%\Rime\

@rem taskkill /F /IM WeaselServer.exe"
@rem start "" /D "C:\Program Files (x86)\Rime\weasel-0.16.3\" "WeaselServer.exe" /B
@rem Restart-Service -Name service.exe
"C:\Program Files (x86)\Rime\weasel-0.17.4\WeaselDeployer.exe" /deploy
@rem shutdown /l
@rem pause