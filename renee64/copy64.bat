@rem echo off
cd %~dp0
@rem .\setupRenee32.exe
if not exist %windir%\System32\uimetool.exe copy /Y .\uimetool.exe %windir%\System32\*
if not exist %windir%\System32\miniime.tpl copy /Y .\miniime.tpl %windir%\System32\*
regedit.exe /s .\renee.reg
control.exe intl.cpl,,/f:".\renee.xml"
@rem 點選開始功能表，在「開始搜尋」的輸入框中輸入"regedit"並執行，找到以下編碼： 
@rem "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" 
@rem 此行便是在開機的時候應該自動執行的程式清單，右邊的欄位應該要有ctfmon字串值，
@rem 如果消失了代表問題就出在這裡！ 修正辦法為：在右邊欄位點選右鍵新增字串值"ctfmon"，
@rem 然後再修改這個字串值的數值資料為 "C:\Windows\system32\ctfmon.exe" 完成後關閉。
%windir%\System32\ctfmon.exe
@rem regedit /s .\reneesim.reg
copy /Y .\renee.tbl %windir%\System32\*
copy /Y .\reneePHR.tbl %windir%\System32\*
copy /Y .\reneePTR.tbl %windir%\System32\*
inuse   .\renee.ime %windir%\System32\* /Y 
if not exist %windir%\System32\renee.ime copy /Y .\renee.ime %windir%\System32\* 
if not exist %windir%\System32\uniime.dll copy /Y .\uniime.dll %windir%\System32\*
IF %ERRORLEVEL% NEQ 0 (
   dir %windir%\System32\renee*.*
   @rem dir %windir%\System32\uniime.dll
   @rem dir %windir%\System32\uimetool.exe
   @rem dir %windir%\System32\miniime.tpl
  @echo *
  @echo *** renee.ime not copied. Please restart windows and rerun setupRenee3264.bat
  @pause
)
