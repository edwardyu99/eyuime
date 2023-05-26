@echo on
cd %~dp0
copy /Y  %SystemRoot%\SysWOW64\renee.ime .
copy /Y  %SystemRoot%\SysWOW64\reneephr.tbl .
copy /Y  %SystemRoot%\SysWOW64\reneeptr.tbl .
copy /Y  %SystemRoot%\SysWOW64\renee.tbl .
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" ./renee32.iss
copy /Y .\output\setupRenee32.exe ..\renee64\output\.
@pause

