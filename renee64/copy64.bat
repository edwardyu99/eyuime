@rem echo off
cd %~dp0
@rem .\setupRenee32.exe
if not exist %windir%\System32\uimetool.exe copy /Y .\uimetool.exe %windir%\System32\*
if not exist %windir%\System32\miniime.tpl copy /Y .\miniime.tpl %windir%\System32\*
regedit.exe /s .\renee.reg
control.exe intl.cpl,,/f:".\renee.xml"
@rem �c�x�_ʼ���ܱ��ڡ��_ʼ�ь�����ݔ�����ݔ��"regedit"�K���У��ҵ����¾��a�� 
@rem "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" 
@rem ���б������_�C�ĕr��ԓ�Ԅӈ��еĳ�ʽ��Σ���߅�ę�λ��ԓҪ��ctfmon�ִ�ֵ��
@rem �����ʧ�˴��톖�}�ͳ����@�e�� �����k���飺����߅��λ�c�x���I�����ִ�ֵ"ctfmon"��
@rem Ȼ�����޸��@���ִ�ֵ�Ĕ�ֵ�Y�Ϟ� "C:\Windows\system32\ctfmon.exe" ������P�]��
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
