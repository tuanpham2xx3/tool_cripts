#!/usr/bin/env python3
"""
GUI Application cho Macro Recorder Tool
Sử dụng tkinter để tạo giao diện đơn giản với nút bấm
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import time
import os
from macro_recorder import MacroRecorder
try:
    from version import __version__, APP_NAME
except ImportError:
    __version__ = "1.0.0"
    APP_NAME = "Macro Recorder Tool"

class MacroRecorderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"🎯 {APP_NAME} v{__version__}")
        self.root.geometry("1000x550")
        
        # Tạo recorder instance
        self.recorder = MacroRecorder()
        
        # Đặt callback cho F9
        self.recorder.set_f9_callback(self.handle_f9_save_prompt)
        
        # Trạng thái
        self.recording = False
        self.screenshot_enabled = False
        
        # Macro storage for alternating playback
        self.macro_a_events = []
        self.macro_b_events = []
        self.macro_a_filename = ""
        self.macro_b_filename = ""
        
        # Tạo giao diện
        self.create_widgets()
        
        # Redirect stdout để hiển thị log trong GUI
        self.redirect_output()
        
    def create_widgets(self):
        """Tạo các widget cho giao diện"""
        
        # Main container frame
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Left scrollable frame for controls
        self.canvas = tk.Canvas(main_container, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S)
        
        self.scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=5, sticky=tk.N+tk.S)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Main frame inside canvas
        main_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=main_frame, anchor="nw")
        
        # Title
        title_label = ttk.Label(main_frame, text=f"🎯 {APP_NAME.upper()} v{__version__}", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # === MACRO CONTROLS ===
        macro_frame = ttk.LabelFrame(main_frame, text="📹 Macro Controls", padding="10")
        macro_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, padx=(0, 5))
        
        # Macro buttons
        self.record_btn = ttk.Button(macro_frame, text="🎬 Start Recording", 
                                   command=self.start_recording, width=20)
        self.record_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.stop_btn = ttk.Button(macro_frame, text="⏹️ Stop Recording", 
                                 command=self.stop_recording, width=20, state='disabled')
        self.stop_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.save_btn = ttk.Button(macro_frame, text="💾 Save Macro", 
                                 command=self.save_macro, width=20)
        self.save_btn.grid(row=1, column=0, padx=5, pady=5)
        
        self.load_btn = ttk.Button(macro_frame, text="📂 Load Macro", 
                                 command=self.load_macro, width=20)
        self.load_btn.grid(row=1, column=1, padx=5, pady=5)
        
        # Playback controls
        playback_frame = ttk.Frame(macro_frame)
        playback_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(playback_frame, text="▶️ Play", 
                  command=lambda: self.replay_macro(1.0), width=10).grid(row=0, column=0, padx=1)
        ttk.Button(playback_frame, text="⚡ 2x", 
                  command=lambda: self.replay_macro(2.0), width=8).grid(row=0, column=1, padx=1)
        ttk.Button(playback_frame, text="🐌 0.5x", 
                  command=lambda: self.replay_macro(0.5), width=8).grid(row=0, column=2, padx=1)
        self.stop_replay_btn = ttk.Button(playback_frame, text="⏹️ Stop", 
                                        command=self.stop_replay, width=8, state='disabled')
        self.stop_replay_btn.grid(row=0, column=3, padx=1)
        
        # Smoothness control
        smooth_frame = ttk.Frame(macro_frame)
        smooth_frame.grid(row=3, column=0, columnspan=2, pady=(5, 0))
        
        ttk.Label(smooth_frame, text="Smoothness:").grid(row=0, column=0, padx=(0, 5))
        self.smooth_var = tk.DoubleVar(value=1.0)
        smooth_scale = ttk.Scale(smooth_frame, from_=0.1, to=2.0, variable=self.smooth_var, 
                               orient=tk.HORIZONTAL, length=150)
        smooth_scale.grid(row=0, column=1, padx=5)
        self.smooth_label = ttk.Label(smooth_frame, text="1.0x")
        self.smooth_label.grid(row=0, column=2, padx=(5, 0))
        
        # Update label when scale changes
        def update_smooth_label(*args):
            value = self.smooth_var.get()
            self.smooth_label.config(text=f"{value:.1f}x")
            self.recorder.smooth_factor = value
            
        self.smooth_var.trace('w', update_smooth_label)
        
        # === SCREENSHOT CONTROLS ===
        screenshot_frame = ttk.LabelFrame(main_frame, text="📸 Screenshot Controls", padding="10")
        screenshot_frame.grid(row=1, column=2, columnspan=2, sticky=tk.W+tk.E, padx=(5, 0))
        
        self.hotkey_btn = ttk.Button(screenshot_frame, text="🔥 Enable Hotkey (F12)", 
                                   command=self.toggle_screenshot_hotkey, width=20)
        self.hotkey_btn.grid(row=0, column=0, padx=5, pady=5)
        
        ttk.Button(screenshot_frame, text="📸 Take Screenshot", 
                  command=self.take_screenshot, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Button(screenshot_frame, text="📁 List Screenshots", 
                  command=self.list_screenshots, width=20).grid(row=1, column=0, padx=5, pady=5)
        
        ttk.Button(screenshot_frame, text="🗑️ Cleanup Old", 
                  command=self.cleanup_screenshots, width=20).grid(row=1, column=1, padx=5, pady=5)
        
        # === AUTO TYPE & REPEAT CONTROLS ===
        paste_frame = ttk.LabelFrame(main_frame, text="⌨️ Auto Type & Repeat", padding="10")
        paste_frame.grid(row=2, column=0, columnspan=4, sticky=tk.W+tk.E, pady=(10, 0))
        
        # Type content section
        paste_content_frame = ttk.Frame(paste_frame)
        paste_content_frame.grid(row=0, column=0, columnspan=4, sticky=tk.W+tk.E, pady=(0, 10))
        
        ttk.Label(paste_content_frame, text="⌨️ Type Content (F7):").grid(row=0, column=0, sticky=tk.W)
        self.paste_entry = ttk.Entry(paste_content_frame, width=50)
        self.paste_entry.grid(row=0, column=1, padx=(5, 5), sticky=tk.W+tk.E)
        
        ttk.Button(paste_content_frame, text="⌨️ Set", 
                  command=self.set_type_content, width=8).grid(row=0, column=2, padx=(5, 0))
        
        # Configure column weight for expansion
        paste_content_frame.columnconfigure(1, weight=1)
        
        # Repeat control section
        repeat_frame = ttk.Frame(paste_frame)
        repeat_frame.grid(row=1, column=0, columnspan=4, sticky=tk.W+tk.E)
        
        ttk.Label(repeat_frame, text="🔁 Repeat Count:").grid(row=0, column=0, sticky=tk.W)
        self.repeat_var = tk.IntVar(value=1)
        repeat_spinbox = ttk.Spinbox(repeat_frame, from_=1, to=50, textvariable=self.repeat_var, width=10)
        repeat_spinbox.grid(row=0, column=1, padx=(5, 10))
        
        # Warning label for high repeat counts
        self.repeat_warning = ttk.Label(repeat_frame, text="⚠️ Max 50 để tránh quá tải", foreground="orange", font=("Arial", 8))
        self.repeat_warning.grid(row=0, column=2, padx=(5, 0))
        
        # Play with repeat buttons
        ttk.Button(repeat_frame, text="▶️ Play × Repeat", 
                  command=lambda: self.replay_macro_with_repeat(1.0), width=15).grid(row=0, column=2, padx=5)
        ttk.Button(repeat_frame, text="⚡ 2x × Repeat", 
                  command=lambda: self.replay_macro_with_repeat(2.0), width=15).grid(row=0, column=3, padx=5)
        
        # === ALTERNATING REPLAY ===
        alt_frame = ttk.LabelFrame(main_frame, text="🔄 Alternating Replay (A × x → B × 1)", padding="10")
        alt_frame.grid(row=3, column=0, columnspan=4, sticky=tk.W+tk.E+tk.N+tk.S, pady=(10, 0))
        
        # Configure alt_frame grid weights for responsive layout
        alt_frame.grid_columnconfigure(0, weight=1)
        alt_frame.grid_columnconfigure(1, weight=1)
        alt_frame.grid_rowconfigure(0, weight=0)  # Macro loading section
        alt_frame.grid_rowconfigure(1, weight=0)  # Settings section  
        alt_frame.grid_rowconfigure(2, weight=0)  # Progress section
        alt_frame.grid_rowconfigure(3, weight=0)  # Play buttons
        
        # Top section: Macro loading
        macro_section = ttk.Frame(alt_frame)
        macro_section.grid(row=0, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
        macro_section.grid_columnconfigure(0, weight=1)
        macro_section.grid_columnconfigure(1, weight=1)
        
        # Macro A section
        macro_a_frame = ttk.LabelFrame(macro_section, text="📹 Macro A", padding="5")
        macro_a_frame.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=(0, 5))
        
        ttk.Button(macro_a_frame, text="📂 Load A", 
                  command=self.load_macro_a, width=12).grid(row=0, column=0, padx=5, pady=2)
        self.macro_a_label = ttk.Label(macro_a_frame, text="Chưa load", foreground="gray", 
                                      font=("Arial", 8), wraplength=200)
        self.macro_a_label.grid(row=1, column=0, sticky=tk.W+tk.E, padx=5, pady=2)
        macro_a_frame.grid_columnconfigure(0, weight=1)
        
        # Macro B section  
        macro_b_frame = ttk.LabelFrame(macro_section, text="📹 Macro B", padding="5")
        macro_b_frame.grid(row=0, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=(5, 0))
        
        ttk.Button(macro_b_frame, text="📂 Load B", 
                  command=self.load_macro_b, width=12).grid(row=0, column=0, padx=5, pady=2)
        self.macro_b_label = ttk.Label(macro_b_frame, text="Chưa load", foreground="gray", 
                                      font=("Arial", 8), wraplength=200)
        self.macro_b_label.grid(row=1, column=0, sticky=tk.W+tk.E, padx=5, pady=2)
        macro_b_frame.grid_columnconfigure(0, weight=1)
        
        # Control settings
        control_frame = ttk.LabelFrame(alt_frame, text="⚙️ Settings", padding="5")
        control_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
        
        # Row 1: A repeat and cycles
        ttk.Label(control_frame, text="🔁 A repeat:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.a_repeat_var = tk.IntVar(value=3)
        self.a_repeat_var.trace('w', lambda *args: self.update_alternating_info())
        ttk.Spinbox(control_frame, from_=1, to=20, textvariable=self.a_repeat_var, width=8).grid(row=0, column=1, padx=(0, 15))
        
        ttk.Label(control_frame, text="🔄 Chu kỳ:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.cycles_var = tk.IntVar(value=1)
        self.cycles_var.trace('w', lambda *args: self.update_alternating_info())
        ttk.Spinbox(control_frame, from_=1, to=50, textvariable=self.cycles_var, width=8).grid(row=0, column=3, padx=(0, 15))
        
        # Row 2: Speed
        ttk.Label(control_frame, text="⚡ Tốc độ:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.alt_speed_var = tk.StringVar(value="1.0x")
        speed_combo = ttk.Combobox(control_frame, textvariable=self.alt_speed_var, 
                                  values=["0.5x", "1.0x", "1.5x", "2.0x"], width=8, state="readonly")
        speed_combo.grid(row=1, column=1, pady=(5, 0))
        
        # Progress display section
        progress_frame = ttk.LabelFrame(alt_frame, text="📊 Progress", padding="5")
        progress_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W+tk.E, pady=(0, 10))
        progress_frame.grid_columnconfigure(1, weight=1)
        progress_frame.grid_columnconfigure(3, weight=1)
        
        # Current A repeat progress
        ttk.Label(progress_frame, text="🔁 A Progress:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.a_progress_label = ttk.Label(progress_frame, text="0/3", foreground="blue", font=("Arial", 9, "bold"))
        self.a_progress_label.grid(row=0, column=1, sticky=tk.W)
        
        # Current cycle progress  
        ttk.Label(progress_frame, text="🔄 Cycle:").grid(row=0, column=2, sticky=tk.W, padx=(20, 5))
        self.cycle_progress_label = ttk.Label(progress_frame, text="0/1", foreground="green", font=("Arial", 9, "bold"))
        self.cycle_progress_label.grid(row=0, column=3, sticky=tk.W)
        
        # Current action display
        self.current_action_label = ttk.Label(progress_frame, text="Chưa bắt đầu", 
                                            foreground="gray", font=("Arial", 8))
        self.current_action_label.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(5, 0))
        
        # Play buttons and info
        play_frame = ttk.Frame(alt_frame)
        play_frame.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E)
        
        ttk.Button(play_frame, text="▶️ Start Alternating", 
                  command=self.start_alternating_replay, width=20).grid(row=0, column=0, padx=(0, 5))
        self.stop_alt_btn = ttk.Button(play_frame, text="⏹️ Stop", 
                                      command=self.stop_alternating_replay, width=12, state='disabled')
        self.stop_alt_btn.grid(row=0, column=1)
        
        # Info display
        self.alt_info_label = ttk.Label(play_frame, text="Ví dụ: A×3 → B×1 → A×3 → B×1...", 
                                       foreground="blue", font=("Arial", 8))
        self.alt_info_label.grid(row=1, column=0, columnspan=2, pady=(5, 0), sticky=tk.W)
        
        # === LOG AREA (Right Side) ===
        log_frame = ttk.LabelFrame(main_container, text="📝 Log", padding="5")
        log_frame.grid(row=0, column=4, rowspan=4, sticky=tk.W+tk.E+tk.N+tk.S, padx=(10, 0), pady=(0, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=28, width=38, font=("Consolas", 8), wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)
        
        # Clear log button
        ttk.Button(log_frame, text="🧹 Clear", 
                  command=self.clear_log, width=12).grid(row=1, column=0, pady=(3, 0), sticky=tk.W+tk.E)
        
        # === STATUS & ACTIONS (Bottom) ===
        status_frame = ttk.Frame(main_container)
        status_frame.grid(row=1, column=0, columnspan=4, sticky=tk.W+tk.E, pady=(10, 0))
        
        # Status section
        status_left = ttk.Frame(status_frame)
        status_left.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(status_left, text="Status:").grid(row=0, column=0, sticky=tk.W)
        self.status_label = ttk.Label(status_left, text="Ready", foreground="green")
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 20))
        
        # Macro info
        self.macro_info_label = ttk.Label(status_left, text="No macro loaded", foreground="gray")
        self.macro_info_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 20))
        
        # Action buttons section  
        action_frame = ttk.Frame(status_frame)
        action_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Button(action_frame, text="📊 Stats", 
                  command=self.show_stats, width=8).grid(row=0, column=0, padx=(0, 5))
        
        ttk.Button(action_frame, text="❓ Help", 
                  command=self.show_help, width=8).grid(row=0, column=1)
        
        # Configure status frame
        status_frame.grid_columnconfigure(0, weight=1)  # Left section expands
        status_frame.grid_columnconfigure(1, weight=0)  # Right section fixed
        
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main container configuration
        main_container.grid_rowconfigure(0, weight=1)  # Canvas gets most space
        main_container.grid_rowconfigure(1, weight=0)  # Status bar fixed height
        
        # Content columns (0-3) have equal weight, log column (4) and scrollbar (5) are fixed width
        for i in range(4):
            main_container.grid_columnconfigure(i, weight=1, uniform="content")
        main_container.grid_columnconfigure(4, weight=0, minsize=300)  # Log column fixed width
        main_container.grid_columnconfigure(5, weight=0)  # Scrollbar column
        
        # Main frame configuration
        main_frame.grid_rowconfigure(3, weight=1)  # Alternating replay section gets most space
        for i in range(4):
            main_frame.grid_columnconfigure(i, weight=1, uniform="content")
        
        # Log frame configuration  
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)
        
        # Bind canvas events for scrolling
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        main_frame.bind('<Configure>', self.on_frame_configure)
        
        # Bind mouse wheel only when mouse is over the canvas
        self.canvas.bind("<Enter>", self.on_canvas_enter)
        self.canvas.bind("<Leave>", self.on_canvas_leave)
        
        # Initial log message
        self.log("🚀 Tool đã khởi động!")
        self.log("💡 Sẵn sàng hoạt động!")
        
        # Auto-enable hotkeys on startup
        self.auto_enable_hotkeys()
        
        # Configure initial scroll region
        self.root.after(100, self.update_scroll_region)
        
    def auto_enable_hotkeys(self):
        """Tự động bật các hotkey khi khởi động"""
        try:
            # Enable screenshot hotkey (F12) and auto type hotkey (F7)
            self.recorder.start_screenshot_hotkey()
            self.screenshot_enabled = True
            self.hotkey_btn.config(text="🛑 Disable Hotkey")
            self.log("🔥 Hotkey: F12, F7 ON")
            self.update_status("Hotkeys: ON (F12, F7)", "green")
        except Exception as e:
            self.log(f"⚠️ Không thể bật hotkey: {e}")
            self.update_status("Hotkeys: ERROR", "red")
        
    def redirect_output(self):
        """Redirect print statements to log area"""
        import sys
        sys.stdout = TextRedirector(self.log_text)
        
    def log(self, message):
        """Add message to log area"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        """Clear log area"""
        self.log_text.delete(1.0, tk.END)
        
    def update_status(self, text, color="black"):
        """Update status label"""
        self.status_label.config(text=text, foreground=color)
    
    def update_macro_info(self):
        """Update macro information display"""
        if not self.recorder.events:
            self.macro_info_label.config(text="No macro loaded", foreground="gray")
            return
        
        # Calculate basic info
        event_count = len(self.recorder.events)
        duration = self.recorder.events[-1]['timestamp'] if self.recorder.events else 0
        
        # Create info text
        info_text = f"📝 {event_count} events | ⏱️ {duration:.1f}s"
        
        if event_count > 0:
            events_per_sec = event_count / duration if duration > 0 else 0
            info_text += f" | 📈 {events_per_sec:.1f}/s"
        
        self.macro_info_label.config(text=info_text, foreground="blue")
        
    def start_recording(self):
        """Start recording macro"""
        if self.recording:
            self.log("⚠️ Đang trong quá trình ghi!")
            return
            
        self.log("🎬 Chuẩn bị ghi...")
        self.log("⏳ 3s để sẵn sàng...")
        self.update_status("Preparing...", "orange")
        
        # Countdown in separate thread
        def countdown_and_record():
            for i in range(3, 0, -1):
                self.log(f"   {i}...")
                time.sleep(1)
            
            self.recorder.start_recording()
            self.recording = True
            self.log("✅ Bắt đầu ghi! F9=dừng")
            self.update_status("Recording... (F9=stop&save)", "red")
            self.record_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            
        threading.Thread(target=countdown_and_record, daemon=True).start()
        
    def stop_recording(self):
        """Stop recording macro"""
        self.recorder.stop_recording()
        self.recording = False
        self.log("✅ Dừng ghi!")
        self.update_status("Ready", "green")
        self.record_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.update_macro_info()
    
    def handle_f9_save_prompt(self):
        """Xử lý F9 với dialog lưu file"""
        # Dừng recording trước
        self.recorder.recording = False
        self.recorder.end_time = time.time()
        
        if self.recorder.mouse_listener:
            self.recorder.mouse_listener.stop()
        if self.recorder.keyboard_listener:
            self.recorder.keyboard_listener.stop()
        
        # Cập nhật UI
        self.recording = False
        self.log("✅ Dừng ghi!")
        self.update_status("Ready", "green")
        self.record_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.update_macro_info()
        
        # Hiện recording summary
        if self.recorder.events and self.recorder.start_time and self.recorder.end_time:
            duration = self.recorder.end_time - self.recorder.start_time
            self.log(f"📊 {duration:.1f}s, {len(self.recorder.events)} events")
            self.log(f"📈 {len(self.recorder.events)/duration:.1f}/s")
        
        # Hỏi có muốn lưu không
        if self.recorder.events:
            result = messagebox.askyesno("💾 Lưu macro", 
                                       "Bạn có muốn lưu macro này không?",
                                       icon='question')
            if result:
                self.save_macro()
        
    def save_macro(self):
        """Save macro to file"""
        if not self.recorder.events:
            messagebox.showwarning("Warning", "Không có macro nào để lưu!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Lưu macro"
        )
        
        if filename:
            self.recorder.save_macro(filename)
            self.log(f"💾 Lưu: {os.path.basename(filename)}")
            
    def load_macro(self):
        """Load macro from file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Tải macro"
        )
        
        if filename:
            if self.recorder.load_macro(filename):
                self.log(f"📂 Tải: {os.path.basename(filename)}")
                self.update_macro_info()
            else:
                self.log(f"❌ Lỗi tải: {os.path.basename(filename)}")
                self.update_macro_info()
                
    def replay_macro(self, speed=1.0):
        """Replay macro with specified speed"""
        if not self.recorder.events:
            messagebox.showwarning("Warning", "Không có macro nào để phát!")
            return
            
        if self.recorder.replaying:
            self.log("⚠️ Đang phát lại macro khác!")
            return
            
        speed_text = {1.0: "bình thường", 2.0: "2x", 0.5: "0.5x"}
        self.log(f"▶️ Phát lại macro với tốc độ {speed_text.get(speed, str(speed))}...")
        self.log("⏳ 3 giây để chuẩn bị...")
        self.log("🛑 Nhấn ESC hoặc click nút Stop để dừng")
        self.update_status(f"Preparing replay ({speed_text.get(speed, str(speed))})", "orange")
        
        def countdown_and_replay():
            for i in range(3, 0, -1):
                self.log(f"   {i}...")
                time.sleep(1)
                
            self.update_status(f"Replaying ({speed_text.get(speed, str(speed))})", "blue")
            self.stop_replay_btn.config(state='normal')
            
            success = self.recorder.replay_macro(speed, enable_hotkey_stop=True)
            
            self.stop_replay_btn.config(state='disabled')
            if success:
                self.update_status("Ready", "green")
            else:
                self.update_status("Stopped", "orange")
            
        threading.Thread(target=countdown_and_replay, daemon=True).start()
    
    def stop_replay(self):
        """Stop macro replay"""
        if self.recorder.replaying:
            self.log("🛑 Dừng phát lại macro...")
            self.recorder.stop_replay()
            self.stop_replay_btn.config(state='disabled')
        else:
            self.log("⚠️ Không có macro nào đang phát lại!")
        
    def toggle_screenshot_hotkey(self):
        """Toggle screenshot hotkey on/off"""
        if self.screenshot_enabled:
            self.recorder.stop_screenshot_hotkey()
            self.screenshot_enabled = False
            self.hotkey_btn.config(text="🔥 Enable Hotkey (F12)")
            self.log("🛑 Đã tắt hotkey chụp màn hình!")
            self.update_status("Screenshot hotkey: OFF", "black")
        else:
            self.recorder.start_screenshot_hotkey()
            self.screenshot_enabled = True
            self.hotkey_btn.config(text="🛑 Disable Hotkey")
            self.log("🔥 Đã bật hotkey chụp màn hình! (F12: chụp)")
            self.update_status("Screenshot hotkey: ON (F12)", "green")
            
    def take_screenshot(self):
        """Take screenshot immediately"""
        self.log("📸 Đang chụp màn hình...")
        screenshot_path = self.recorder.take_screenshot()
        if screenshot_path:
            self.log(f"✅ Screenshot đã được lưu: {screenshot_path}")
        else:
            self.log("❌ Chụp màn hình thất bại!")
            
    def list_screenshots(self):
        """List all screenshots"""
        self.log("📁 Danh sách screenshot:")
        self.recorder.list_screenshots()
        
    def cleanup_screenshots(self):
        """Cleanup old screenshots"""
        # Ask for number of days
        dialog = tk.Toplevel(self.root)
        dialog.title("Cleanup Screenshots")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Xóa screenshot cũ hơn bao nhiêu ngày?").pack(pady=10)
        
        days_var = tk.StringVar(value="7")
        days_entry = ttk.Entry(dialog, textvariable=days_var, width=10)
        days_entry.pack(pady=5)
        
        def do_cleanup():
            try:
                days = int(days_var.get())
                if days < 1:
                    messagebox.showerror("Error", "Số ngày phải >= 1!")
                    return
                    
                self.log(f"🗑️ Đang xóa screenshot cũ hơn {days} ngày...")
                self.recorder.cleanup_old_screenshots(days)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Vui lòng nhập số ngày hợp lệ!")
                
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="OK", command=do_cleanup).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def show_stats(self):
        """Show macro statistics"""
        self.log("📊 Thống kê macro:")
        self.recorder.print_stats()
        
    def show_help(self):
        """Show help dialog"""
        help_text = """
🎯 HƯỚNG DẪN SỬ DỤNG

📹 GHI MACRO:
• Click "Start Recording" để bắt đầu ghi
• Thực hiện các hành động cần ghi lại
• Click "Stop Recording" hoặc nhấn F9 để dừng
• Click "Save Macro" để lưu vào file (format mới với thông tin timing)

▶️ PHÁT LẠI MACRO:
• Click "Load Macro" để tải macro từ file
• Điều chỉnh "Smoothness" để phát lại mượt hơn:
  - 0.1x: Rất chậm, chính xác tuyệt đối
  - 1.0x: Tốc độ bình thường 
  - 2.0x: Nhanh hơn, ít delay
• Click "Play" / "2x" / "0.5x" để phát lại
• Click "Stop" hoặc nhấn ESC để dừng phát lại

📸 CHỤP MÀN HÌNH:
• Hotkey tự động bật khi khởi động! 🔥
• Nhấn F12 bất cứ lúc nào để chụp màn hình
• Click "Disable/Enable Hotkey" để bật/tắt F12
• Click "Take Screenshot" để chụp ngay lập tức
• Screenshot được lưu trong folder SCREENSHOT/

🔄 PHÁT LẠI XEN KẼ:
• Load Macro A và B từ các file khác nhau
• Cài đặt A repeat: số lần phát A trước khi chạy B
• Cài đặt chu kỳ: tổng số chu kỳ A-B
• Ví dụ: A×3 → B×1 → A×3 → B×1... (lặp theo chu kỳ)
• Nhấn ESC để dừng phát lại xen kẽ

📊 THÔNG TIN MACRO:
• Hiển thị số sự kiện, thời lượng, tần suất
• Click "Stats" để xem thống kê chi tiết
• Format mới lưu thông tin timing để phát lại mượt hơn

⌨️ PHÍM TẮT:
• F9: Dừng ghi macro và hỏi có lưu không
• F7: Auto gõ nội dung đã đặt
• F12: Chụp màn hình (tự động bật!)
• ESC: Dừng phát lại macro
• Ctrl+C: Dừng bất kỳ hoạt động nào
"""
        
        # Create help dialog
        help_dialog = tk.Toplevel(self.root)
        help_dialog.title("❓ Help")
        help_dialog.geometry("500x400")
        help_dialog.transient(self.root)
        
        text_widget = scrolledtext.ScrolledText(help_dialog, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(expand=True, fill='both')
        text_widget.insert(1.0, help_text)
        text_widget.config(state='disabled')
        
        ttk.Button(help_dialog, text="OK", command=help_dialog.destroy).pack(pady=10)
    
    def set_type_content(self):
        """Set type content from entry field"""
        content = self.paste_entry.get()
        if content:
            self.recorder.set_type_content(content)
            self.log(f"⌨️ Đã đặt nội dung gõ: '{content[:50]}{'...' if len(content) > 50 else ''}'")
        else:
            messagebox.showwarning("Warning", "Vui lòng nhập nội dung để gõ!")
    
    def replay_macro_with_repeat(self, speed=1.0):
        """Replay macro with repeat count"""
        if not self.recorder.events:
            messagebox.showwarning("Warning", "Chưa có macro để phát lại!")
            return
            
        repeat_count = self.repeat_var.get()
        
        def replay_thread():
            self.log(f"▶️ Bắt đầu phát lại macro với tốc độ {speed}x × {repeat_count} lần")
            self.update_status(f"Playing {speed}x × {repeat_count}...", "blue")
            self.stop_replay_btn.config(state='normal')
            
            success = self.recorder.replay_macro(speed, True, repeat_count)
            
            if success:
                self.log("✅ Hoàn thành phát lại macro!")
            else:
                self.log("⏹️ Phát lại macro bị dừng")
                
            self.update_status("Ready", "green")
            self.stop_replay_btn.config(state='disabled')
        
        threading.Thread(target=replay_thread, daemon=True).start()
    
    def load_macro_a(self):
        """Load macro A for alternating playback"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Tải Macro A"
        )
        
        if filename:
            # Create temporary recorder to load the macro
            temp_recorder = MacroRecorder()
            if temp_recorder.load_macro(filename):
                self.macro_a_events = temp_recorder.events.copy()
                self.macro_a_filename = os.path.basename(filename)
                self.macro_a_label.config(text=f"{self.macro_a_filename} ({len(self.macro_a_events)} events)", 
                                        foreground="green")
                self.log(f"📂 A: {os.path.basename(filename)}")
                self.update_alternating_info()
            else:
                self.log(f"❌ Lỗi A: {os.path.basename(filename)}")
                
    def load_macro_b(self):
        """Load macro B for alternating playback"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Tải Macro B"
        )
        
        if filename:
            # Create temporary recorder to load the macro
            temp_recorder = MacroRecorder()
            if temp_recorder.load_macro(filename):
                self.macro_b_events = temp_recorder.events.copy()
                self.macro_b_filename = os.path.basename(filename)
                self.macro_b_label.config(text=f"{self.macro_b_filename} ({len(self.macro_b_events)} events)", 
                                        foreground="green")
                self.log(f"📂 B: {os.path.basename(filename)}")
                self.update_alternating_info()
            else:
                self.log(f"❌ Lỗi B: {os.path.basename(filename)}")
    
    def update_alternating_info(self):
        """Update alternating replay info display"""
        if self.macro_a_events and self.macro_b_events:
            a_repeat = self.a_repeat_var.get()
            cycles = self.cycles_var.get()
            info_text = f"Sẽ chạy: A×{a_repeat} → B×1, lặp {cycles} chu kỳ"
            self.alt_info_label.config(text=info_text, foreground="blue")
            
            # Update progress displays
            self.a_progress_label.config(text=f"0/{a_repeat}")
            self.cycle_progress_label.config(text=f"0/{cycles}")
            self.current_action_label.config(text="Sẵn sàng để bắt đầu", foreground="green")
        else:
            self.alt_info_label.config(text="Cần load cả Macro A và B", foreground="orange")
            self.a_progress_label.config(text="0/0")
            self.cycle_progress_label.config(text="0/0")
            self.current_action_label.config(text="Chưa load macro", foreground="gray")
    
    def update_alternating_progress(self, a_current=0, a_total=0, cycle_current=0, cycle_total=0, action=""):
        """Update alternating replay progress display"""
        try:
            # Update A repeat progress
            self.a_progress_label.config(text=f"{a_current}/{a_total}")
            if a_current >= a_total and a_total > 0:
                self.a_progress_label.config(foreground="green")
            else:
                self.a_progress_label.config(foreground="blue")
            
            # Update cycle progress
            self.cycle_progress_label.config(text=f"{cycle_current}/{cycle_total}")
            if cycle_current >= cycle_total and cycle_total > 0:
                self.cycle_progress_label.config(foreground="green")
            else:
                self.cycle_progress_label.config(foreground="blue")
            
            # Update current action
            if action:
                self.current_action_label.config(text=action, foreground="blue")
            
            # Force GUI update
            self.root.update_idletasks()
        except Exception as e:
            self.log(f"⚠️ Lỗi cập nhật progress: {e}")
    
    def reset_alternating_progress(self):
        """Reset alternating replay progress to initial state"""
        try:
            a_repeat = self.a_repeat_var.get()
            cycles = self.cycles_var.get()
            self.a_progress_label.config(text=f"0/{a_repeat}", foreground="blue")
            self.cycle_progress_label.config(text=f"0/{cycles}", foreground="blue")
            self.current_action_label.config(text="Chưa bắt đầu", foreground="gray")
        except Exception:
            self.a_progress_label.config(text="0/0", foreground="gray")
            self.cycle_progress_label.config(text="0/0", foreground="gray")
            self.current_action_label.config(text="Chưa bắt đầu", foreground="gray")
    
    def start_alternating_replay(self):
        """Start alternating replay between macro A and B"""
        if not self.macro_a_events:
            messagebox.showwarning("Warning", "Chưa load Macro A!")
            return
        
        if not self.macro_b_events:
            messagebox.showwarning("Warning", "Chưa load Macro B!")
            return
        
        if self.recorder.replaying:
            self.log("⚠️ Đang phát lại macro khác!")
            return
        
        a_repeat = self.a_repeat_var.get()
        cycles = self.cycles_var.get()
        speed_text = self.alt_speed_var.get()
        speed = float(speed_text.replace('x', ''))
        
        self.log(f"🔄 Bắt đầu xen kẽ:")
        self.log(f"📹 A: {self.macro_a_filename[:15]}...")
        self.log(f"📹 B: {self.macro_b_filename[:15]}...")
        self.log(f"🔁 A×{a_repeat}→B×1, {cycles} chu kỳ")
        self.log("📊 Xem tiến độ ở Progress!")
        self.log("⏳ Chuẩn bị trong 3s...")
        
        # Reset progress display
        self.reset_alternating_progress()
        
        def countdown_and_start():
            for i in range(3, 0, -1):
                self.log(f"   {i}...")
                self.update_alternating_progress(0, a_repeat, 0, cycles, f"Chuẩn bị... {i}")
                time.sleep(1)
            
            self.update_status(f"Alternating {speed_text} (A×{a_repeat}→B)", "blue")
            self.stop_alt_btn.config(state='normal')
            self.update_alternating_progress(0, a_repeat, 0, cycles, "Bắt đầu phát lại...")
            
            # Pass progress callback to recorder
            def progress_callback(a_current, a_total, cycle_current, cycle_total, action):
                self.update_alternating_progress(a_current, a_total, cycle_current, cycle_total, action)
            
            success = self.recorder.replay_alternating(
                self.macro_a_events, 
                self.macro_b_events, 
                a_repeat, 
                cycles, 
                speed,
                progress_callback=progress_callback
            )
            
            self.stop_alt_btn.config(state='disabled')
            if success:
                self.update_status("Ready", "green")
                self.update_alternating_progress(a_repeat, a_repeat, cycles, cycles, "✅ Hoàn thành!")
                self.log("✅ Hoàn thành xen kẽ!")
            else:
                self.update_status("Stopped", "orange")
                self.current_action_label.config(text="⏹️ Đã dừng", foreground="orange")
                self.log("⏹️ Xen kẽ bị dừng")
        
        threading.Thread(target=countdown_and_start, daemon=True).start()
    
    def on_canvas_configure(self, event):
        """Handle canvas configuration changes"""
        # Update scroll region when canvas size changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Update canvas window width to match canvas width
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
    
    def on_frame_configure(self, event):
        """Handle main frame configuration changes"""
        # Update scroll region when frame content changes
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        try:
            # Only scroll if content is larger than canvas and mouse is over canvas
            bbox = self.canvas.bbox("all")
            if bbox and bbox[3] > self.canvas.winfo_height():
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except Exception:
            pass  # Ignore errors during scrolling
    
    def on_canvas_enter(self, event):
        """Bind mouse wheel when entering canvas"""
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    
    def on_canvas_leave(self, event):
        """Unbind mouse wheel when leaving canvas"""
        self.canvas.unbind_all("<MouseWheel>")
    
    def update_scroll_region(self):
        """Update canvas scroll region"""
        try:
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        except Exception:
            pass
    
    def stop_alternating_replay(self):
        """Stop alternating replay"""
        if self.recorder.replaying:
            self.log("🛑 Dừng xen kẽ...")
            self.recorder.stop_replay()
            self.stop_alt_btn.config(state='disabled')
            self.current_action_label.config(text="⏹️ Đã dừng", foreground="orange")
        else:
            self.log("⚠️ Không có xen kẽ nào!")
        
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Bạn có muốn thoát?"):
            # Stop all activities
            self.recorder.stop_recording()
            self.recorder.stop_replay()
            self.recorder.stop_screenshot_hotkey()
            self.root.destroy()

class TextRedirector:
    """Redirect text to a tkinter widget"""
    def __init__(self, widget):
        self.widget = widget

    def write(self, str_input):
        self.widget.insert(tk.END, str_input)
        self.widget.see(tk.END)
        
    def flush(self):
        pass

def main():
    """Main function to run GUI app"""
    root = tk.Tk()
    
    # Set application icon (if available)
    try:
        # Try to set a simple icon
        root.iconbitmap(default='')
    except:
        pass
    
    # Create app
    app = MacroRecorderGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Run the app
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Lỗi khởi động GUI: {e}")
        print("💡 Thử chạy console version: python main.py") 