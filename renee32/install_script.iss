;InnoSetupVersion=5.5.7 (Unicode)

[Setup]
AppName=‰ΩôÊ∞è‰∏≠ÊñáËº∏ÂÖ•Ê≥ï32bits
AppId={{6E7B8FA5-3F31-47CD-A6DE-4D26465009BE}
AppVersion=64bits windows 10 (20170907 èVñ|◊÷≈≈œ»∞Ê)
AppPublisher=Edward Yu
AppPublisherURL=https://sites.google.com/site/eykmime/eywin98
AppSupportURL=https://sites.google.com/site/eykmime/eywin98
AppUpdatesURL=https://sites.google.com/site/eykmime/eywin98
CreateAppDir=no
OutputBaseFilename=setuprenee32
Compression=lzma
DisableDirPage=auto
DisableProgramGroupPage=auto
WizardImageFile=embedded\WizardImage0.bmp
WizardSmallImageFile=embedded\WizardSmallImage0.bmp

[Files]
Source: "{win}\copy32.bat"; DestDir: "{win}"; MinVersion: 0.0,5.0; Flags: ignoreversion 
Source: "{win}\miniime.tpl"; DestDir: "{win}"; MinVersion: 0.0,5.0; Flags: ignoreversion 
Source: "{win}\renee.IME"; DestDir: "{win}"; MinVersion: 0.0,5.0; Flags: ignoreversion 
Source: "{win}\renee.reg"; DestDir: "{win}"; MinVersion: 0.0,5.0; Flags: ignoreversion 
Source: "{win}\renee.TBL"; DestDir: "{win}"; MinVersion: 0.0,5.0; Flags: ignoreversion 
Source: "{win}\reneePHR.TBL"; DestDir: "{win}"; MinVersion: 0.0,5.0; Flags: ignoreversion 
Source: "{win}\reneePTR.TBL"; DestDir: "{win}"; MinVersion: 0.0,5.0; Flags: ignoreversion 
Source: "{win}\UIMETOOL.exe"; DestDir: "{win}"; MinVersion: 0.0,5.0; Flags: ignoreversion 
Source: "{win}\UNIIME.DLL"; DestDir: "{win}"; MinVersion: 0.0,5.0; Flags: ignoreversion 
Source: "{win}\inuse.exe"; DestDir: "{win}"; MinVersion: 0.0,5.0; Flags: ignoreversion 

[Run]
Filename: "{app}\copy32.bat"; MinVersion: 0.0,5.0; 

[CustomMessages]
english.NameAndVersion=%1 version %2
english.AdditionalIcons=Additional shortcuts:
english.CreateDesktopIcon=Create a &desktop shortcut
english.CreateQuickLaunchIcon=Create a &Quick Launch shortcut
english.ProgramOnTheWeb=%1 on the Web
english.UninstallProgram=Uninstall %1
english.LaunchProgram=Launch %1
english.AssocFileExtension=&Associate %1 with the %2 file extension
english.AssocingFileExtension=Associating %1 with the %2 file extension...
english.AutoStartProgramGroupDescription=Startup:
english.AutoStartProgram=Automatically start %1
english.AddonHostProgramNotFound=%1 could not be located in the folder you selected.%n%nDo you want to continue anyway?

[Languages]
; These files are stubs
; To achieve better results after recompilation, use the real language files
Name: "english"; MessagesFile: "embedded\english.isl"; 
