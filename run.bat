@echo off
echo ========================================
echo    MACRO RECORDER TOOL
echo ========================================
echo.

REM Kiểm tra Python có tồn tại không
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python không được tìm thấy!
    echo    Vui lòng cài đặt Python từ https://python.org
    pause
    exit /b 1
)

echo ✅ Python đã được cài đặt
echo.

REM Hỏi người dùng muốn làm gì
echo Bạn muốn làm gì?
echo 1. Cài đặt thư viện và chạy GUI tool
echo 2. Chạy GUI tool (đã cài đặt thư viện)
echo 3. Chạy Console tool  
echo 4. Test GUI có hoạt động không
echo 5. Demo tính năng screenshot
echo 6. Demo tính năng timing mới
echo 7. Thoát
echo.
echo 💡 Lưu ý: Hotkey (F12, F7) tự động bật khi khởi động!
echo.
set /p choice="Chọn (1-7): "

if "%choice%"=="1" (
    echo.
    echo 📦 Đang cài đặt thư viện...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Cài đặt thất bại!
        pause
        exit /b 1
    )
    echo ✅ Cài đặt thành công!
    echo.
    echo 🚀 Đang khởi động GUI tool...
    python gui_app.py
) else if "%choice%"=="2" (
    echo.
    echo 🚀 Đang khởi động GUI tool...
    python gui_app.py
) else if "%choice%"=="3" (
    echo.
    echo 🚀 Đang khởi động Console tool...
    python main.py
) else if "%choice%"=="4" (
    echo.
    echo 🧪 Đang test GUI...
    python gui_demo.py
) else if "%choice%"=="5" (
    echo.
    echo 🎯 Đang chạy demo screenshot...
    python test_screenshot.py
) else if "%choice%"=="6" (
    echo.
    echo ⏱️ Đang chạy demo timing...
    python test_timing.py
) else if "%choice%"=="7" (
    echo.
    echo 👋 Tạm biệt!
    exit /b 0
) else (
    echo.
    echo ❌ Lựa chọn không hợp lệ!
)

echo.
pause 