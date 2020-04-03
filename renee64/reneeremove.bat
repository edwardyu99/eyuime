@echo off
cd %~dp0
@rem control.exe intl.cpl,,/f:".\reneeremove.xml"
control intl.cpl,, /f:"%CD%\reneeremove.xml"
