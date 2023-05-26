@echo on
cd %~dp0
copy /Y .\renee.*.bin ..\rimeCan\.
cd .\output\
powershell "Compress-Archive -Path ..\..\rimeCan\* -DestinationPath androidReneeRimeCan.zip -Force"
cd ..
@pause

