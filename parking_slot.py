# parking_slot.py
# Quản lý từng chỗ đỗ xe

from gpiozero import InputDevice
import config

class ParkingSlot:
    """
    Đại diện cho 1 chỗ đỗ xe
    Sử dụng cảm biến IR để phát hiện xe
    """
    
    def __init__(self, slot_id, ir_pin):
        self.slot_id = slot_id
        self.ir_sensor = InputDevice(ir_pin, pull_up=True)
        self._occupied = False
        
        print(f"[Slot {slot_id}] Khởi tạo tại GPIO {ir_pin}")
    
    def is_occupied(self):
        """
        Kiểm tra chỗ đỗ có xe không
        IR sensor: LOW (0) = có vật cản (có xe), HIGH (1) = không có xe
        """
        # Đọc trạng thái cảm biến IR
        sensor_value = self.ir_sensor.value
        
        # IR sensor thường trả về 0 khi phát hiện vật cản
        self._occupied = (sensor_value == 0)
        return self._occupied
    
    def get_status(self):
        """Trả về trạng thái slot dạng text"""
        return "Có xe" if self.is_occupied() else "Trống"
    
    def cleanup(self):
        """Dọn dẹp tài nguyên"""
        self.ir_sensor.close()
