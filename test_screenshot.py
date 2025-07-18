#!/usr/bin/env python3
"""
Test script để demo tính năng screenshot
"""

from macro_recorder import MacroRecorder
import time

def demo_screenshot():
    """Demo tính năng chụp màn hình"""
    print("🎯 DEMO TÍNH NĂNG SCREENSHOT")
    print("="*40)
    
    # Tạo recorder instance
    recorder = MacroRecorder()
    
    print("📸 Test 1: Chụp màn hình ngay lập tức")
    screenshot_path = recorder.take_screenshot()
    if screenshot_path:
        print(f"✅ Đã chụp thành công: {screenshot_path}")
    else:
        print("❌ Chụp màn hình thất bại!")
    
    print("\n📸 Test 2: Bật hotkey và demo trong 10 giây")
    print("   - Nhấn F12 để chụp màn hình")
    
    recorder.start_screenshot_hotkey()
    
    # Đợi 10 giây
    for i in range(10, 0, -1):
        print(f"   ⏰ Còn {i} giây... (F12: chụp)")
        time.sleep(1)
    
    recorder.stop_screenshot_hotkey()
    print("✅ Đã tắt hotkey!")
    
    print("\n📁 Test 3: Xem danh sách screenshot")
    recorder.list_screenshots()
    
    print("\n✅ Demo hoàn thành!")
    print("💡 Để sử dụng đầy đủ, chạy: python main.py")

if __name__ == "__main__":
    try:
        demo_screenshot()
    except KeyboardInterrupt:
        print("\n🛑 Demo bị dừng!")
    except Exception as e:
        print(f"❌ Lỗi: {e}") 