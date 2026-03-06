 
# Quản lý toàn bộ bãi đỗ xe

from gpiozero import LED
from parking_slot import ParkingSlot
import config

class ParkingLotManager:
    
    
    def __init__(self):
        self.total_slots = config.TOTAL_SLOTS
        self.vehicles_inside = 0  
        
         
        self.status_led = LED(config.LED_PIN)
        
         
        self.slots = [
            ParkingSlot(slot_id=1, ir_pin=config.IR_SENSOR_PIN)
        ]
        
        print(f"[ParkingLot] Khởi tạo bãi đỗ: {self.total_slots} chỗ")
        self._update_led_status()
    
    def get_available_slots(self):
        
        return self.total_slots - self.vehicles_inside
    
    def is_full(self):
        
        return self.vehicles_inside >= self.total_slots
    
    def vehicle_entered(self):
        
        if not self.is_full():
            self.vehicles_inside += 1
            print(f"[ParkingLot] Xe vào bãi - Số xe hiện tại: {self.vehicles_inside}/{self.total_slots}")
            self._update_led_status()
        else:
            print("[ParkingLot] CẢNH BÁO: Bãi đã đầy!")
    
    def vehicle_exited(self):
         
        if self.vehicles_inside > 0:
            self.vehicles_inside -= 1
            print(f"[ParkingLot] Xe rời bãi - Số xe hiện tại: {self.vehicles_inside}/{self.total_slots}")
            self._update_led_status()
    
    def _update_led_status(self):
        
        if self.is_full():
            self.status_led.on()
            print("[LED] Bãi đầy - Đèn SÁNG")
        else:
            self.status_led.off()
            print("[LED] Còn chỗ trống - Đèn TẮT")
    
    def get_status_summary(self):
        
        return {
            'total_slots': self.total_slots,
            'occupied': self.vehicles_inside,
            'available': self.get_available_slots(),
            'is_full': self.is_full()
        }
    
    def cleanup(self):
        
        self.status_led.close()
        for slot in self.slots:
            slot.cleanup()
        print("[ParkingLot] Đã dọn dẹp tài nguyên")
