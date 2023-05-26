powershell "Compress-Archive -Path setupRenee32.exe -DestinationPath setupRenee32.zip -Force"
powershell "Compress-Archive -Path *.bat, *.xml, *.exe -DestinationPath setupRenee64.zip -Force"
@pause