@echo on
cd %~dp0
copy /Y  %SystemRoot%\System32\renee.ime .
copy /Y  %SystemRoot%\System32\reneephr.tbl .
copy /Y  %SystemRoot%\System32\reneeptr.tbl .
copy /Y  %SystemRoot%\System32\renee.tbl .
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" ./renee64.iss
@pause

