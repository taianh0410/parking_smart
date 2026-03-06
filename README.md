# 🚗 Hệ Thống Bãi Đỗ Xe Thông Minh

Dự án IoT sử dụng Raspberry Pi 3 B+ để quản lý bãi đỗ xe tự động với cơ chế chống đếm sai.

## 📋 Tính Năng

- ✅ Tự động mở/đóng cổng barie khi quẹt thẻ
- ✅ Phát hiện xe qua cổng bằng cảm biến siêu âm
- ✅ **State Machine chống đếm sai** - Xe phải đi qua hoàn toàn mới được tính
- ✅ Theo dõi số chỗ trống real-time
- ✅ Đèn LED báo trạng thái bãi đầy
- ✅ Web Dashboard hiển thị trạng thái

## 🔌 Sơ Đồ Kết Nối GPIO

| Thiết bị | GPIO Pin |
|----------|----------|
| Servo (Barie) | GPIO 6 |
| Siêu âm TRIGGER | GPIO 15 |
| Siêu âm ECHO | GPIO 4 |
| Cảm biến IR | GPIO 22 |
| LED trạng thái | GPIO 13 |
| Nút bấm | GPIO 21 |

## 🏗️ Kiến Trúc Code (OOP)

```
SmartParkingSystem
├── GateController          # Điều khiển cổng + State Machine
├── ParkingLotManager       # Quản lý bãi đỗ
├── ParkingSlot             # Quản lý từng chỗ đỗ
└── WebDashboard            # Web server Flask
```

## 🔄 State Machine (Chống Đếm Sai)

```
IDLE → GATE_OPENING → WAITING_ENTRY → VEHICLE_IN_ZONE → WAITING_EXIT → GATE_CLOSING → IDLE
```

**Logic chống đếm sai:**
1. Xe phải đi VÀO vùng cảm biến (WAITING_ENTRY → VEHICLE_IN_ZONE)
2. Sau đó đi RA KHỎI vùng cảm biến (VEHICLE_IN_ZONE → WAITING_EXIT)
3. Chỉ khi đó mới tính là 1 lượt vào hợp lệ

**Trường hợp KHÔNG được đếm:**
- Xe tiến vào rồi lùi ra → KHÔNG tăng số xe

## 📦 Cài Đặt

### 1. Cài đặt thư viện

```bash
pip3 install -r requirements.txt
```

### 2. Test phần cứng (QUAN TRỌNG!)

Trước khi chạy hệ thống chính, test từng linh kiện:

```bash
python3 TEST_HARDWARE.py
```

Script này sẽ kiểm tra:
- ✅ Servo quay được không
- ✅ Nút bấm hoạt động không
- ✅ Cảm biến siêu âm đo được khoảng cách không
- ✅ Cảm biến IR phát hiện vật cản không
- ✅ LED sáng/tắt được không

### 3. Chạy chương trình chính

```bash
python3 main.py
```

### 4. Truy cập Dashboard

Mở trình duyệt và truy cập:
```
http://localhost:5000
```

Hoặc từ thiết bị khác trong cùng mạng:
```
http://<IP_của_Raspberry_Pi>:5000
```

**Tìm IP của Raspberry Pi:**
```bash
hostname -I
```

## 🎯 Cách Sử Dụng

1. Khởi động hệ thống: `python3 main.py`
2. Bấm nút GPIO 21 (mô phỏng quẹt thẻ)
3. Servo mở cổng 90°
4. Xe đi vào → Hệ thống phát hiện bằng cảm biến siêu âm
5. Xe đi qua hoàn toàn → Cổng tự động đóng
6. Số xe trong bãi tăng lên
7. Dashboard tự động cập nhật

## 📁 Cấu Trúc Thư Mục

```
smart-parking/
├── main.py                 # Chương trình chính
├── config.py               # Cấu hình GPIO
├── gate_controller.py      # Điều khiển cổng + State Machine
├── parking_lot_manager.py  # Quản lý bãi đỗ
├── parking_slot.py         # Quản lý slot đỗ
├── web_dashboard.py        # Web server
├── templates/
│   └── index.html         # Giao diện web
├── requirements.txt        # Thư viện Python
└── README.md              # File này
```

## 🧪 Test Hệ Thống

### Test cơ bản:
1. Bấm nút → Cổng mở
2. Đưa tay vào vùng cảm biến siêu âm (< 20cm)
3. Rút tay ra → Cổng đóng, số xe tăng

### Test chống đếm sai:
1. Bấm nút → Cổng mở
2. Đưa tay vào vùng cảm biến
3. **Rút tay ra ngay** (mô phỏng xe lùi)
4. ✅ Số xe KHÔNG tăng (chống đếm sai thành công)

## 🛠️ Tùy Chỉnh

Chỉnh sửa file `config.py`:

```python
TOTAL_SLOTS = 5              # Số chỗ đỗ
DISTANCE_THRESHOLD = 20      # Ngưỡng phát hiện xe (cm)
SERVO_OPEN_ANGLE = 90        # Góc mở servo
```

## 📝 Ghi Chú Quan Trọng

- Đảm bảo Raspberry Pi đã enable GPIO
- Cảm biến siêu âm hoạt động tốt trong khoảng 2cm - 400cm
- Servo cần nguồn 5V riêng nếu dùng servo lớn
- Web dashboard tự động cập nhật mỗi 2 giây

## 👨‍🎓 Sinh Viên Thực Hiện

- Dự án: Bãi Đỗ Xe Thông Minh
- Nền tảng: Raspberry Pi 3 B+
- Ngôn ngữ: Python 3
- Thư viện: gpiozero, Flask

## 📄 License

Dự án học tập - Tự do sử dụng cho mục đích giáo dục
