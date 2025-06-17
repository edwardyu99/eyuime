#!/bin/bash

echo "Removing unused packages and dependencies..."
sudo apt-get autoremove && sudo apt-get autoclean

echo "Cleaning temporary files..."
sudo rm -rf /tmp/*
sudo rm -rf /var/tmp/*

# echo "Removing Docker leftovers..."
# docker system prune -f

echo "Running shrink_vhdx.bat to shrink the VHDX file..."
powershell.exe -Command "Start-Process -FilePath 'C:\\Edward\\shrink_vhdx.bat' -Verb RunAs"

echo "Shrink process initiated. Please check the output in the command prompt window."

echo "Cleanup completed."

