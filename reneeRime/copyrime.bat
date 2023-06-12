@rem echo off
cd %~dp0

if not exist %APPDATA%\Rime\ mkdir %APPDATA%\Rime\
if not exist %APPDATA%\Rime\build\ mkdir %APPDATA%\Rime\build\
@rem copy /Y .\default.custom.yaml %APPDATA%\Rime\*
@rem copy /Y .\renee.schema.yaml %APPDATA%\Rime\*
%APPDATA%\Rime\weasel-0.15.0.0-installer.exe

@rem copy /Y .\renee.prism.bin %APPDATA%\Rime\build\*
@rem copy /Y .\renee.reverse.bin %APPDATA%\Rime\build\*


@rem inuse .\renee.table.bin %APPDATA%\Rime\build\* /Y 
@rem if not exist %APPDATA%\Rime\build\renee.table.bin copy /Y .\renee.table.bin %APPDATA%\Rime\build\*

@rem IF %ERRORLEVEL% NEQ 0 (   
@rem   @echo *
@rem   @echo *** copyrime error. Please restart windows and rerun setupReneeRime.exe
@rem )
@pause