#!/usr/bin/env python3
"""
Script để build Macro Recorder Tool thành executable
Sử dụng PyInstaller để tạo standalone .exe file
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_requirements():
    """Cài đặt các thư viện cần thiết"""
    print("📦 Cài đặt dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Đã cài đặt dependencies")
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi cài đặt: {e}")
        return False
    return True

def clean_build():
    """Xóa các file build cũ"""
    print("🧹 Dọn dẹp build cũ...")
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Xóa {dir_name}/")
    
    # Xóa .spec files cũ
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"   Xóa {spec_file}")

def create_icon():
    """Tạo icon cho app nếu chưa có"""
    icon_path = "app_icon.ico"
    if not os.path.exists(icon_path):
        print("🎨 Tạo icon mặc định...")
        # Tạo icon đơn giản bằng PIL nếu có
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Tạo icon 256x256
            img = Image.new('RGBA', (256, 256))  # Create blank RGBA image
            img.paste((65, 105, 225, 255), [0, 0, 256, 256])  # Fill with RoyalBlue
            draw = ImageDraw.Draw(img)
            
            # Vẽ background gradient
            for i in range(256):
                color = (65 + i//8, 105 + i//8, 225, 255)
                draw.line([(0, i), (256, i)], fill=color)
            
            # Vẽ text "MR"
            try:
                font = ImageFont.truetype("arial.ttf", 120)
            except:
                font = ImageFont.load_default()
                
            bbox = draw.textbbox((0, 0), "MR", font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (256 - text_width) // 2
            y = (256 - text_height) // 2
            
            # Shadow
            draw.text((x + 3, y + 3), "MR", font=font, fill=(0, 0, 0, 128))
            # Main text
            draw.text((x, y), "MR", font=font, fill=(255, 255, 255, 255))
            
            # Lưu icon
            img.save(icon_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
            print(f"✅ Đã tạo icon: {icon_path}")
            
        except ImportError:
            print("⚠️ Không có PIL, sử dụng icon mặc định")
            return None
            
    return icon_path

def build_exe():
    """Build executable với PyInstaller"""
    print("🔨 Bắt đầu build executable...")
    
    # Tạo icon
    icon_path = create_icon()
    
    # Build command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Tạo single exe file
        "--windowed",                   # Không hiện console window
        "--name=MacroRecorderTool",     # Tên file exe
        "--clean",                      # Clean build
        "--noconfirm",                  # Không hỏi overwrite
    ]
    
    # Thêm icon nếu có
    if icon_path and os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])
    
    # Hidden imports để đảm bảo tất cả modules được include
    hidden_imports = [
        "tkinter",
        "tkinter.ttk", 
        "tkinter.scrolledtext",
        "pynput",
        "pynput.mouse",
        "pynput.keyboard", 
        "pyautogui",
        "PIL",
        "PIL.Image",
        "PIL.ImageGrab"
    ]
    
    for module in hidden_imports:
        cmd.extend(["--hidden-import", module])
    
    # Add data files
    cmd.extend([
        "--add-data", "requirements.txt;.",
        "--add-data", "README.md;.",
    ])
    
    # Main script
    cmd.append("gui_app.py")
    
    print(f"Chạy lệnh: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build thành công!")
        
        # Kiểm tra file đã tạo
        exe_path = os.path.join("dist", "MacroRecorderTool.exe")
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📦 File exe: {exe_path}")
            print(f"📊 Kích thước: {size_mb:.1f} MB")
            return exe_path
        else:
            print("❌ Không tìm thấy file exe")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi build: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return None

def create_installer_script():
    """Tạo script Inno Setup để build installer"""
    iss_content = '''
[Setup]
AppName=Macro Recorder Tool
AppVersion=1.0
AppVerName=Macro Recorder Tool v1.0
AppPublisher=Macro Recorder Development
DefaultDirName={autopf}\\MacroRecorderTool
DefaultGroupName=Macro Recorder Tool
UninstallDisplayIcon={app}\\MacroRecorderTool.exe
Compression=lzma2
SolidCompression=yes
OutputDir=installer
OutputBaseFilename=MacroRecorderTool_Setup
SetupIconFile=app_icon.ico
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "vietnamese"; MessagesFile: "compiler:Languages\\Vietnamese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\MacroRecorderTool.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\Macro Recorder Tool"; Filename: "{app}\\MacroRecorderTool.exe"
Name: "{group}\\{cm:UninstallProgram,Macro Recorder Tool}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\Macro Recorder Tool"; Filename: "{app}\\MacroRecorderTool.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\MacroRecorderTool.exe"; Description: "{cm:LaunchProgram,Macro Recorder Tool}"; Flags: nowait postinstall skipifsilent

[Code]
function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{#emit SetupSetting("AppId")}_is1');
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
'''
    
    with open("MacroRecorderTool.iss", "w", encoding="utf-8") as f:
        f.write(iss_content)
    
    print("✅ Đã tạo script Inno Setup: MacroRecorderTool.iss")

def main():
    """Main function"""
    print("🎯 MACRO RECORDER TOOL - BUILD EXE")
    print("=" * 50)
    
    # Kiểm tra Python version
    if sys.version_info < (3, 7):
        print("❌ Cần Python 3.7 trở lên")
        return
    
    print(f"🐍 Python version: {sys.version}")
    
    # Bước 1: Cài đặt requirements
    if not install_requirements():
        return
    
    # Bước 2: Dọn dẹp
    clean_build()
    
    # Bước 3: Build exe
    exe_path = build_exe()
    if not exe_path:
        return
    
    # Bước 4: Tạo installer script
    create_installer_script()
    
    print("\n" + "=" * 50)
    print("✅ BUILD HOÀN THÀNH!")
    print(f"📦 Executable: {exe_path}")
    print(f"📊 Size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
    print("\n📋 HƯỚNG DẪN TIẾP THEO:")
    print("1. Test exe: double-click vào dist/MacroRecorderTool.exe")
    print("2. Tạo installer: Cài Inno Setup rồi compile MacroRecorderTool.iss")
    print("3. Hoặc copy file exe để distribute trực tiếp")
    print("\n🎉 Thành công!")

if __name__ == "__main__":
    main() 