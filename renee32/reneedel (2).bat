@echo off
cd %~dp0

regedit.exe /s .\reneedel.reg

@echo *  
@echo *** Yu's input method deleted. Please restart windows
  @pause

