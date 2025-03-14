﻿; Script generated by the Inno Script Studio Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!
; 20230803 "weasel-0.15.0.0-installer.exe" no longer provided here because of google virus check.
;          Please download and install latest version of weasel from https://rime.im/
; 20240609 update rime from 0.15.0 to 0.16.1
#define MyAppName "余氏中文輸入法 (小狼毫版)"
#define MyAppVersion "64bits windows 10 (RIME小狼毫版)"
#define MyAppPublisher "Edward Yu"
#define MyAppURL "https://sites.google.com/site/eykmime"
#define MyAppExeName "MyProg.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{84927019-5C31-4A37-9B2E-E35A6C111950}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={%APPDATA}\Rime
CreateAppDir=yes 
; no
OutputBaseFilename=setupReneeRime
Compression=lzma
SolidCompression=yes
AlwaysRestart=yes
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64
UninstallRestartComputer=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "inuse.exe"; DestDir: "{win}"; Flags: ignoreversion
Source: "reneecopyrime.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "reneeremoverime.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "default.custom.yaml"; DestDir: "{app}"; Flags: ignoreversion
Source: "reneeRime.iss"; DestDir: "{app}"; Flags: ignoreversion
Source: "renee.prism.bin"; DestDir: "{app}"; Flags: ignoreversion
Source: "renee.reverse.bin"; DestDir: "{app}"; Flags: ignoreversion
Source: "renee.schema.yaml"; DestDir: "{app}"; Flags: ignoreversion
Source: "renee.dict_head.yaml"; DestDir: "{app}"; Flags: ignoreversion
Source: "renee.table.bin"; DestDir: "{app}"; Flags: ignoreversion
Source: "reneeRimeDeploy.bat"; DestDir: "{app}"; Flags: ignoreversion
; Source: "Trime-20200909.apk"; DestDir: "{app}"; Flags: ignoreversion
Source: "renee.rimecan.sh"; DestDir: "{app}"; Flags: ignoreversion
Source: "default.yaml"; DestDir: "{app}"; Flags: ignoreversion
Source: "renee.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "weasel.custom.yaml"; DestDir: "{app}"; Flags: ignoreversion
; https://rime.im/download/ 
;Source: "weasel_0chinese_lnk.txt"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weasel_1user_folder.lnk"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weasel_2dict_manager.lnk"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weasel_3sync.lnk"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weasel_4setup_option.lnk"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weasel_5deplloy.lnk"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weasel_6APPDATA.lnk"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weasel_7readme.lnk"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weasel_8input_option.lnk"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weasel_9update.lnk"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weasel_server.lnk"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weasel_uninstall.lnk"; DestDir: "{app}"; Flags: ignoreversion
;Source: "weasel-0.15.0.0-installer.exe"; DestDir: "{app}"; Flags: ignoreversion
; 0.14.3.0
; NOTE: Don't use "Flags: ignoreversion" on any shared system files
[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\RunOnce"; \
    ValueType: string; ValueName: "MyProg"; ValueData: """{app}\reneeRimeDeploy.bat"""

[Run]
Filename: "{app}\reneecopyrime.bat"
[UninstallRun]
Filename: "{app}\reneeremoverime.bat"
