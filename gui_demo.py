#!/usr/bin/env python3
"""
Demo script để kiểm tra GUI
"""

try:
    import tkinter as tk
    from tkinter import messagebox
    print("✅ Tkinter đã sẵn sàng!")
    
    # Test basic GUI
    root = tk.Tk()
    root.title("Test GUI")
    root.geometry("300x200")
    
    label = tk.Label(root, text="🎯 GUI Test", font=('Arial', 14))
    label.pack(pady=20)
    
    def test_click():
        messagebox.showinfo("Success", "✅ GUI hoạt động tốt!\n\nBạn có thể chạy:\npython gui_app.py")
        root.destroy()
    
    button = tk.Button(root, text="Click để test", command=test_click)
    button.pack(pady=10)
    
    info_label = tk.Label(root, text="Nếu thấy window này thì GUI OK!", 
                         wraplength=250)
    info_label.pack(pady=10)
    
    root.mainloop()
    
except ImportError:
    print("❌ Tkinter không có sẵn!")
    print("💡 Cài đặt Python với tkinter support")
except Exception as e:
    print(f"❌ Lỗi: {e}") 