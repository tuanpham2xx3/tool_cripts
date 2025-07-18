#!/usr/bin/env python3
"""
Script cài đặt và chạy Macro Recorder Tool
"""

import subprocess
import sys
import os

def install_requirements():
    """Cài đặt các thư viện cần thiết"""
    print("🔧 Đang cài đặt thư viện cần thiết...")
    
    required_packages = [
        'pynput==1.7.6',
        'pyautogui==0.9.54', 
        'keyboard==0.13.5',
        'pillow==10.0.1'
    ]
    
    for package in required_packages:
        try:
            print(f"📦 Cài đặt {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ Đã cài đặt {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Lỗi cài đặt {package}: {e}")
            return False
    
    return True

def check_python_version():
    """Kiểm tra phiên bản Python"""
    if sys.version_info < (3, 7):
        print("❌ Tool yêu cầu Python 3.7 trở lên!")
        print(f"   Phiên bản hiện tại: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version}")
    return True

def check_permissions():
    """Kiểm tra quyền truy cập"""
    print("⚠️  Lưu ý về quyền truy cập:")
    
    if sys.platform == "win32":
        print("   - Windows: Tool cần quyền truy cập chuột/bàn phím")
        print("   - Nếu gặp lỗi, hãy chạy với quyền Administrator")
    elif sys.platform == "darwin":
        print("   - macOS: Cần cấp quyền Accessibility")
        print("   - Vào System Preferences > Security & Privacy > Accessibility")
        print("   - Thêm Terminal hoặc Python vào danh sách cho phép")
    else:
        print("   - Linux: Có thể cần chạy với sudo")

def main():
    """Hàm main"""
    print("🚀 MACRO RECORDER TOOL - SETUP & RUN")
    print("="*50)
    
    # Kiểm tra phiên bản Python
    if not check_python_version():
        return
    
    # Kiểm tra quyền truy cập
    check_permissions()
    
    # Hỏi người dùng có muốn cài đặt không
    install = input("\n📥 Bạn có muốn cài đặt thư viện cần thiết? (y/n): ").lower().strip()
    
    if install in ['y', 'yes', 'có']:
        if not install_requirements():
            print("❌ Cài đặt thất bại!")
            return
        print("\n✅ Cài đặt hoàn tất!")
    else:
        print("⏭️  Bỏ qua cài đặt thư viện")
    
    # Hỏi có muốn chạy luôn không
    run = input("\n🎯 Bạn có muốn chạy tool ngay bây giờ? (y/n): ").lower().strip()
    
    if run in ['y', 'yes', 'có']:
        print("\n🏃 Đang khởi động Macro Recorder Tool...")
        try:
            if os.path.exists('main.py'):
                os.system('python main.py')
            else:
                print("❌ Không tìm thấy main.py!")
        except Exception as e:
            print(f"❌ Lỗi khởi động: {e}")
    else:
        print("\n👋 Để chạy tool, sử dụng lệnh: python main.py")

if __name__ == "__main__":
    main() 