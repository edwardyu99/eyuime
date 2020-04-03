@echo on
cd %~dp0
.\simyu32.exe
copy /Y .\simyu.ime %windir%\System32\*
copy /Y .\simyu.tbl %windir%\System32\*
copy /Y .\simyuPHR.tbl %windir%\System32\*
copy /Y .\simyuPTR.tbl %windir%\System32\*
if not exist %windir%\System32\uniime.dll copy /Y .\uniime.dll %windir%\System32\*
@rem if not exist %windir%\System32\uimetool.exe copy /Y .\uimetool.exe %windir%\System32\*
@rem if not exist %windir%\System32\miniime.tpl copy /Y .\miniime.tpl %windir%\System32\*
regedit /s .\simyu.reg
regedit /s .\simyusim.reg
dir %windir%\Syswow64\simyu*.*
dir %windir%\System32\simyu*.*
pause