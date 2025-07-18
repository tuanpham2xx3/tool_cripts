# 🎯 Macro Recorder Tool

Tool ghi lại và phát lại các hành động chuột và bàn phím trên máy tính sử dụng Python.

## ✨ Tính năng

- 📹 **Ghi lại hành động**: Ghi lại click chuột, di chuyển chuột, cuộn chuột và các phím bấm
- ▶️ **Phát lại tự động**: Phát lại chính xác các hành động đã ghi
- 🚀 **Tốc độ linh hoạt**: Phát lại với tốc độ bình thường, nhanh (2x) hoặc chậm (0.5x)
- 🔁 **Lặp lại macro**: Phát lại macro nhiều lần liên tiếp (1-100 lần)
- ⌨️ **Auto Type**: F7 để tự động gõ nội dung đã đặt trước
- 💾 **Lưu trữ**: Lưu macro vào file JSON để sử dụng lại
- 📊 **Thống kê**: Xem thống kê chi tiết về macro
- 🖥️ **Hai giao diện**: GUI với nút bấm hoặc Console menu
- 📸 **Chụp màn hình**: Hotkey F12 tự động bật, chụp màn hình nhanh
- 📁 **Quản lý screenshot**: Xem, quản lý và xóa screenshot cũ
- ⏹️ **Hotkey dừng**: Nhấn ESC để dừng phát lại macro
- ⏱️ **Timing chi tiết**: Lưu thông tin thời gian để phát lại mượt mà
- 🎛️ **Smoothness control**: Điều chỉnh độ mượt khi phát lại

## ⚡ Quick Start

**Cách nhanh nhất (Windows):**
```batch
# Chỉ cần click đúp file này:
run.bat
```

**Hoặc chạy GUI trực tiếp:**
```bash
pip install -r requirements.txt
python gui_app.py
```

## 🔧 Cài đặt

### Yêu cầu hệ thống
- Python 3.7+
- Windows/macOS/Linux
- Quyền truy cập chuột và bàn phím
- Tkinter (thường có sẵn với Python)

### Cài đặt thư viện

```bash
# Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

hoặc cài đặt từng thư viện:

```bash
pip install pynput pyautogui keyboard pillow
```

### Chạy ứng dụng

**Windows (dễ dàng):**
```batch
# Click đúp vào file run.bat
run.bat
```

**GUI Application (khuyên dùng):**
```bash
python gui_app.py
```

**Console Application:**
```bash
python main.py
```

**Demo screenshot:**
```bash
python test_screenshot.py
```

**Demo timing features:**
```bash
python test_timing.py
```

## 🚀 Hướng dẫn sử dụng

### 🖥️ Giao diện GUI (Khuyên dùng)
Chạy `python gui_app.py` để sử dụng giao diện với nút bấm:
- **Macro Controls**: Các nút ghi/phát lại macro
- **Screenshot Controls**: Quản lý chụp màn hình
- **Activity Log**: Xem log hoạt động trong thời gian thực
- **Status Bar**: Theo dõi trạng thái hiện tại

### 📟 Giao diện Console
Chạy `python main.py` để sử dụng menu truyền thống

### Ghi macro:
1. Chạy `python main.py`
2. Chọn `1` để bắt đầu ghi
3. Thực hiện các hành động cần ghi lại
4. Nhấn `F9` để dừng ghi và hỏi lưu (hoặc chọn `2` trong menu)
5. Chọn `3` để lưu macro vào file

### Phát lại macro:
1. Chọn `4` để tải macro từ file
2. Chọn `5` để phát lại với tốc độ bình thường
3. Hoặc chọn `6` (2x) hoặc `7` (0.5x) để điều chỉnh tốc độ
4. Nhấn `Ctrl+C` để dừng phát lại bất cứ lúc nào

### Chụp màn hình:
1. Hotkey tự động bật khi khởi động! 🔥
2. Nhấn `F12` bất cứ lúc nào để chụp màn hình
3. Chọn `10` để bật/tắt hotkey chụp màn hình
4. Chọn `12` để chụp màn hình ngay lập tức
5. Chọn `13` để xem danh sách screenshot
6. Chọn `14` để xóa screenshot cũ

### ⌨️ Phím tắt và hotkey:
- **F9**: Dừng ghi macro và hỏi có lưu không
- **F7**: Auto gõ nội dung đã đặt trước
- **F12**: Chụp màn hình (khi đã bật hotkey)
- **ESC**: Dừng phát lại macro (tính năng mới!)
- **Ctrl+C**: Dừng bất kỳ hoạt động nào

## 📝 Ví dụ sử dụng

### Tự động hóa công việc lặp lại:
- Điền form
- Thao tác trên phần mềm
- Game automation
- Testing UI

### Ghi macro mở ứng dụng:
1. Ghi macro mở Notepad
2. Lưu vào file `open_notepad.json`
3. Phát lại để mở Notepad tự động

### Chụp màn hình tự động:
1. Hotkey F12 tự động bật khi khởi động! 🔥
2. Làm việc bình thường, nhấn `F12` khi cần chụp màn hình
3. Screenshot tự động lưu trong folder `SCREENSHOT/`
4. Dùng cho: Báo lỗi, ghi lại kết quả, tạo tutorial

### Phát lại macro mượt mà:
1. Ghi macro với timing chính xác
2. File mới lưu thông tin chi tiết về thời gian
3. Điều chỉnh Smoothness trong GUI (0.1x - 2.0x):
   - **0.1x**: Rất chậm, chính xác tuyệt đối
   - **1.0x**: Tốc độ gốc, cân bằng
   - **2.0x**: Nhanh hơn, ít delay
4. Nhấn ESC để dừng phát lại bất cứ lúc nào

## ⚠️ Lưu ý quan trọng

- **Quyền truy cập**: Tool cần quyền truy cập chuột và bàn phím
- **Tọa độ màn hình**: Macro ghi lại tọa độ tuyệt đối, đảm bảo không thay đổi vị trí cửa sổ
- **An toàn**: Có thể dừng bất cứ lúc nào bằng `Ctrl+C`
- **Fail-safe**: PyAutoGUI có tính năng fail-safe khi di chuột vào góc màn hình

## 📁 Cấu trúc file

```
macro-recorder/
├── gui_app.py          # GUI Application (khuyên dùng)
├── main.py             # Console Application
├── macro_recorder.py   # Class chính xử lý ghi/phát lại
├── requirements.txt    # Danh sách thư viện cần thiết
├── install_and_run.py  # Script cài đặt tự động
├── test_screenshot.py  # Demo tính năng screenshot
├── test_timing.py      # Demo tính năng timing mới
├── run.bat            # Batch file cho Windows
├── README.md          # File hướng dẫn này
├── example_macro.json # File macro mẫu
├── *.json             # File macro đã lưu
└── SCREENSHOT/        # Folder chứa screenshot (tự tạo)
    └── screenshot_*.png # File screenshot theo timestamp
