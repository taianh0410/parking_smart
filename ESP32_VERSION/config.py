# config.py - ESP32/ESP8266 Version
# Cấu hình GPIO và thông số hệ thống cho ESP32

# GPIO Pins (ESP32)
SERVO_PIN = 13          # Động cơ Servo mở cổng Barie
ULTRASONIC_TRIGGER = 5  # Cảm biến siêu âm - TRIGGER
ULTRASONIC_ECHO = 18    # Cảm biến siêu âm - ECHO
IR_SENSOR_PIN = 19      # Cảm biến hồng ngoại IR (slot đỗ)
LED_PIN = 2             # Đèn LED báo trạng thái (LED onboard ESP32)
BUTTON_PIN = 4          # Nút bấm (mô phỏng quẹt thẻ/lấy vé)

# Thông số hệ thống
TOTAL_SLOTS = 5         # Tổng số chỗ đỗ xe
SERVO_OPEN_ANGLE = 90   # Góc mở servo (độ)
SERVO_CLOSE_ANGLE = 0   # Góc đóng servo (độ)
DISTANCE_THRESHOLD = 20 # Ngưỡng phát hiện xe (cm)
DEBOUNCE_TIME = 300     # Thời gian chống dội nút bấm (ms)

# WiFi Configuration
WIFI_SSID = "YourWiFiName"      # Tên WiFi
WIFI_PASSWORD = "YourPassword"   # Mật khẩu WiFi
WEB_PORT = 80                    # Port web server
