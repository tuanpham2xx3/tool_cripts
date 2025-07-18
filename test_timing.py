#!/usr/bin/env python3
"""
Test script để demo tính năng timing và smoothness mới
"""

from macro_recorder import MacroRecorder
import time
import json

def demo_timing_features():
    """Demo các tính năng timing mới"""
    print("🎯 DEMO TÍNH NĂNG TIMING & SMOOTHNESS")
    print("="*50)
    
    recorder = MacroRecorder()
    
    # Test với file macro mẫu
    print("📂 Test 1: Tải và phân tích macro mẫu...")
    if recorder.load_macro("example_macro.json"):
        print("✅ Đã tải macro thành công!")
        
        print("\n📊 Test 2: Thống kê chi tiết...")
        recorder.print_stats()
        
        print("\n⚙️ Test 3: Điều chỉnh smoothness...")
        print("Current smoothness factor:", recorder.smooth_factor)
        
        # Test với các mức smoothness khác nhau
        smoothness_levels = [0.5, 1.0, 1.5]
        for smooth in smoothness_levels:
            recorder.smooth_factor = smooth
            print(f"\n🎛️ Smoothness: {smooth}x")
            
            # Simulate một vài sự kiện để test timing
            if recorder.events and len(recorder.events) >= 3:
                print("📈 Delay analysis với smoothness", smooth)
                for i in range(min(3, len(recorder.events)-1)):
                    event = recorder.events[i]
                    next_event = recorder.events[i+1]
                    raw_delay = next_event['timestamp'] - event['timestamp']
                    smooth_delay = max(recorder.min_delay, raw_delay * smooth)
                    print(f"   Event {i+1}: {raw_delay:.3f}s → {smooth_delay:.3f}s")
        
        print("\n🛑 Test 4: Demo hotkey dừng...")
        print("   (Chạy macro và nhấn ESC để test - skip trong demo)")
        
    else:
        print("❌ Không thể tải macro mẫu!")
        print("💡 Tạo macro đơn giản để demo...")
        
        # Tạo macro demo
        demo_events = [
            {
                'type': 'mouse_click',
                'timestamp': 0.0,
                'x': 100, 'y': 100,
                'button': 'Button.left',
                'pressed': True
            },
            {
                'type': 'key_press',
                'timestamp': 0.5,
                'key': 'h'
            },
            {
                'type': 'key_press',
                'timestamp': 1.0,
                'key': 'i'
            }
        ]
        
        recorder.events = demo_events
        recorder.start_time = time.time()
        recorder.end_time = recorder.start_time + 1.0
        
        print("📝 Đã tạo macro demo với 3 sự kiện")
        print("💾 Lưu với format mới...")
        recorder.save_macro("demo_timing.json")
        
        print("📂 Tải lại để test format mới...")
        recorder.load_macro("demo_timing.json")

def demo_macro_format():
    """Demo format macro mới với thông tin timing"""
    print("\n" + "="*50)
    print("📋 DEMO FORMAT MACRO MỚI")
    print("="*50)
    
    try:
        with open("demo_timing.json", 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("🗂️ Cấu trúc file macro mới:")
        print("├── version:", data.get('version', 'N/A'))
        print("├── created_at:", data.get('created_at', 'N/A'))
        
        if 'recording_info' in data:
            info = data['recording_info']
            print("├── recording_info:")
            print(f"│   ├── total_events: {info.get('total_events', 'N/A')}")
            print(f"│   ├── actual_duration: {info.get('actual_duration', 'N/A'):.3f}s")
            print(f"│   └── events_per_second: {info.get('events_per_second', 'N/A'):.2f}")
        
        if 'timing_stats' in data:
            timing = data['timing_stats']
            print("├── timing_stats:")
            print(f"│   ├── average_delay: {timing.get('average_delay', 'N/A'):.3f}s")
            print(f"│   ├── min_delay: {timing.get('min_delay', 'N/A'):.3f}s")
            print(f"│   ├── max_delay: {timing.get('max_delay', 'N/A'):.3f}s")
            print(f"│   └── recommended_min_delay: {timing.get('recommended_min_delay', 'N/A'):.3f}s")
        
        if 'event_counts' in data:
            counts = data['event_counts']
            print("└── event_counts:")
            for event_type, count in counts.items():
                print(f"    ├── {event_type}: {count}")
        
        print(f"\n📊 Total events in file: {len(data.get('events', []))}")
        
    except Exception as e:
        print(f"❌ Lỗi đọc file: {e}")

def main():
    """Main function"""
    try:
        demo_timing_features()
        demo_macro_format()
        
        print("\n" + "="*50)
        print("✅ DEMO HOÀN THÀNH!")
        print("💡 Chạy GUI để test đầy đủ: python gui_app.py")
        print("📋 Features mới:")
        print("   • ESC để dừng phát lại")
        print("   • Smoothness slider trong GUI")
        print("   • Thông tin timing chi tiết")
        print("   • Format file mới với metadata")
        print("   • Phát lại mượt mà hơn")
        
    except KeyboardInterrupt:
        print("\n🛑 Demo bị dừng!")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main() 