; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Automate-It Installer"
#define MyAppVersion "2.0"
#define MyAppPublisher "Kedvall Studios"
#define MyAppURL "https://kedvall.github.io/CompanySoftware/"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{2689FB3E-FBFA-4788-BB28-7D64B0ED5BAC}
SetupIconFile="C:\Users\kedvall\dev\CompanySoftware\SJE\Program Builder\icons\Automate-It Installer.ico"
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\Automate-It Suite
DefaultGroupName=Automate-It Suite
OutputBaseFilename=Automate-It Installer
Password=SJE2016!
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\kedvall\dev\CompanySoftware\SJE\Program Builder\dist\Excel Data Mapper.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\kedvall\dev\CompanySoftware\SJE\Program Builder\dist\Excel Extractor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\kedvall\dev\CompanySoftware\SJE\Program Builder\dist\IFS Importer.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\kedvall\dev\CompanySoftware\SJE\IFS Importer\helper\ActivateIFS.exe"; DestDir: "{app}\helper"; Flags: ignoreversion
Source: "C:\Users\kedvall\dev\CompanySoftware\SJE\IFS Importer\helper\ActivateImporter.exe"; DestDir: "{app}\helper"; Flags: ignoreversion
Source: "C:\Users\kedvall\dev\CompanySoftware\SJE\IFS Importer\helper\ActivateInventoryPart.exe"; DestDir: "{app}\helper"; Flags: ignoreversion
Source: "C:\Users\kedvall\dev\CompanySoftware\SJE\IFS Importer\helper\FocusControl.exe"; DestDir: "{app}\helper"; Flags: ignoreversion
Source: "C:\Users\kedvall\dev\CompanySoftware\SJE\IFS Importer\helper\GetControlID.exe"; DestDir: "{app}\helper"; Flags: ignoreversion
Source: "C:\Users\kedvall\dev\CompanySoftware\SJE\IFS Importer\helper\GetControlValue.exe"; DestDir: "{app}\helper"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{userdesktop}\Excel Data Mapper"; Filename: "{app}\Excel Data Mapper.exe"; IconFilename: "{app}\Excel Data Mapper.exe"; Tasks: desktopicon
Name: "{userdesktop}\Excel Extractor"; Filename: "{app}\Excel Extractor.exe"; IconFilename: "{app}\\Excel Extractor.exe"; Tasks: desktopicon
Name: "{userdesktop}\IFS Importer.exe"; Filename: "{app}\IFS Importer.exe"; IconFilename: "{app}\IFS Importer.exe"; Tasks: desktopicon
