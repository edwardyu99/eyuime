@echo off
cd %~dp0
copy /Y .\renee.ime %windir%\System32\*
copy /Y .\renee.tbl %windir%\System32\*
copy /Y .\reneePHR.tbl %windir%\System32\*
copy /Y .\reneePTR.tbl %windir%\System32\*
if not exist %windir%\System32\uniime.dll copy /Y .\uniime.dll %windir%\System32\*
if not exist %windir%\System32\uimetool.exe copy /Y .\uimetool.exe %windir%\System32\*
if not exist %windir%\System32\miniime.tpl copy /Y .\miniime.tpl %windir%\System32\*
regedit /s .\renee.reg
@rem dir %windir%\System32\renee*.*
@rem dir %windir%\System32\uniime.dll
@rem dir %windir%\System32\uimetool.exe
@rem dir %windir%\System32\miniime.tpl
@rem pause