```

## 🔍 API Reference

### GUI Application
```python
python gui_app.py    # Chạy giao diện đồ họa
```

### Console Application  
```python
python main.py       # Chạy giao diện console
```

### MacroRecorder Class

```python
from macro_recorder import MacroRecorder

recorder = MacroRecorder()

# Ghi macro
recorder.start_recording()    # Bắt đầu ghi
recorder.stop_recording()     # Dừng ghi

# Lưu/tải macro
recorder.save_macro("my_macro.json")    # Lưu macro
recorder.load_macro("my_macro.json")    # Tải macro

# Phát lại
recorder.replay_macro(1.0)     # Tốc độ bình thường
recorder.replay_macro(2.0)     # Tốc độ 2x
recorder.replay_macro(0.5)     # Tốc độ 0.5x

# Thống kê
recorder.print_stats()         # In thống kê

# Screenshot
recorder.start_screenshot_hotkey()    # Bật hotkey F12
recorder.stop_screenshot_hotkey()     # Tắt hotkey
recorder.take_screenshot()            # Chụp màn hình ngay
recorder.list_screenshots()           # Liệt kê screenshot
recorder.cleanup_old_screenshots(7)   # Xóa screenshot cũ >7 ngày
```

## 🐛 Troubleshooting

### Lỗi thường gặp:

**"ModuleNotFoundError"**: Chưa cài đặt thư viện
```bash
pip install -r requirements.txt
```

**"Permission denied"**: Thiếu quyền truy cập
- Windows: Chạy với quyền Administrator
- macOS: Cấp quyền Accessibility trong System Preferences
- Linux: Chạy với sudo (nếu cần)

**Macro không chạy đúng**: 
- Đảm bảo màn hình ở cùng độ phân giải
- Không thay đổi vị trí cửa sổ
- Kiểm tra tốc độ phát lại

**Screenshot không hoạt động**:
- Kiểm tra quyền truy cập màn hình
- Đảm bảo có đủ dung lượng ổ cứng
- Folder SCREENSHOT sẽ được tạo tự động

## 📦 Build Executable (Tùy chọn)

Tạo file .exe độc lập:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy tạo issue hoặc pull request.

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🌟 Tính năng sắp tới

- [ ] GUI với Tkinter/PyQt
- [ ] Ghi macro có điều kiện
- [ ] Hỗ trợ hotkey tùy chỉnh
- [ ] Macro scheduler
- [ ] Image recognition
- [ ] Macro editor với timeline 