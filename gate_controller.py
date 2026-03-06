# gate_controller.py
# Điều khiển cổng vào với State Machine chống đếm sai

from gpiozero import Servo, Button, DistanceSensor
from time import sleep
from enum import Enum
import config

class GateState(Enum):
    """
    State Machine cho cổng vào
    - IDLE: Chờ người dùng bấm nút
    - GATE_OPENING: Đang mở cổng
    - WAITING_ENTRY: Chờ xe đi vào vùng cảm biến
    - VEHICLE_IN_ZONE: Xe đang ở trong vùng cảm biến
    - WAITING_EXIT: Chờ xe đi ra khỏi vùng cảm biến
    - GATE_CLOSING: Đang đóng cổng
    """
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
        # Khởi tạo phần cứng
        self.servo = Servo(config.SERVO_PIN)
        self.button = Button(config.BUTTON_PIN, bounce_time=config.DEBOUNCE_TIME)
        self.ultrasonic = DistanceSensor(
            echo=config.ULTRASONIC_ECHO,
            trigger=config.ULTRASONIC_TRIGGER,
            max_distance=4  # Tối đa 4m
        )
        
        # State Machine
        self.current_state = GateState.IDLE
        self.on_vehicle_entered = on_vehicle_entered_callback
        
        # Đăng ký sự kiện nút bấm
        self.button.when_pressed = self._on_button_pressed
        
        print("[GateController] Khởi tạo thành công")
    
    def _on_button_pressed(self):
        """Xử lý khi người dùng bấm nút (quẹt thẻ/lấy vé)"""
        if self.current_state == GateState.IDLE:
            print("[Gate] Nút được bấm - Bắt đầu mở cổng")
            self._open_gate()
    
    def _open_gate(self):
        """Mở cổng barie"""
        print("[Gate] Đang mở cổng...")
        self.current_state = GateState.GATE_OPENING
        
        # Mở servo 90 độ
        self.servo.max()  # Tương đương 90 độ
        sleep(1)  # Chờ servo mở hoàn toàn
        
        self.current_state = GateState.WAITING_ENTRY
        print("[Gate] Cổng đã mở - Chờ xe vào")
    
    def _close_gate(self):
        """Đóng cổng barie"""
        print("[Gate] Đang đóng cổng...")
        self.current_state = GateState.GATE_CLOSING
        
        # Đóng servo về 0 độ
        self.servo.min()  # Tương đương 0 độ
        sleep(1)  # Chờ servo đóng hoàn toàn
        
        self.current_state = GateState.IDLE
        print("[Gate] Cổng đã đóng - Sẵn sàng")
    
    def _get_distance(self):
        """Đọc khoảng cách từ cảm biến siêu âm (cm)"""
        try:
            distance_m = self.ultrasonic.distance
            distance_cm = distance_m * 100
            return distance_cm
        except:
            return 999  # Trả về giá trị lớn nếu lỗi
    
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
        self.servo.close()
        self.button.close()
        self.ultrasonic.close()
        print("[GateController] Đã dọn dẹp tài nguyên")
