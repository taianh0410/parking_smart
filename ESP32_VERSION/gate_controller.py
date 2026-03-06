# gate_controller.py - ESP32 Version
# Điều khiển cổng vào với State Machine chống đếm sai

from machine import Pin, PWM, time_pulse_us
import time
import config

class GateState:
    """State Machine cho cổng vào"""
    IDLE = 1
    GATE_OPENING = 2
    WAITING_ENTRY = 3
    VEHICLE_IN_ZONE = 4
    WAITING_EXIT = 5
    GATE_CLOSING = 6


class GateController:
    """
    Điều khiển cổng vào với cơ chế chống đếm sai
    Sử dụng State Machine để đảm bảo xe phải đi qua hoàn toàn mới được tính
    """
    
    def __init__(self, on_vehicle_entered_callback=None):
        # Khởi tạo Servo (PWM)
        self.servo = PWM(Pin(config.SERVO_PIN), freq=50)
        
        # Khởi tạo nút bấm
        self.button = Pin(config.BUTTON_PIN, Pin.IN, Pin.PULL_UP)
        self.last_button_state = 1
        self.last_button_time = 0
        
        # Khởi tạo cảm biến siêu âm
        self.trigger = Pin(config.ULTRASONIC_TRIGGER, Pin.OUT)
        self.echo = Pin(config.ULTRASONIC_ECHO, Pin.IN)
        self.trigger.value(0)
        
        # State Machine
        self.current_state = GateState.IDLE
        self.on_vehicle_entered = on_vehicle_entered_callback
        
        # Đóng cổng ban đầu
        self._set_servo_angle(config.SERVO_CLOSE_ANGLE)
        
        print("[GateController] Khởi tạo thành công")
    
    def _set_servo_angle(self, angle):
        """
        Điều khiển góc servo (0-180 độ)
        Duty cycle: 0° = 26, 90° = 77, 180° = 128
        """
        duty = int(26 + (angle / 180) * 102)
        self.servo.duty(duty)
    
    def _check_button(self):
        """Kiểm tra nút bấm với debounce"""
        current_state = self.button.value()
        current_time = time.ticks_ms()
        
        # Phát hiện cạnh xuống (nút được bấm)
        if current_state == 0 and self.last_button_state == 1:
            if time.ticks_diff(current_time, self.last_button_time) > config.DEBOUNCE_TIME:
                self.last_button_time = current_time
                self.last_button_state = current_state
                return True
        
        self.last_button_state = current_state
        return False
    
    def _open_gate(self):
        """Mở cổng barie"""
        print("[Gate] Đang mở cổng...")
        self.current_state = GateState.GATE_OPENING
        
        # Mở servo 90 độ
        self._set_servo_angle(config.SERVO_OPEN_ANGLE)
        time.sleep(1)  # Chờ servo mở hoàn toàn
        
        self.current_state = GateState.WAITING_ENTRY
        print("[Gate] Cổng đã mở - Chờ xe vào")
    
    def _close_gate(self):
        """Đóng cổng barie"""
        print("[Gate] Đang đóng cổng...")
        self.current_state = GateState.GATE_CLOSING
        
        # Đóng servo về 0 độ
        self._set_servo_angle(config.SERVO_CLOSE_ANGLE)
        time.sleep(1)  # Chờ servo đóng hoàn toàn
        
        self.current_state = GateState.IDLE
        print("[Gate] Cổng đã đóng - Sẵn sàng")
    
    def _get_distance(self):
        """
        Đọc khoảng cách từ cảm biến siêu âm (cm)
        """
        try:
            # Gửi xung trigger
            self.trigger.value(0)
            time.sleep_us(2)
            self.trigger.value(1)
            time.sleep_us(10)
            self.trigger.value(0)
            
            # Đo thời gian xung echo
            pulse_time = time_pulse_us(self.echo, 1, 30000)  # Timeout 30ms
            
            if pulse_time < 0:
                return 999  # Timeout
            
            # Tính khoảng cách: distance = (time * speed_of_sound) / 2
            # speed_of_sound = 343 m/s = 0.0343 cm/µs
            distance = (pulse_time * 0.0343) / 2
            return distance
        except:
            return 999
    
    def _is_vehicle_detected(self):
        """Kiểm tra có xe trong vùng cảm biến không"""
        distance = self._get_distance()
        return distance < config.DISTANCE_THRESHOLD
    
    def update(self):
        """
        Cập nhật State Machine (gọi liên tục trong vòng lặp chính)
        
        Logic chống đếm sai:
        1. WAITING_ENTRY: Chờ xe đi VÀO vùng cảm biến
        2. VEHICLE_IN_ZONE: Xe đang Ở TRONG vùng cảm biến
        3. WAITING_EXIT: Chờ xe đi RA KHỎI vùng cảm biến
        
        Chỉ khi xe đi qua cả 3 trạng thái này mới được tính là 1 lượt vào hợp lệ
        """
        
        # Kiểm tra nút bấm
        if self.current_state == GateState.IDLE:
            if self._check_button():
                print("[Gate] Nút được bấm - Bắt đầu mở cổng")
                self._open_gate()
        
        # State Machine xử lý xe đi qua
        if self.current_state == GateState.WAITING_ENTRY:
            # Chờ xe đi vào vùng cảm biến
            if self._is_vehicle_detected():
                print("[Gate] Phát hiện xe đi vào vùng cảm biến")
                self.current_state = GateState.VEHICLE_IN_ZONE
        
        elif self.current_state == GateState.VEHICLE_IN_ZONE:
            # Xe đang ở trong vùng cảm biến
            if not self._is_vehicle_detected():
                # Xe đã ra khỏi vùng cảm biến
                print("[Gate] Xe đã đi qua cổng hoàn toàn")
                self.current_state = GateState.WAITING_EXIT
                
                # Gửi tín hiệu: 1 xe đã vào bãi (hợp lệ)
                if self.on_vehicle_entered:
                    self.on_vehicle_entered()
                
                # Đóng cổng
                self._close_gate()
    
    def cleanup(self):
        """Dọn dẹp tài nguyên"""
        self.servo.deinit()
        print("[GateController] Đã dọn dẹp tài nguyên")
