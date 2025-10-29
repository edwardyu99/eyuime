@echo off
cd %~dp0
@rem cd /d "%~dp0"
@rem echo Current directory is now: %CD%
@rem cd %APPDATA%\Rime\

if not exist %APPDATA%\Rime\ mkdir %APPDATA%\Rime\
if not exist %APPDATA%\Rime\build\ mkdir %APPDATA%\Rime\build\

@rem copy /Y .\renee.schema.yaml %APPDATA%\Rime\build\*
@rem copy /Y .\renee.ico %APPDATA%\Rime\build\*

@rem copy /Y .\default.custom.yaml %APPDATA%\Rime\*
@rem copy /Y .\installation.yaml %APPDATA%\Rime\*
@rem copy /Y .\weasel.custom.yaml %APPDATA%\Rime\*
@rem copy /Y .\user.yaml %APPDATA%\Rime\*

@rem copy /Y .\renee.prism.bin %APPDATA%\Rime\build\*
@rem copy /Y .\renee.reverse.bin %APPDATA%\Rime\build\*
@rem inuse .\renee.table.bin %APPDATA%\Rime\build\* /Y 
@rem copy /Y .\renee.table.bin %APPDATA%\Rime\build\*

@rem pause