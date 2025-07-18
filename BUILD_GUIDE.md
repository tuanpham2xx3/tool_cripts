# 📦 HƯỚNG DẪN BUILD EXE - MACRO RECORDER TOOL

Hướng dẫn chi tiết để đóng gói Macro Recorder Tool thành file `.exe` và tạo installer cho Windows.

## 🚀 Quick Start (Cách nhanh nhất)

### Windows - Chỉ cần 1 click:
```batch
# Click đúp vào file này:
build_exe.bat
```

### Manual - Chạy Python script:
```bash
python build_exe.py
```

## 📋 Yêu cầu hệ thống

### Cần thiết:
- **Python 3.7+** (khuyên dùng 3.9+)
- **Windows 10/11** (để build exe cho Windows)
- **Internet connection** (để download PyInstaller)

### Tùy chọn (cho installer):
- **Inno Setup 6** (free): https://jrsoftware.org/isdl.php

## 🔧 Quá trình Build

### Bước 1: Chuẩn bị
```bash
# Kiểm tra Python
python --version

# Kiểm tra các file cần thiết
dir /b *.py *.txt *.md
```

### Bước 2: Build EXE
```bash
# Cách 1: Sử dụng batch file (Windows)
build_exe.bat

# Cách 2: Chạy Python script trực tiếp  
python build_exe.py

# Cách 3: Manual PyInstaller
pip install pyinstaller
pyinstaller --onefile --windowed --name=MacroRecorderTool gui_app.py
```

### Bước 3: Test EXE
```bash
# File sẽ ở trong folder dist/
dist\MacroRecorderTool.exe
```

## 📊 Kết quả Build

### File EXE:
- **Vị trí**: `dist/MacroRecorderTool.exe`
- **Kích thước**: ~25-40 MB
- **Loại**: Standalone (không cần cài Python)

### Tự động tạo:
- ✅ Icon cho app (app_icon.ico)
- ✅ Hidden imports cho tất cả dependencies
- ✅ Embedded data files (README, requirements)
- ✅ Windows compatibility

## 🎨 Tùy chỉnh Build

### Build options trong `build_exe.py`:

```python
# Build types
--onefile          # Single exe file (~40MB)
--onedir          # Folder với exe + libs (~100MB+)
--windowed        # Không hiện console
--console         # Hiện console để debug

# Optimization
--exclude-module  # Loại bỏ modules không cần
--upx-dir        # Compress với UPX (giảm size)
```

### Custom icon:
1. Tạo file `app_icon.ico` (256x256)
2. Đặt cùng folder với `build_exe.py`
3. Build sẽ tự động sử dụng

## 📦 Tạo Installer (Windows)

### Option 1: Sử dụng script có sẵn
```bash
# Build script sẽ tự động tạo MacroRecorderTool.iss
# Sau đó:
1. Cài Inno Setup: https://jrsoftware.org/isdl.php
2. Mở MacroRecorderTool.iss
3. Click Build > Compile
4. Installer sẽ ở folder installer/
```

### Option 2: Manual Inno Setup
```inno
[Setup]
AppName=Macro Recorder Tool
AppVersion=1.0
DefaultDirName={autopf}\MacroRecorderTool
OutputBaseFilename=MacroRecorderTool_Setup

[Files]
Source: "dist\MacroRecorderTool.exe"; DestDir: "{app}"

[Icons]
Name: "{group}\Macro Recorder Tool"; Filename: "{app}\MacroRecorderTool.exe"
```

## 🐛 Troubleshooting

### Lỗi thường gặp:

#### 1. "ModuleNotFoundError" khi chạy exe:
```bash
# Thêm hidden import trong build_exe.py:
--hidden-import tkinter.ttk
--hidden-import pynput.mouse
```

#### 2. Exe quá chậm khởi động:
```bash
# Sử dụng --onedir thay vì --onefile
# Hoặc exclude các modules không cần:
--exclude-module matplotlib
```

#### 3. Antivirus block exe:
```bash
# Add exception cho folder dist/
# Hoặc upload lên VirusTotal để verify
```

#### 4. Icon không hiện:
```bash
# Đảm bảo app_icon.ico có format đúng
# Hoặc sử dụng online converter: ICO format
```

### Debug build:
```bash
# Build với console để thấy errors:
pyinstaller --onefile --console --name=MacroRecorderTool_Debug gui_app.py
```

## 📈 Optimization Tips

### Giảm size exe:
1. **Exclude unused modules**:
   ```python
   --exclude-module matplotlib
   --exclude-module numpy
   ```

2. **UPX compression**:
   ```bash
   # Download UPX, add to PATH
   --upx-dir C:\upx
   ```

3. **One-dir build** (nhanh hơn):
   ```python
   --onedir  # Thay vì --onefile
   ```

### Tăng performance:
1. **Optimize imports** trong code
2. **Lazy loading** cho heavy modules
3. **Cache compiled** `.pyc` files

## 🚀 Distribution

### Phân phối EXE file:
```
✅ Single file: MacroRecorderTool.exe (~25-40MB)
✅ No installation required
✅ Run anywhere on Windows
✅ No Python dependency
```

### Phân phối Installer:
```
✅ Professional installer experience
✅ Start menu shortcuts
✅ Desktop icon (optional)
✅ Uninstaller included
✅ Auto-upgrade capability
```

## 📂 File Structure sau Build

```
project/
├── dist/
│   └── MacroRecorderTool.exe     # Main executable
├── build/                        # Temp build files
├── installer/
│   └── MacroRecorderTool_Setup.exe  # Installer
├── app_icon.ico                  # App icon
├── MacroRecorderTool.iss         # Inno Setup script
├── MacroRecorderTool.spec        # PyInstaller spec
└── build_exe.py                  # Build script
```

## ✅ Checklist trước khi distribute

- [ ] Test exe trên máy sạch (không có Python)
- [ ] Test tất cả features hoạt động
- [ ] Kiểm tra file size hợp lý
- [ ] Scan antivirus
- [ ] Test installer (nếu có)
- [ ] Verify icon và metadata
- [ ] Test trên Windows versions khác nhau

## 🎯 Production Build Command

```bash
# Build production-ready exe:
python build_exe.py

# Kết quả:
# ✅ MacroRecorderTool.exe (ready to distribute)
# ✅ MacroRecorderTool_Setup.exe (installer)
# ✅ Professional appearance
# ✅ All features working
```

## 📞 Support

Nếu gặp vấn đề:
1. Kiểm tra Python version >= 3.7
2. Ensure all dependencies trong requirements.txt
3. Test script gui_app.py trước khi build
4. Check build logs để tìm errors
5. Try clean build (xóa build/, dist/)

---

**🎉 Chúc build thành công!** 