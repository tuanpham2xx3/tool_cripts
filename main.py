#!/usr/bin/env python3
"""
Macro Recorder Tool - Ghi lại và phát lại hành động chuột/bàn phím
Sử dụng: python main.py
"""

import sys
import time
from macro_recorder import MacroRecorder

def print_menu():
    """In menu chính"""
    print("\n" + "="*50)
    print("🎯 MACRO RECORDER TOOL")
    print("="*50)
    print("1. 📹 Bắt đầu ghi macro")
    print("2. ⏹️  Dừng ghi macro")
    print("3. 💾 Lưu macro")
    print("4. 📂 Tải macro")
    print("5. ▶️  Phát lại macro")
    print("6. ⚡ Phát lại macro (tốc độ 2x)")
    print("7. 🐌 Phát lại macro (tốc độ 0.5x)")
    print("8. 📊 Xem thống kê macro")
    print("─" * 50)
    print("10. 🔄 Toggle hotkey chụp màn hình (F12)")
    print("11. ⌨️ Đặt nội dung auto type (F7)")
    print("12. 📸 Chụp màn hình ngay")
    print("13. 📁 Xem danh sách screenshot")
    print("14. 🗑️  Xóa screenshot cũ (>7 ngày)")
    print("15. 🔁 Phát lại macro với số lần lặp")
    print("─" * 50)
    print("9. ❓ Hướng dẫn")
    print("0. 🚪 Thoát")
    print("="*50)

def print_help():
    """In hướng dẫn sử dụng"""
    print("\n" + "="*60)
    print("📖 HƯỚNG DẪN SỬ DỤNG")
    print("="*60)
    print("🔸 Để ghi macro:")
    print("   - Chọn '1' để bắt đầu ghi")
    print("   - Thực hiện các hành động trên máy tính")
    print("   - Nhấn F9 để dừng ghi và hỏi lưu (hoặc chọn '2')")
    print("   - Chọn '3' để lưu macro vào file sau khi ghi")
    print()
    print("🔸 Để phát lại macro:")
    print("   - Chọn '4' để tải macro từ file")
    print("   - Chọn '5' để phát lại với tốc độ bình thường")
    print("   - Nhấn Ctrl+C để dừng phát lại bất cứ lúc nào")
    print()
    print("🔸 Tính năng chụp màn hình:")
    print("   - Hotkey tự động bật khi khởi động!")
    print("   - Nhấn F12 để chụp màn hình bất cứ lúc nào")
    print("   - Chọn '10' để bật/tắt hotkey chụp màn hình")
    print("   - Chọn '12' để chụp màn hình ngay lập tức")
    print("   - Screenshot được lưu trong folder SCREENSHOT/")
    print("   - Chọn '13' để xem danh sách screenshot đã chụp")
    print("   - Chọn '14' để xóa screenshot cũ")
    print()
    print("🔸 Tính năng mới:")
    print("   - F7: Auto gõ nội dung đã đặt trước")
    print("   - F12: Hotkey chụp màn hình tự động bật!")
    print("   - Có thể lặp lại macro nhiều lần liên tiếp")
    print("   - F9: Dừng ghi và hỏi có lưu không")
    print()
    print("🔸 Lưu ý quan trọng:")
    print("   - Đảm bảo màn hình ở vị trí tương tự khi phát lại")
    print("   - Tool ghi lại tọa độ tuyệt đối của chuột")
    print("   - Không di chuyển cửa sổ giữa việc ghi và phát lại")
    print("   - File macro được lưu dưới định dạng JSON")
    print("   - Screenshot được lưu với format: screenshot_YYYYMMDD_HHMMSS.png")
    print("="*60)

def handle_f9_save_prompt(recorder):
    """Xử lý F9 với prompt lưu file"""
    recorder.stop_recording()
    print("\n✅ Đã dừng ghi macro!")
    
    if recorder.events:
        while True:
            try:
                save_choice = input("💾 Bạn có muốn lưu macro này không? (y/n): ").strip().lower()
                if save_choice in ['y', 'yes', 'có']:
                    filename = input("📝 Tên file để lưu (Enter = tự động): ").strip()
                    if not filename:
                        filename = f"macro_{int(time.time())}"
                    if not filename.endswith('.json'):
                        filename += '.json'
                    recorder.save_macro(filename)
                    break
                elif save_choice in ['n', 'no', 'không']:
                    print("❌ Không lưu macro.")
                    break
                else:
                    print("❓ Vui lòng nhập 'y' (có) hoặc 'n' (không)")
            except:
                break

