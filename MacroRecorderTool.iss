
[Setup]
AppName=Macro Recorder Tool
AppVersion=1.0
AppVerName=Macro Recorder Tool v1.0
AppPublisher=Macro Recorder Development
DefaultDirName={autopf}\MacroRecorderTool
DefaultGroupName=Macro Recorder Tool
UninstallDisplayIcon={app}\MacroRecorderTool.exe
Compression=lzma2
SolidCompression=yes
OutputDir=installer
OutputBaseFilename=MacroRecorderTool_Setup
SetupIconFile=app_icon.ico
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "vietnamese"; MessagesFile: "compiler:Languages\Vietnamese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\MacroRecorderTool.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Macro Recorder Tool"; Filename: "{app}\MacroRecorderTool.exe"
Name: "{group}\{cm:UninstallProgram,Macro Recorder Tool}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Macro Recorder Tool"; Filename: "{app}\MacroRecorderTool.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\MacroRecorderTool.exe"; Description: "{cm:LaunchProgram,Macro Recorder Tool}"; Flags: nowait postinstall skipifsilent

[Code]
function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppId")}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;

function UnInstallOldVersion(): Integer;
var
  sUnInstallString: String;
  iResultCode: Integer;
begin
  Result := 0;
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Exec(sUnInstallString, '/SILENT /NORESTART /SUPPRESSMSGBOXES','', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
      Result := 3
    else
      Result := 2;
  end else
    Result := 1;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep=ssInstall) then
  begin
    if (IsUpgrade()) then
    begin
      UnInstallOldVersion();
    end;
  end;
end;
