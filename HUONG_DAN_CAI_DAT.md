# 📘 HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY HỆ THỐNG TRÊN RASPBERRY PI

## 🎯 Mục Tiêu
Hướng dẫn chi tiết từng bước để chạy hệ thống bãi đỗ xe thông minh trên Raspberry Pi 3 B+

---

## 📋 BƯỚC 1: CHUẨN BỊ PHẦN CỨNG

### 1.1. Danh Sách Linh Kiện

| STT | Linh Kiện | Số Lượng | Ghi Chú |
|-----|-----------|----------|---------|
| 1 | Raspberry Pi 3 B+ | 1 | Đã cài Raspbian OS |
| 2 | Servo SG90 (hoặc tương tự) | 1 | Động cơ mở cổng barie |
| 3 | Cảm biến siêu âm HC-SR04 | 1 | Phát hiện xe qua cổng |
| 4 | Cảm biến hồng ngoại IR | 1 | Phát hiện xe trong slot |
| 5 | LED 5mm | 1 | Báo trạng thái bãi đầy |
| 6 | Nút bấm (Push Button) | 1 | Mô phỏng quẹt thẻ |
| 7 | Điện trở 220Ω | 1 | Cho LED |
| 8 | Điện trở 10kΩ | 1 | Pull-down cho nút bấm |
| 9 | Breadboard | 1 | Kết nối mạch |
| 10 | Dây jumper | 20+ | Kết nối |

### 1.2. Sơ Đồ Kết Nối GPIO

```
┌─────────────────────────────────────────────────┐
│           RASPBERRY PI 3 B+ GPIO                │
├─────────────────────────────────────────────────┤
│ GPIO 6  ──→ Servo (Dây tín hiệu - Màu vàng)   │
│ 5V      ──→ Servo (Dây nguồn - Màu đỏ)        │
│ GND     ──→ Servo (Dây đất - Màu nâu)         │
├─────────────────────────────────────────────────┤
│ GPIO 15 ──→ HC-SR04 TRIGGER                    │
│ GPIO 4  ──→ HC-SR04 ECHO                       │
│ 5V      ──→ HC-SR04 VCC                        │
│ GND     ──→ HC-SR04 GND                        │
├─────────────────────────────────────────────────┤
│ GPIO 22 ──→ IR Sensor OUT                      │
│ 5V      ──→ IR Sensor VCC                      │
│ GND     ──→ IR Sensor GND                      │
├─────────────────────────────────────────────────┤
│ GPIO 13 ──→ LED (Chân dương qua điện trở 220Ω)│
│ GND     ──→ LED (Chân âm)                      │
├─────────────────────────────────────────────────┤
│ GPIO 21 ──→ Nút bấm (1 chân)                   │
│ GND     ──→ Nút bấm (chân còn lại)             │
└─────────────────────────────────────────────────┘
```

### 1.3. Lưu Ý Quan Trọng

⚠️ **Cảm biến siêu âm HC-SR04:**
- Chân ECHO xuất ra 5V, nhưng GPIO Raspberry Pi chỉ chịu được 3.3V
- **PHẢI dùng điện trở phân áp** hoặc module chuyển đổi mức logic
- Sơ đồ phân áp đơn giản:
  ```
  ECHO ──[R1: 1kΩ]──┬──→ GPIO 4
                    │
                  [R2: 2kΩ]
                    │
                   GND
  ```

⚠️ **Servo:**
- Nếu dùng servo lớn (>9g), cần nguồn 5V riêng (không lấy từ Pi)
- Servo SG90 nhỏ có thể lấy nguồn trực tiếp từ 5V của Pi

---

## 🖥️ BƯỚC 2: CHUẨN BỊ RASPBERRY PI

### 2.1. Cập Nhật Hệ Thống

Mở Terminal trên Raspberry Pi và chạy:

```bash
sudo apt update
sudo apt upgrade -y
```

### 2.2. Cài Đặt Python 3 và pip

```bash
# Kiểm tra Python đã cài chưa
python3 --version

# Cài pip nếu chưa có
sudo apt install python3-pip -y
```

### 2.3. Cài Đặt Git (nếu chưa có)

```bash
sudo apt install git -y
```

---

## 📦 BƯỚC 3: TẢI CODE VỀ RASPBERRY PI

### Cách 1: Dùng Git (Nếu code đã push lên GitHub)

```bash
cd ~
git clone https://github.com/your-username/smart-parking.git
cd smart-parking
```

### Cách 2: Tải Trực Tiếp (Nếu chưa có Git repo)

**Trên máy tính:**
1. Nén toàn bộ thư mục code thành file `smart-parking.zip`
2. Dùng WinSCP hoặc FileZilla để copy vào Raspberry Pi

**Trên Raspberry Pi:**
```bash
cd ~
unzip smart-parking.zip
cd smart-parking
```