def main():
    """Hàm main"""
    recorder = MacroRecorder()
    
    # Đặt callback cho F9
    recorder.set_f9_callback(lambda: handle_f9_save_prompt(recorder))
    
    print("🚀 Khởi động Macro Recorder Tool...")
    print("⚠️  Lưu ý: Tool này yêu cầu quyền truy cập chuột và bàn phím")
    
    # Auto-enable hotkeys on startup
    print("🔥 Tự động bật hotkey...")
    try:
        recorder.start_screenshot_hotkey()
        print("✅ Hotkey đã được bật! (F12: chụp, F7: gõ)")
    except Exception as e:
        print(f"⚠️ Không thể bật hotkey: {e}")
    
    time.sleep(1)
    
    while True:
        try:
            print_menu()
            choice = input("👉 Chọn chức năng (0-15): ").strip()
            
            if choice == '1':
                print("\n🎬 Chuẩn bị ghi macro...")
                print("⏳ Bạn có 3 giây để chuẩn bị...")
                for i in range(3, 0, -1):
                    print(f"   {i}...")
                    time.sleep(1)
                recorder.start_recording()
                print("✅ Đã bắt đầu ghi! Nhấn F9 để dừng.")
                
            elif choice == '2':
                recorder.stop_recording()
                print("✅ Đã dừng ghi macro!")
                
            elif choice == '3':
                filename = input("📝 Tên file để lưu (không cần .json): ").strip()
                if not filename:
                    filename = f"macro_{int(time.time())}"
                if not filename.endswith('.json'):
                    filename += '.json'
                recorder.save_macro(filename)
                
            elif choice == '4':
                filename = input("📂 Tên file để tải (không cần .json): ").strip()
                if not filename:
                    print("❌ Vui lòng nhập tên file!")
                    continue
                if not filename.endswith('.json'):
                    filename += '.json'
                recorder.load_macro(filename)
                
            elif choice == '5':
                print("▶️  Phát lại macro với tốc độ bình thường...")
                print("⏳ Bạn có 3 giây để chuẩn bị...")
                for i in range(3, 0, -1):
                    print(f"   {i}...")
                    time.sleep(1)
                recorder.replay_macro(1.0)
                
            elif choice == '6':
                print("⚡ Phát lại macro với tốc độ 2x...")
                print("⏳ Bạn có 3 giây để chuẩn bị...")
                for i in range(3, 0, -1):
                    print(f"   {i}...")
                    time.sleep(1)
                recorder.replay_macro(2.0)
                
            elif choice == '7':
                print("🐌 Phát lại macro với tốc độ 0.5x...")
                print("⏳ Bạn có 3 giây để chuẩn bị...")
                for i in range(3, 0, -1):
                    print(f"   {i}...")
                    time.sleep(1)
                recorder.replay_macro(0.5)
                
            elif choice == '8':
                recorder.print_stats()
                
            elif choice == '10':
                # Toggle hotkey status
                if recorder.screenshot_enabled:
                    recorder.stop_screenshot_hotkey()
                    print("🛑 Đã tắt hotkey chụp màn hình!")
                else:
                    recorder.start_screenshot_hotkey()
                    print("🔥 Đã bật hotkey chụp màn hình!")
                
            elif choice == '11':
                content = input("⌨️ Nhập nội dung để gõ khi nhấn F7: ").strip()
                if content:
                    recorder.set_type_content(content)
                else:
                    print("❌ Chưa nhập nội dung!")
                
            elif choice == '12':
                print("📸 Đang chụp màn hình...")
                screenshot_path = recorder.take_screenshot()
                if screenshot_path:
                    print(f"✅ Screenshot đã được lưu!")
                
            elif choice == '13':
                recorder.list_screenshots()
                
            elif choice == '14':
                days = input("🗑️  Xóa screenshot cũ hơn bao nhiêu ngày? (mặc định 7): ").strip()
                try:
                    days = int(days) if days else 7
                    if days < 1:
                        print("❌ Số ngày phải >= 1!")
                        continue
                    print(f"🗑️  Đang xóa screenshot cũ hơn {days} ngày...")
                    recorder.cleanup_old_screenshots(days)
                except ValueError:
                    print("❌ Vui lòng nhập số ngày hợp lệ!")
            
            elif choice == '15':
                # Get speed
                speed_input = input("⚡ Tốc độ phát lại (0.5, 1.0, 2.0) [mặc định 1.0]: ").strip()
                try:
                    speed = float(speed_input) if speed_input else 1.0
                    if speed <= 0:
                        print("❌ Tốc độ phải > 0!")
                        continue
                except ValueError:
                    print("❌ Tốc độ không hợp lệ!")
                    continue
                    
                # Get repeat count
                repeat_input = input("🔁 Số lần lặp lại [mặc định 1]: ").strip()
                try:
                    repeat_count = int(repeat_input) if repeat_input else 1
                    if repeat_count < 1:
                        print("❌ Số lần lặp phải >= 1!")
                        continue
                except ValueError:
                    print("❌ Số lần lặp không hợp lệ!")
                    continue
                
                print(f"▶️ Phát lại macro với tốc độ {speed}x × {repeat_count} lần...")
                print("⏳ Bạn có 3 giây để chuẩn bị...")
                for i in range(3, 0, -1):
                    print(f"   {i}...")
                    time.sleep(1)
                recorder.replay_macro(speed, True, repeat_count)
                
            elif choice == '9':
                print_help()
                
            elif choice == '0':
                print("👋 Cảm ơn bạn đã sử dụng Macro Recorder Tool!")
                recorder.stop_screenshot_hotkey()  # Tắt hotkey trước khi thoát
                sys.exit(0)
                
            else:
                print("❌ Lựa chọn không hợp lệ! Vui lòng chọn từ 0-15.")
                
        except KeyboardInterrupt:
            print("\n\n🛑 Đã nhận Ctrl+C. Dừng tool...")
            recorder.stop_recording()
            recorder.stop_screenshot_hotkey()
            sys.exit(0)
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            print("🔄 Tool sẽ tiếp tục hoạt động...")

if __name__ == "__main__":
    main() 