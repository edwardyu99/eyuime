@echo on
cd %~dp0
@rem copy /Y .\renee.dict.yaml ..\rimeCan\.
cd .\output\
powershell "Compress-Archive -Path setupReneeRime.exe -DestinationPath setupReneeRime.zip -Force"
cd ..
@pause

