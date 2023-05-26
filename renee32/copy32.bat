@echo off
cd %~dp0

if not exist %windir%\System32\uimetool.exe copy /Y .\uimetool.exe %windir%\System32\*
if not exist %windir%\System32\miniime.tpl copy /Y .\miniime.tpl %windir%\System32\*
copy /Y .\renee.tbl %windir%\System32\*
copy /Y .\reneePHR.tbl %windir%\System32\*
copy /Y .\reneePTR.tbl %windir%\System32\*
regedit.exe /s .\renee.reg
control.exe intl.cpl,,/f:".\renee.xml"
@rem %windir%\System32\ctfmon.exe
inuse   .\renee.ime %windir%\System32\* /Y 
if not exist %windir%\System32\renee.ime copy /Y .\renee.ime %windir%\System32\* 
@rem copy /Y .\renee.ime %windir%\System32\* 
if not exist %windir%\System32\uniime.dll copy /Y .\uniime.dll %windir%\System32\*
IF %ERRORLEVEL% NEQ 0 (
   dir %windir%\System32\renee*.*
   @rem dir %windir%\System32\uniime.dll
   @rem dir %windir%\System32\uimetool.exe
   @rem dir %windir%\System32\miniime.tpl
@echo *  
@echo *** renee.ime not copied. Please restart windows and rerun setup.bat
  @pause
)
