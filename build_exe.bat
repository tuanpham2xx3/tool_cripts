@echo off
echo ========================================
echo    MACRO RECORDER TOOL - BUILD EXE
echo ========================================
echo.

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python khong duoc tim thay!
    echo    Vui long cai dat Python tu https://python.org
    pause
    exit /b 1
)

echo ✅ Python da duoc cai dat
echo.

REM Hoi user muon lam gi
echo Ban muon lam gi?
echo 1. Build EXE file (khuyen dung)
echo 2. Build EXE + tao Installer
echo 3. Chi tao script Installer
echo 4. Clean build files
echo 5. Test EXE da build
echo 6. Thoat
echo.
set /p choice="Chon (1-6): "

if "%choice%"=="1" (
    echo.
    echo 🔨 Dang build EXE file...
    python build_exe.py
    goto end
) else if "%choice%"=="2" (
    echo.
    echo 🔨 Dang build EXE + Installer...
    python build_exe.py
    echo.
    echo 📦 De tao installer, can cai Inno Setup:
    echo    1. Download tu: https://jrsoftware.org/isdl.php
    echo    2. Cai dat Inno Setup
    echo    3. Mo file MacroRecorderTool.iss
    echo    4. Click Build ^> Compile
    echo.
    echo ✅ Hoac chay lenh sau neu da cai Inno Setup:
    echo    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" MacroRecorderTool.iss
    goto end
) else if "%choice%"=="3" (
    echo.
    echo 📝 Chi tao script installer...
    python -c "from build_exe import create_installer_script; create_installer_script()"
    echo ✅ Da tao MacroRecorderTool.iss
    goto end
) else if "%choice%"=="4" (
    echo.
    echo 🧹 Dang don dep build files...
    if exist build rmdir /s /q build
    if exist dist rmdir /s /q dist
    if exist installer rmdir /s /q installer
    if exist __pycache__ rmdir /s /q __pycache__
    del /q *.spec 2>nul
    del /q app_icon.ico 2>nul
    echo ✅ Da don dep xong
    goto end
) else if "%choice%"=="5" (
    echo.
    if exist "dist\MacroRecorderTool.exe" (
        echo 🚀 Dang chay EXE file...
        start "" "dist\MacroRecorderTool.exe"
    ) else (
        echo ❌ Khong tim thay file EXE!
        echo    Hay build truoc bang cach chon option 1
    )
    goto end
) else if "%choice%"=="6" (
    echo.
    echo 👋 Tam biet!
    exit /b 0
) else (
    echo.
    echo ❌ Lua chon khong hop le!
    goto end
)

:end
echo.
pause 