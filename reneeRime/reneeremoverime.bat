@echo off
cd %~dp0

del .\renee.schema*.yaml
del .\reneecopyrime.bat
@rem del .\renee.table.bin
del .\renee.*.bin
del .\reneeRimeDeploy*.bat
del .\reneeRime.iss
del %APPDATA%\Rime\renee.schema*.yaml

@rem del %APPDATA%\Rime\build\renee.table.bin
del %APPDATA%\Rime\build\renee.*.bin
del .\weasel-0.14.3.0-installer.exe

@rem IF %ERRORLEVEL% NEQ 0 (   
@rem   @echo *
@rem   @echo *** copyrime error. Please restart windows and rerun setupReneeRime.exe
@rem )
@rem pause