### Cách 3: Tạo Thủ Công (Nếu chưa có code)

```bash
# Tạo thư mục dự án
mkdir ~/smart-parking
cd ~/smart-parking

# Tạo thư mục templates
mkdir templates

# Tạo các file (copy nội dung từ code đã viết)
nano config.py
nano gate_controller.py
nano parking_lot_manager.py
nano parking_slot.py
nano web_dashboard.py
nano main.py
nano requirements.txt
nano templates/index.html
```

---

## 🔧 BƯỚC 4: CÀI ĐẶT THỨ VIỆN PYTHON

### 4.1. Cài Đặt Thư Viện

```bash
cd ~/smart-parking
pip3 install -r requirements.txt
```

Hoặc cài thủ công:

```bash
pip3 install gpiozero
pip3 install Flask
```

### 4.2. Kiểm Tra Cài Đặt

```bash
python3 -c "import gpiozero; print('gpiozero OK')"
python3 -c "import flask; print('Flask OK')"
```

Nếu thấy "OK" là thành công!

---

## ▶️ BƯỚC 5: CHẠY CHƯƠNG TRÌNH

### 5.1. Chạy Lần Đầu (Test)

```bash
cd ~/smart-parking
python3 main.py
```

**Kết quả mong đợi:**
```
==================================================
HỆ THỐNG BÃI ĐỖ XE THÔNG MINH
Raspberry Pi 3 B+ | Python + gpiozero
==================================================
[ParkingLot] Khởi tạo bãi đỗ: 5 chỗ
[LED] Còn chỗ trống - Đèn TẮT
[Slot 1] Khởi tạo tại GPIO 22
[GateController] Khởi tạo thành công
[WebDashboard] Khởi tạo tại http://0.0.0.0:5000

✅ Hệ thống đã sẵn sàng!
📊 Truy cập dashboard tại: http://localhost:5000
🔘 Bấm nút GPIO 21 để mở cổng
```

### 5.2. Truy Cập Web Dashboard

**Trên chính Raspberry Pi:**
- Mở trình duyệt Chromium
- Truy cập: `http://localhost:5000`

**Từ máy tính/điện thoại khác (cùng mạng WiFi):**
1. Tìm IP của Raspberry Pi:
   ```bash
   hostname -I
   ```
   Ví dụ: `192.168.1.100`

2. Truy cập: `http://192.168.1.100:5000`

### 5.3. Test Chức Năng

**Test 1: Nút bấm**
- Bấm nút GPIO 21
- Servo phải quay 90° (mở cổng)
- Terminal hiển thị: `[Gate] Nút được bấm - Bắt đầu mở cổng`

**Test 2: Cảm biến siêu âm**
- Đưa tay vào trước cảm biến (< 20cm)
- Terminal hiển thị: `[Gate] Phát hiện xe đi vào vùng cảm biến`
- Rút tay ra
- Terminal hiển thị: `[Gate] Xe đã đi qua cổng hoàn toàn`
- Servo đóng lại (0°)
- Số xe tăng lên: `[ParkingLot] Xe vào bãi - Số xe hiện tại: 1/5`

**Test 3: Chống đếm sai**
- Bấm nút mở cổng
- Đưa tay vào cảm biến
- **Rút tay ra ngay** (mô phỏng xe lùi)
- ✅ Số xe KHÔNG tăng (chống đếm sai thành công!)

**Test 4: Web Dashboard**
- Mở web `http://IP:5000`
- Kiểm tra số chỗ trống hiển thị đúng
- Bấm nút → Xe vào → Web tự động cập nhật sau 2 giây

---

## 🚀 BƯỚC 6: CHẠY TỰ ĐỘNG KHI KHỞI ĐỘNG

### 6.1. Tạo Service Systemd

```bash
sudo nano /etc/systemd/system/smart-parking.service
```

Dán nội dung sau:

```ini
[Unit]
Description=Smart Parking System
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/smart-parking
ExecStart=/usr/bin/python3 /home/pi/smart-parking/main.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 6.2. Kích Hoạt Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Kích hoạt service
sudo systemctl enable smart-parking.service

# Khởi động service
sudo systemctl start smart-parking.service

# Kiểm tra trạng thái
sudo systemctl status smart-parking.service
```

### 6.3. Các Lệnh Quản Lý Service

```bash
# Dừng service
sudo systemctl stop smart-parking.service

# Khởi động lại service
sudo systemctl restart smart-parking.service

# Xem log
sudo journalctl -u smart-parking.service -f
```

---

## 🔍 BƯỚC 7: KHẮC PHỤC SỰ CỐ

### Lỗi 1: "ModuleNotFoundError: No module named 'gpiozero'"

**Nguyên nhân:** Chưa cài thư viện

