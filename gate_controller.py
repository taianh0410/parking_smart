 
from gpiozero import Servo, Button, DistanceSensor
from time import sleep
from enum import Enum
import config

class GateState(Enum):
     
    IDLE = 1
    GATE_OPENING = 2
    WAITING_ENTRY = 3
    VEHICLE_IN_ZONE = 4
    WAITING_EXIT = 5
    GATE_CLOSING = 6


class GateController:
    
    
    def __init__(self, on_vehicle_entered_callback=None):
         
        self.servo = Servo(config.SERVO_PIN)
        self.button = Button(config.BUTTON_PIN, bounce_time=config.DEBOUNCE_TIME)
        self.ultrasonic = DistanceSensor(
            echo=config.ULTRASONIC_ECHO,
            trigger=config.ULTRASONIC_TRIGGER,
            max_distance=4  # Tối đa 4m
        )
        
       
        self.current_state = GateState.IDLE
        self.on_vehicle_entered = on_vehicle_entered_callback
        
       
        self.button.when_pressed = self._on_button_pressed
        
        print("[GateController] Khởi tạo thành công")
    
    def _on_button_pressed(self):
        
        if self.current_state == GateState.IDLE:
            print("[Gate] Nút được bấm - Bắt đầu mở cổng")
            self._open_gate()
    
    def _open_gate(self):
         
        print("[Gate] Đang mở cổng...")
        self.current_state = GateState.GATE_OPENING
        
      
        self.servo.max()   
        sleep(1)   
        
        self.current_state = GateState.WAITING_ENTRY
        print("[Gate] Cổng đã mở - Chờ xe vào")
    
    def _close_gate(self):
        """Đóng cổng barie"""
        print("[Gate] Đang đóng cổng...")
        self.current_state = GateState.GATE_CLOSING
        
     
        self.servo.min()   
        sleep(1)  
        
        self.current_state = GateState.IDLE
        print("[Gate] Cổng đã đóng - Sẵn sàng")
    
    def _get_distance(self):
         
        try:
            distance_m = self.ultrasonic.distance
            distance_cm = distance_m * 100
            return distance_cm
        except:
            return 999  # Trả về giá trị lớn nếu lỗi
    
    def _is_vehicle_detected(self):
         
        distance = self._get_distance()
        return distance < config.DISTANCE_THRESHOLD
    
    def update(self):
        
        
        if self.current_state == GateState.WAITING_ENTRY:
           
            if self._is_vehicle_detected():
                print("[Gate] Phát hiện xe đi vào vùng cảm biến")
                self.current_state = GateState.VEHICLE_IN_ZONE
        
        elif self.current_state == GateState.VEHICLE_IN_ZONE:
            
            if not self._is_vehicle_detected():
                 
                print("[Gate] Xe đã đi qua cổng hoàn toàn")
                self.current_state = GateState.WAITING_EXIT
                
              
                if self.on_vehicle_entered:
                    self.on_vehicle_entered()
                
                
                self._close_gate()
    
    def cleanup(self):
         
        self.servo.close()
        self.button.close()
        self.ultrasonic.close()
        print("[GateController] Đã dọn dẹp tài nguyên")
