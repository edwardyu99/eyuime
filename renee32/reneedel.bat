@echo off
cd %~dp0

C:\Windows\system32\regedt32.exe /s .\reneedel.reg
C:\Windows\syswow64\regedit.exe /s .\reneedel.reg


@echo *  
@echo *** Yu's input method deleted. Please restart windows
  @pause