**Giải pháp:**
```bash
pip3 install gpiozero
```

### Lỗi 2: "Permission denied" khi chạy

**Nguyên nhân:** Không có quyền truy cập GPIO

**Giải pháp:**
```bash
# Thêm user vào group gpio
sudo usermod -a -G gpio pi

# Hoặc chạy với sudo (không khuyến khích)
sudo python3 main.py
```

### Lỗi 3: Servo không quay

**Nguyên nhân:** 
- Kết nối sai chân
- Nguồn không đủ

**Giải pháp:**
1. Kiểm tra lại kết nối GPIO 6
2. Dùng nguồn 5V riêng cho servo
3. Test servo đơn giản:
   ```python
   from gpiozero import Servo
   servo = Servo(6)
   servo.max()  # Quay 90°
   ```

### Lỗi 4: Cảm biến siêu âm không hoạt động

**Nguyên nhân:**
- Chưa phân áp cho chân ECHO
- Kết nối sai

**Giải pháp:**
1. Kiểm tra điện trở phân áp
2. Test cảm biến:
   ```python
   from gpiozero import DistanceSensor
   sensor = DistanceSensor(echo=4, trigger=15)
   while True:
       print(f"Distance: {sensor.distance * 100:.1f} cm")
       time.sleep(1)
   ```

### Lỗi 5: Web không truy cập được

**Nguyên nhân:**
- Firewall chặn port 5000
- Sai IP

**Giải pháp:**
```bash
# Kiểm tra IP
hostname -I

# Mở port 5000 (nếu có firewall)
sudo ufw allow 5000

# Kiểm tra Flask đang chạy
ps aux | grep python
```

---

## 📊 BƯỚC 8: TÙY CHỈNH HỆ THỐNG

### 8.1. Thay Đổi Số Chỗ Đỗ

Sửa file `config.py`:
```python
TOTAL_SLOTS = 10  # Thay đổi từ 5 thành 10
```

### 8.2. Thay Đổi Ngưỡng Phát Hiện Xe

Sửa file `config.py`:
```python
DISTANCE_THRESHOLD = 30  # Tăng từ 20cm lên 30cm
```

### 8.3. Thay Đổi Port Web

Sửa file `web_dashboard.py`:
```python
def __init__(self, parking_manager, host='0.0.0.0', port=8080):  # Đổi từ 5000 sang 8080
```

---

## 📸 BƯỚC 9: DEMO VÀ BẢO VỆ ĐỒ ÁN

### 9.1. Chuẩn Bị Demo

1. **Kiểm tra kết nối:** Đảm bảo tất cả linh kiện hoạt động
2. **Chạy hệ thống:** `python3 main.py`
3. **Mở web dashboard:** Hiển thị trên màn hình lớn
4. **Chuẩn bị kịch bản:**
   - Demo 1: Xe vào bình thường
   - Demo 2: Xe lùi lại (chống đếm sai)
   - Demo 3: Bãi đầy (LED sáng)

### 9.2. Các Câu Hỏi Thường Gặp Khi Bảo Vệ

**Q: Tại sao dùng State Machine?**
A: Để chống đếm sai. Xe phải đi qua 3 trạng thái: VÀO → TRONG → RA mới được tính.

**Q: Nếu 2 xe vào cùng lúc thì sao?**
A: Hệ thống chỉ mở cổng khi có người bấm nút, nên mỗi lần chỉ 1 xe vào.

**Q: Làm sao biết bãi đầy?**
A: LED GPIO 13 sẽ sáng khi bãi đầy. Web dashboard cũng hiển thị "Bãi đầy".

**Q: Có thể mở rộng thêm chức năng gì?**
A: 
- Thêm camera nhận diện biển số
- Gửi thông báo qua Telegram
- Lưu lịch sử ra/vào database
- Tính tiền đỗ xe tự động

---

## ✅ CHECKLIST HOÀN THÀNH

- [ ] Đã kết nối đúng tất cả linh kiện theo sơ đồ GPIO
- [ ] Đã cài đặt Python 3 và pip
- [ ] Đã cài đặt thư viện gpiozero và Flask
- [ ] Đã tải code về Raspberry Pi
- [ ] Chạy được `python3 main.py` không lỗi
- [ ] Nút bấm hoạt động → Servo quay
- [ ] Cảm biến siêu âm phát hiện vật thể
- [ ] Web dashboard truy cập được
- [ ] Test chống đếm sai thành công
- [ ] LED sáng khi bãi đầy
- [ ] Đã tạo service tự động chạy (tùy chọn)

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, kiểm tra:
1. Terminal có báo lỗi gì không?
2. Kết nối GPIO đúng chưa?
3. Thư viện đã cài đủ chưa?
4. Nguồn điện đủ mạnh không?

**Chúc bạn thành công với đồ án! 🎉**
