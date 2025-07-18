import json
import time
import threading
import os
from datetime import datetime
from pynput import mouse, keyboard
from pynput.mouse import Button, Listener as MouseListener
from pynput.keyboard import Key, Listener as KeyboardListener
import pyautogui

class MacroRecorder:
    def __init__(self):
        self.recording = False
        self.replaying = False
        self.events = []
        self.start_time = None
        self.end_time = None
        self.mouse_listener = None
        self.keyboard_listener = None
        self.screenshot_listener = None
        self.replay_listener = None
        self.screenshot_enabled = False
        
        # Screenshot folder
        self.screenshot_folder = "SCREENSHOT"
        self.create_screenshot_folder()
        
        # Replay settings
        self.min_delay = 0.01  # Minimum delay between events (10ms)
        self.smooth_factor = 1.0  # Smoothness factor for delays
        
        # Callback for when F9 is pressed (for save prompt)
        self.on_f9_callback = None
        
        # Auto type content for F7
        self.type_content = ""
        
        # Modifier key tracking for proper key combinations
        self._ctrl_pressed = False
        self._shift_pressed = False
        self._alt_pressed = False
        
        # Disable pyautogui fail-safe (optional, be careful!)
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.01  # Reduce default pause for smoother playback
    
    def set_f9_callback(self, callback):
        """Đặt callback khi nhấn F9"""
        self.on_f9_callback = callback
    
    def set_type_content(self, content):
        """Đặt nội dung để gõ khi nhấn F7"""
        self.type_content = content
        print(f"📝 Đã đặt nội dung gõ: '{content[:50]}{'...' if len(content) > 50 else ''}'")
    
    def auto_type(self):
        """Tự động gõ nội dung đã đặt"""
        if not self.type_content:
            print("❌ Chưa có nội dung để gõ! Hãy đặt nội dung trước.")
            return
            
        try:
            # Sử dụng pyautogui để gõ text
            pyautogui.typewrite(self.type_content)
            print(f"✅ Đã gõ: '{self.type_content[:50]}{'...' if len(self.type_content) > 50 else ''}'")
        except Exception as e:
            print(f"❌ Lỗi khi gõ: {e}")
    
    def start_recording(self):
        """Bắt đầu ghi lại các hành động"""
        if self.recording:
            print("Đang trong quá trình ghi!")
            return
            
        print("Bắt đầu ghi lại hành động...")
        print("Nhấn F9 để dừng ghi")
        
        self.recording = True
        self.events = []
        self.start_time = time.time()
        
        # Tạo listeners cho mouse và keyboard
        self.mouse_listener = MouseListener(
            on_move=self.on_mouse_move,
            on_click=self.on_mouse_click,
            on_scroll=self.on_mouse_scroll
        )
        
        self.keyboard_listener = KeyboardListener(
            on_press=self.on_key_press,
            on_release=self.on_key_release
        )
        
        # Bắt đầu lắng nghe
        self.mouse_listener.start()
        self.keyboard_listener.start()
    
    def stop_recording(self):
        """Dừng ghi lại"""
        if not self.recording:
            return
            
        print("Dừng ghi lại!")
        self.recording = False
        self.end_time = time.time()
        
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            
        # Print recording summary
        if self.events and self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            print(f"📊 Tóm tắt bản ghi:")
            print(f"   ⏱️  Thời lượng: {duration:.2f} giây")
            print(f"   📝 Sự kiện: {len(self.events)}")
            print(f"   📈 Tần suất: {len(self.events)/duration:.1f} sự kiện/giây")
    
    def on_mouse_move(self, x, y):
        """Ghi lại di chuyển chuột"""
        if self.recording and self.start_time is not None:
            timestamp = time.time() - self.start_time
            self.events.append({
                'type': 'mouse_move',
                'timestamp': timestamp,
                'x': x,
                'y': y
            })
    
    def on_mouse_click(self, x, y, button, pressed):
        """Ghi lại click chuột"""
        if self.recording and self.start_time is not None:
            timestamp = time.time() - self.start_time
            self.events.append({
                'type': 'mouse_click',
                'timestamp': timestamp,
                'x': x,
                'y': y,
                'button': str(button),
                'pressed': pressed
            })
            print(f"Click {'press' if pressed else 'release'}: {button} tại ({x}, {y})")
    
    def on_mouse_scroll(self, x, y, dx, dy):
        """Ghi lại cuộn chuột"""
        if self.recording and self.start_time is not None:
            timestamp = time.time() - self.start_time
            self.events.append({
                'type': 'mouse_scroll',
                'timestamp': timestamp,
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy
            })
    
    def on_key_press(self, key):
        """Ghi lại nhấn phím"""
        if self.recording and self.start_time is not None:
            # Dừng ghi khi nhấn F9
            if key == keyboard.Key.f9:
                if self.on_f9_callback:
                    self.on_f9_callback()
                else:
                    self.stop_recording()
                return
                
            timestamp = time.time() - self.start_time
            try:
                key_char = key.char
            except AttributeError:
                key_char = str(key)
                
            self.events.append({
                'type': 'key_press',
                'timestamp': timestamp,
                'key': key_char
            })
            print(f"Key press: {key_char}")
    
    def on_key_release(self, key):
        """Ghi lại thả phím"""
        if self.recording and self.start_time is not None:
            timestamp = time.time() - self.start_time
            try:
                key_char = key.char
            except AttributeError:
                key_char = str(key)
                
            self.events.append({
                'type': 'key_release',
                'timestamp': timestamp,
                'key': key_char
            })
    
    def save_macro(self, filename):
        """Lưu macro vào file"""
        if not self.events:
            print("Không có sự kiện nào để lưu!")
            return
            
        # Calculate timing statistics
        duration = self.events[-1]['timestamp'] if self.events else 0
        actual_duration = (self.end_time - self.start_time) if (self.end_time and self.start_time) else duration
        
        # Calculate delays between events
        delays = []
        for i in range(1, len(self.events)):
            delay = self.events[i]['timestamp'] - self.events[i-1]['timestamp']
            delays.append(delay)
        
        avg_delay = sum(delays) / len(delays) if delays else 0
        min_delay = min(delays) if delays else 0
        max_delay = max(delays) if delays else 0
        
        # Count event types
        event_counts = {}
        for event in self.events:
            event_type = event['type']
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        data = {
            'created_at': datetime.now().isoformat(),
            'version': '2.0',
            'recording_info': {
                'start_time': self.start_time,
                'end_time': self.end_time,
                'actual_duration': actual_duration,
                'event_duration': duration,
                'total_events': len(self.events),
                'events_per_second': len(self.events) / actual_duration if actual_duration > 0 else 0
            },
            'timing_stats': {
                'average_delay': avg_delay,
                'min_delay': min_delay,
                'max_delay': max_delay,
                'smooth_factor': self.smooth_factor,
                'recommended_min_delay': max(self.min_delay, avg_delay * 0.1)
            },
            'event_counts': event_counts,
            'events': self.events
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Đã lưu {len(self.events)} sự kiện vào {filename}")
        print(f"📊 Thống kê:")
        print(f"   ⏱️  Thời lượng thực: {actual_duration:.2f}s")
        print(f"   📈 Delay trung bình: {avg_delay:.3f}s")
        print(f"   ⚡ Delay tối thiểu: {min_delay:.3f}s")
        print(f"   🐌 Delay tối đa: {max_delay:.3f}s")
    
    def load_macro(self, filename):
        """Tải macro từ file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.events = data['events']
            
            # Handle both old and new format
            if 'version' in data and data['version'] == '2.0':
                # New format with detailed info
                recording_info = data.get('recording_info', {})
                timing_stats = data.get('timing_stats', {})
                event_counts = data.get('event_counts', {})
                
                print(f"📂 Đã tải macro: {filename}")
                print(f"📊 Thông tin bản ghi:")
                print(f"   📝 Sự kiện: {len(self.events)}")
                print(f"   ⏱️  Thời lượng: {recording_info.get('actual_duration', 0):.2f}s")
                print(f"   📈 Tần suất: {recording_info.get('events_per_second', 0):.1f} sự kiện/giây")
                print(f"   📊 Delay TB: {timing_stats.get('average_delay', 0):.3f}s")
                
                # Load timing settings
                if timing_stats:
                    self.smooth_factor = timing_stats.get('smooth_factor', 1.0)
                    recommended_delay = timing_stats.get('recommended_min_delay', self.min_delay)
                    print(f"   💡 Delay đề xuất: {recommended_delay:.3f}s")
                
                # Show event breakdown
                if event_counts:
                    print(f"   🔍 Phân tích:")
                    for event_type, count in event_counts.items():
                        print(f"      {event_type}: {count}")
                        
            else:
                # Old format - backward compatibility
                duration = data.get('duration', 0)
                print(f"📂 Đã tải macro (format cũ): {filename}")
                print(f"   📝 Sự kiện: {len(self.events)}")
                print(f"   ⏱️  Thời lượng: {duration:.2f}s")
                
            return True
            
        except FileNotFoundError:
            print(f"❌ Không tìm thấy file: {filename}")
            return False
        except Exception as e:
            print(f"❌ Lỗi khi tải file: {e}")
            return False
    
    def replay_macro(self, speed_multiplier=1.0, enable_hotkey_stop=True, repeat_count=1):
        """Phát lại macro với khả năng dừng bằng hotkey và lặp lại"""
        if not self.events:
            print("❌ Không có macro nào để phát!")
            return False
        
        if self.replaying:
            print("⚠️ Đang phát lại macro khác!")
            return False
        
        print(f"▶️ Bắt đầu phát lại macro với {len(self.events)} sự kiện...")
        print(f"⚡ Tốc độ: {speed_multiplier}x")
        print(f"🔁 Số lần lặp: {repeat_count}")
        if enable_hotkey_stop:
            print("🛑 Nhấn ESC để dừng phát lại")
        print("⏸️  Nhấn Ctrl+C để dừng")
        
        self.replaying = True
        
        # Reset modifier key states
        self._ctrl_pressed = False
        self._shift_pressed = False
        self._alt_pressed = False
        
        # Setup hotkey listener for stopping
        if enable_hotkey_stop:
            self.replay_listener = KeyboardListener(on_press=self.on_replay_key_press)
            self.replay_listener.start()
        
        try:
            total_completed_events = 0
            
            # Repeat loop
            for repeat_num in range(repeat_count):
                if not self.replaying:
                    break
                    
                if repeat_count > 1:
                    print(f"🔄 Lần lặp {repeat_num + 1}/{repeat_count}")
                    
                last_timestamp = 0
                completed_events = 0
                
                for i, event in enumerate(self.events):
                    # Check if should stop
                    if not self.replaying:
                        print("🛑 Phát lại đã bị dừng!")
                        break
                    
                    # Calculate wait time with smoothing
                    raw_wait_time = (event['timestamp'] - last_timestamp) / speed_multiplier
                    # Apply minimum delay and smoothing
                    wait_time = max(self.min_delay, raw_wait_time * self.smooth_factor)
                    
                    if wait_time > 0:
                        time.sleep(wait_time)
                    
                    # Check again after sleep
                    if not self.replaying:
                        print("🛑 Phát lại đã bị dừng!")
                        break
                    
                    # Execute event
                    success = self.execute_event(event)
                    if success:
                        completed_events += 1
                        
                    last_timestamp = event['timestamp']
                    
                    # Progress feedback for long macros
                    if len(self.events) > 100 and (i + 1) % 50 == 0:
                        progress = (i + 1) / len(self.events) * 100
                        print(f"📈 Tiến độ: {progress:.1f}% ({i + 1}/{len(self.events)})")
                
                total_completed_events += completed_events
                
                # Break if stopped mid-execution
                if not self.replaying:
                    break
                    
                # Delay between repeats (6 seconds with countdown)
                if repeat_num < repeat_count - 1 and self.replaying:
                    print(f"⏸️  Nghỉ giữa các lần lặp...")
                    for i in range(6, 0, -1):
                        if not self.replaying:  # Check if stopped during pause
                            break
                        print(f"   ⏰ Còn {i} giây đến lần lặp tiếp theo...")
                        time.sleep(1)
            
            if self.replaying:  # Completed normally
                print("✅ Hoàn thành phát lại macro!")
                print(f"📊 Tổng sự kiện: {total_completed_events}/{len(self.events) * repeat_count}")
                return True
            else:
                print(f"⏹️ Phát lại bị dừng. Đã thực hiện: {total_completed_events} sự kiện")
                return False
            
        except KeyboardInterrupt:
            print("⏸️ Đã dừng phát lại macro (Ctrl+C)!")
            return False
        except Exception as e:
            print(f"❌ Lỗi khi phát lại: {e}")
            return False
        finally:
            self.replaying = False
            if self.replay_listener:
                self.replay_listener.stop()
                self.replay_listener = None
    
    def on_replay_key_press(self, key):
        """Xử lý phím bấm khi đang phát lại macro"""
        try:
            # ESC để dừng phát lại
            if key == keyboard.Key.esc:
                print("🛑 Nhận lệnh dừng (ESC)...")
                self.stop_replay()
        except Exception as e:
            print(f"❌ Lỗi xử lý hotkey phát lại: {e}")
    
    def stop_replay(self):
        """Dừng phát lại macro"""
        if self.replaying:
            self.replaying = False
            print("⏹️ Đang dừng phát lại...")
    
    def execute_event(self, event):
        """Thực hiện một sự kiện"""
        try:
            if event['type'] == 'mouse_move':
                pyautogui.moveTo(event['x'], event['y'])
                
            elif event['type'] == 'mouse_click':
                if event['pressed']:
                    button = 'left' if 'left' in event['button'].lower() else 'right'
                    pyautogui.click(event['x'], event['y'], button=button)
                    
            elif event['type'] == 'mouse_scroll':
                pyautogui.scroll(event['dy'], x=event['x'], y=event['y'])
                
            elif event['type'] == 'key_press':
                key = event['key']
                
                # Skip paste operations to avoid duplicate paste
                # Ctrl+V paste sẽ được xử lý ở key_release
                if key == 'v' and hasattr(self, '_ctrl_pressed') and self._ctrl_pressed:
                    return True
                    
                if key and key.startswith('Key.'):
                    # Track modifier keys
                    if key in ['Key.ctrl_l', 'Key.ctrl_r']:
                        self._ctrl_pressed = True
                        return True
                    elif key in ['Key.shift', 'Key.shift_l', 'Key.shift_r']:
                        self._shift_pressed = True
                        return True
                    elif key in ['Key.alt_l', 'Key.alt_r']:
                        self._alt_pressed = True
                        return True
                    
                    # Xử lý các phím đặc biệt khác
                    special_keys = {
                        'Key.space': 'space',
                        'Key.enter': 'enter',
                        'Key.tab': 'tab',
                        'Key.backspace': 'backspace',
                        'Key.delete': 'delete',
                        'Key.esc': 'esc'
                    }
                    mapped_key = special_keys.get(key, key.replace('Key.', ''))
                    if mapped_key:
                        pyautogui.press(mapped_key)
                elif key:
                    # Regular character keys
                    # Check for Ctrl combinations
                    ctrl_pressed = getattr(self, '_ctrl_pressed', False)
                    shift_pressed = getattr(self, '_shift_pressed', False)
                    alt_pressed = getattr(self, '_alt_pressed', False)
                    
                    if ctrl_pressed and key == 'v':
                        # This is Ctrl+V - use pyautogui's hotkey for proper paste
                        pyautogui.hotkey('ctrl', 'v')
                    elif ctrl_pressed and key == 'c':
                        # This is Ctrl+C
                        pyautogui.hotkey('ctrl', 'c')
                    elif ctrl_pressed and key == 'x':
                        # This is Ctrl+X
                        pyautogui.hotkey('ctrl', 'x')
                    elif ctrl_pressed and key == 'a':
                        # This is Ctrl+A
                        pyautogui.hotkey('ctrl', 'a')
                    elif ctrl_pressed and key == 'z':
                        # This is Ctrl+Z
                        pyautogui.hotkey('ctrl', 'z')
                    elif ctrl_pressed and key == 'y':
                        # This is Ctrl+Y
                        pyautogui.hotkey('ctrl', 'y')
                    elif shift_pressed:
                        # Handle shifted characters
                        pyautogui.hotkey('shift', key)
                    elif alt_pressed:
                        # Handle alt combinations
                        pyautogui.hotkey('alt', key)
                    else:
                        # Regular key press
                        pyautogui.press(key)
            
            elif event['type'] == 'key_release':
                key = event['key']
                
                # Track modifier key releases
                if key in ['Key.ctrl_l', 'Key.ctrl_r']:
                    self._ctrl_pressed = False
                elif key in ['Key.shift', 'Key.shift_l', 'Key.shift_r']:
                    self._shift_pressed = False
                elif key in ['Key.alt_l', 'Key.alt_r']:
                    self._alt_pressed = False
            
            return True  # Success
                    
        except Exception as e:
            print(f"❌ Lỗi khi thực hiện sự kiện: {e}")
            return False  # Failed
    
    def print_stats(self):
        """In thống kê về macro hiện tại"""
        if not self.events:
            print("Không có macro nào!")
            return
            
        stats = {
            'mouse_move': 0,
            'mouse_click': 0,
            'mouse_scroll': 0,
            'key_press': 0,
            'key_release': 0
        }
        
        for event in self.events:
            event_type = event['type']
            if event_type in stats:
                stats[event_type] += 1
        
        print("\n=== THỐNG KÊ MACRO ===")
        print(f"Tổng số sự kiện: {len(self.events)}")
        print(f"Di chuyển chuột: {stats['mouse_move']}")
        print(f"Click chuột: {stats['mouse_click']}")
        print(f"Cuộn chuột: {stats['mouse_scroll']}")
        print(f"Nhấn phím: {stats['key_press']}")
        print(f"Thả phím: {stats['key_release']}")
        
        if self.events:
            duration = self.events[-1]['timestamp']
            print(f"Thời lượng: {duration:.2f} giây")
        print("========================\n")
    
    def create_screenshot_folder(self):
        """Tạo folder để lưu screenshot"""
        try:
            if not os.path.exists(self.screenshot_folder):
                os.makedirs(self.screenshot_folder)
                print(f"📁 Đã tạo folder: {self.screenshot_folder}")
        except Exception as e:
            print(f"❌ Lỗi tạo folder screenshot: {e}")
    
    def take_screenshot(self):
        """Chụp màn hình và lưu vào folder"""
        try:
            # Tạo tên file với timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            filepath = os.path.join(self.screenshot_folder, filename)
            
            # Chụp màn hình
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            
            print(f"📸 Đã chụp màn hình: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Lỗi chụp màn hình: {e}")
            return None
    
    def start_screenshot_hotkey(self):
        """Bắt đầu lắng nghe hotkey để chụp màn hình"""
        if self.screenshot_enabled:
            print("Screenshot hotkey đã được bật!")
            return
            
        print("🔥 Bật hotkey chụp màn hình...")
        print("📸 Nhấn F12 để chụp màn hình")
        
        self.screenshot_enabled = True
        
        # Tạo listener riêng cho screenshot
        self.screenshot_listener = KeyboardListener(
            on_press=self.on_screenshot_key_press
        )
        self.screenshot_listener.start()
    
    def stop_screenshot_hotkey(self):
        """Dừng lắng nghe hotkey chụp màn hình"""
        if not self.screenshot_enabled:
            return
            
        print("🛑 Tắt hotkey chụp màn hình!")
        self.screenshot_enabled = False
        
        if self.screenshot_listener:
            self.screenshot_listener.stop()
            self.screenshot_listener = None
    
    def on_screenshot_key_press(self, key):
        """Xử lý phím bấm cho screenshot"""
        if not self.screenshot_enabled:
            return
            
        try:
            # F12 để chụp màn hình
            if key == keyboard.Key.f12:
                self.take_screenshot()
                
            # F7 để auto type
            elif key == keyboard.Key.f7:
                self.auto_type()
                
        except Exception as e:
            print(f"❌ Lỗi xử lý hotkey: {e}")
    
    def list_screenshots(self):
        """Liệt kê các file screenshot đã chụp"""
        try:
            if not os.path.exists(self.screenshot_folder):
                print("📁 Chưa có folder screenshot!")
                return
                
            files = [f for f in os.listdir(self.screenshot_folder) 
                    if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            if not files:
                print("📸 Chưa có screenshot nào!")
                return
                
            print(f"\n📸 DANH SÁCH SCREENSHOT ({len(files)} file):")
            print("=" * 50)
            
            # Sắp xếp theo thời gian (mới nhất trước)
            files.sort(reverse=True)
            
            for i, filename in enumerate(files, 1):
                filepath = os.path.join(self.screenshot_folder, filename)
                size = os.path.getsize(filepath)
                size_mb = size / (1024 * 1024)
                
                # Lấy thời gian từ tên file nếu có
                if filename.startswith('screenshot_') and len(filename) >= 25:
                    time_str = filename[11:26]  # screenshot_YYYYMMDD_HHMMSS
                    try:
                        time_obj = datetime.strptime(time_str, "%Y%m%d_%H%M%S")
                        time_display = time_obj.strftime("%d/%m/%Y %H:%M:%S")
                    except:
                        time_display = "Unknown"
                else:
                    time_display = "Unknown"
                
                print(f"{i:2d}. {filename}")
                print(f"    📅 {time_display}")
                print(f"    📊 {size_mb:.2f} MB")
                print()
                
        except Exception as e:
            print(f"❌ Lỗi liệt kê screenshot: {e}")
    
    def cleanup_old_screenshots(self, days=7):
        """Xóa screenshot cũ hơn số ngày chỉ định"""
        try:
            if not os.path.exists(self.screenshot_folder):
                return
                
            import time as time_module
            cutoff_time = time_module.time() - (days * 24 * 60 * 60)
            deleted_count = 0
            
            for filename in os.listdir(self.screenshot_folder):
                filepath = os.path.join(self.screenshot_folder, filename)
                
                if os.path.isfile(filepath):
                    file_time = os.path.getmtime(filepath)
                    if file_time < cutoff_time:
                        try:
                            os.remove(filepath)
                            deleted_count += 1
                            print(f"🗑️  Đã xóa: {filename}")
                        except Exception as e:
                            print(f"❌ Không thể xóa {filename}: {e}")
            
            if deleted_count > 0:
                print(f"✅ Đã xóa {deleted_count} screenshot cũ!")
            else:
                print("📸 Không có screenshot cũ để xóa!")
                
        except Exception as e:
            print(f"❌ Lỗi cleanup screenshot: {e}")
    
    def replay_alternating(self, macro_a_events, macro_b_events, repeat_a_count=1, total_cycles=1, speed_multiplier=1.0, progress_callback=None):
        """
        Phát lại xen kẽ giữa 2 macro:
        - Phát lại macro A x lần
        - Phát lại macro B 1 lần  
        - Lặp lại total_cycles chu kỳ
        
        Args:
            macro_a_events: List events của macro A
            macro_b_events: List events của macro B
            repeat_a_count: Số lần phát lại macro A trước khi chạy B (mặc định 1)
            total_cycles: Số chu kỳ A-B tổng cộng (mặc định 1)
            speed_multiplier: Tốc độ phát lại (mặc định 1.0)
            progress_callback: Callback function để cập nhật progress (optional)
                              Signature: callback(a_current, a_total, cycle_current, cycle_total, action)
        """
        if not macro_a_events or not macro_b_events:
            print("❌ Cần có cả macro A và macro B để phát lại xen kẽ!")
            return False
        
        if self.replaying:
            print("⚠️ Đang phát lại macro khác!")
            return False
        
        print(f"🔄 Bắt đầu phát lại xen kẽ:")
        print(f"   📹 Macro A: {len(macro_a_events)} sự kiện")
        print(f"   📹 Macro B: {len(macro_b_events)} sự kiện")
        print(f"   🔁 A chạy {repeat_a_count} lần → B chạy 1 lần")
        print(f"   🔄 Tổng {total_cycles} chu kỳ")
        print(f"   ⚡ Tốc độ: {speed_multiplier}x")
        print("🛑 Nhấn ESC để dừng phát lại")
        
        self.replaying = True
        
        # Reset modifier key states
        self._ctrl_pressed = False
        self._shift_pressed = False
        self._alt_pressed = False
        
        # Setup hotkey listener for stopping
        self.replay_listener = KeyboardListener(on_press=self.on_replay_key_press)
        self.replay_listener.start()
        
        try:
            total_completed_events = 0
            
            for cycle in range(total_cycles):
                if not self.replaying:
                    break
                
                print(f"\n🔄 === CHU KỲ {cycle + 1}/{total_cycles} ===")
                
                # Update progress: Start of cycle
                if progress_callback:
                    progress_callback(0, repeat_a_count, cycle + 1, total_cycles, f"Chu kỳ {cycle + 1}/{total_cycles}")
                
                # Phát lại macro A (repeat_a_count lần)
                print(f"▶️ Phát lại Macro A ({repeat_a_count} lần)...")
                for a_repeat in range(repeat_a_count):
                    if not self.replaying:
                        break
                    
                    if repeat_a_count > 1:
                        print(f"   📹 A - Lần {a_repeat + 1}/{repeat_a_count}")
                    
                    # Update progress: A execution
                    if progress_callback:
                        progress_callback(a_repeat + 1, repeat_a_count, cycle + 1, total_cycles, 
                                        f"Chạy Macro A - Lần {a_repeat + 1}/{repeat_a_count}")
                    
                    completed = self._execute_events(macro_a_events, speed_multiplier)
                    total_completed_events += completed
                    
                    if not self.replaying:
                        break
                    
                    # Nghỉ giữa các lần lặp A (nếu có nhiều hơn 1 lần)
                    if a_repeat < repeat_a_count - 1 and self.replaying:
                        print("   ⏸️ Nghỉ 3 giây giữa các lần A...")
                        for i in range(3, 0, -1):
                            if not self.replaying:
                                break
                            print(f"      ⏰ {i}...")
                            if progress_callback:
                                progress_callback(a_repeat + 1, repeat_a_count, cycle + 1, total_cycles, 
                                                f"Nghỉ {i}s giữa A...")
                            time.sleep(1)
                
                if not self.replaying:
                    break
                
                # Phát lại macro B (1 lần)
                print(f"▶️ Phát lại Macro B...")
                if progress_callback:
                    progress_callback(repeat_a_count, repeat_a_count, cycle + 1, total_cycles, "Chạy Macro B")
                
                completed = self._execute_events(macro_b_events, speed_multiplier)
                total_completed_events += completed
                
                if not self.replaying:
                    break
                
                # Nghỉ giữa các chu kỳ (nếu còn chu kỳ tiếp theo)
                if cycle < total_cycles - 1 and self.replaying:
                    print("⏸️ Nghỉ 5 giây giữa các chu kỳ...")
                    for i in range(5, 0, -1):
                        if not self.replaying:
                            break
                        print(f"   ⏰ Còn {i} giây đến chu kỳ tiếp theo...")
                        if progress_callback:
                            progress_callback(repeat_a_count, repeat_a_count, cycle + 1, total_cycles, 
                                            f"Nghỉ {i}s giữa chu kỳ...")
                        time.sleep(1)
            
            if self.replaying:
                print("✅ Hoàn thành phát lại xen kẽ!")
                expected_total = (len(macro_a_events) * repeat_a_count + len(macro_b_events)) * total_cycles
                print(f"📊 Tổng sự kiện: {total_completed_events}/{expected_total}")
                
                # Final progress update
                if progress_callback:
                    progress_callback(repeat_a_count, repeat_a_count, total_cycles, total_cycles, "✅ Hoàn thành!")
                
                return True
            else:
                print(f"⏹️ Phát lại bị dừng. Đã thực hiện: {total_completed_events} sự kiện")
                return False
            
        except KeyboardInterrupt:
            print("⏸️ Đã dừng phát lại xen kẽ (Ctrl+C)!")
            return False
        except Exception as e:
            print(f"❌ Lỗi khi phát lại xen kẽ: {e}")
            return False
        finally:
            self.replaying = False
            if self.replay_listener:
                self.replay_listener.stop()
                self.replay_listener = None
    
    def _execute_events(self, events, speed_multiplier):
        """
        Thực thi danh sách events với tốc độ đã cho
        Trả về số sự kiện đã hoàn thành
        """
        completed_events = 0
        last_timestamp = 0
        
        for i, event in enumerate(events):
            if not self.replaying:
                break
            
            # Calculate wait time with smoothing
            raw_wait_time = (event['timestamp'] - last_timestamp) / speed_multiplier
            wait_time = max(self.min_delay, raw_wait_time * self.smooth_factor)
            
            if wait_time > 0:
                time.sleep(wait_time)
            
            if not self.replaying:
                break
            
            # Execute event
            success = self.execute_event(event)
            if success:
                completed_events += 1
                
            last_timestamp = event['timestamp']
            
            # Progress feedback for long macros
            if len(events) > 50 and (i + 1) % 25 == 0:
                progress = (i + 1) / len(events) * 100
                print(f"   📈 Tiến độ: {progress:.1f}% ({i + 1}/{len(events)})")
        
        return completed_events 