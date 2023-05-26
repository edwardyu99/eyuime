## Enable script tracing  #similar to .bat echo on
# Set-PSDebug -Trace 1

# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned / Unrestricted # for doble-click .ps1 script
# This is a comment
# Write-Host "Hello, World!" # This is also a comment

# Set the source and destination paths
$src = "C:\Users\Dad\OneDrive\eyuime"
$dst = "C:\github\eyuime"

# Get the date of the last commit
$lastCommitDateString = git -C $dst log -1 --format=%cd
$lastCommitDate = [DateTime]::ParseExact($lastCommitDateString, "ddd MMM d HH:mm:ss yyyy K", [System.Globalization.CultureInfo]::InvariantCulture)

# Copy files modified since the last commit
Get-ChildItem $src -Recurse | Where-Object { $_.LastWriteTime -gt $lastCommitDate } | ForEach-Object {
    $destination = $_.FullName.Replace($src, $dst)
#Set-PSDebug -Trace 1
    Copy-Item $_.FullName -Destination $destination -Force
#Set-PSDebug -Trace 0
    Write-Output "Copied file: $($_.FullName)"
}
Read-Host -Prompt "Press Enter to continue"