# config.py
# Cấu hình GPIO và thông số hệ thống

# GPIO Pins (theo sơ đồ phần cứng)
SERVO_PIN = 6           # Động cơ Servo mở cổng Barie
ULTRASONIC_TRIGGER = 15 # Cảm biến siêu âm - TRIGGER
ULTRASONIC_ECHO = 4     # Cảm biến siêu âm - ECHO
IR_SENSOR_PIN = 22      # Cảm biến hồng ngoại IR (slot đỗ)
LED_PIN = 13            # Đèn LED báo trạng thái bãi đỗ
BUTTON_PIN = 21         # Nút bấm (mô phỏng quẹt thẻ/lấy vé)

# Thông số hệ thống
TOTAL_SLOTS = 5         # Tổng số chỗ đỗ xe
SERVO_OPEN_ANGLE = 90   # Góc mở servo (độ)
SERVO_CLOSE_ANGLE = 0   # Góc đóng servo (độ)
DISTANCE_THRESHOLD = 20 # Ngưỡng phát hiện xe (cm)
DEBOUNCE_TIME = 0.3     # Thời gian chống dội nút bấm (giây)
