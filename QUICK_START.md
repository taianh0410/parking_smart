# ⚡ QUICK START - Chạy Nhanh Trong 5 Phút

## Bước 1: Kết nối phần cứng

```
Servo      → GPIO 6  (+ 5V, GND)
Siêu âm    → GPIO 15 (TRIGGER), GPIO 4 (ECHO), 5V, GND
IR Sensor  → GPIO 22, 5V, GND
LED        → GPIO 13 (qua điện trở 220Ω), GND
Nút bấm    → GPIO 21, GND
```

⚠️ **LƯU Ý:** Chân ECHO của siêu âm cần điện trở phân áp 5V → 3.3V!

## Bước 2: Cài đặt thư viện

```bash
cd ~/smart-parking
pip3 install gpiozero Flask
```

## Bước 3: Test phần cứng

```bash
python3 TEST_HARDWARE.py
```

Đảm bảo tất cả linh kiện đều ✅ OK

## Bước 4: Chạy hệ thống

```bash
python3 main.py
```

## Bước 5: Mở web

Tìm IP:
```bash
hostname -I
```

Truy cập: `http://IP:5000`

## Test Nhanh

1. **Bấm nút** → Servo mở 90°
2. **Đưa tay vào cảm biến** → Phát hiện xe
3. **Rút tay ra** → Servo đóng, số xe +1
4. **Kiểm tra web** → Số chỗ trống giảm

## Test Chống Đếm Sai

1. Bấm nút → Cổng mở
2. Đưa tay vào
3. **Rút tay ra ngay** (xe lùi)
4. ✅ Số xe KHÔNG tăng

---

**Xem hướng dẫn chi tiết:** `HUONG_DAN_CAI_DAT.md`
