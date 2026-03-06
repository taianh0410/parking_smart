# parking_lot_manager.py - ESP32 Version
# Quản lý toàn bộ bãi đỗ xe

from machine import Pin
import config

class ParkingLotManager:
    """
    Quản lý toàn bộ bãi đỗ xe
    - Theo dõi số xe trong bãi
    - Điều khiển đèn LED báo trạng thái
    """
    
    def __init__(self):
        self.total_slots = config.TOTAL_SLOTS
        self.vehicles_inside = 0  # Số xe hiện tại trong bãi
        
        # Khởi tạo đèn LED báo trạng thái
        self.status_led = Pin(config.LED_PIN, Pin.OUT)
        self.status_led.value(0)  # Tắt LED ban đầu
        
        # Khởi tạo cảm biến IR cho slot (nếu có)
        self.ir_sensor = Pin(config.IR_SENSOR_PIN, Pin.IN, Pin.PULL_UP)
        
        print(f"[ParkingLot] Khởi tạo bãi đỗ: {self.total_slots} chỗ")
        self._update_led_status()
    
    def get_available_slots(self):
        """Trả về số chỗ trống"""
        return self.total_slots - self.vehicles_inside
    
    def is_full(self):
        """Kiểm tra bãi đỗ đã đầy chưa"""
        return self.vehicles_inside >= self.total_slots
    
    def vehicle_entered(self):
        """
        Xử lý khi có 1 xe vào bãi (được gọi từ GateController)
        """
        if not self.is_full():
            self.vehicles_inside += 1
            print(f"[ParkingLot] Xe vào bãi - Số xe hiện tại: {self.vehicles_inside}/{self.total_slots}")
            self._update_led_status()
        else:
            print("[ParkingLot] CẢNH BÁO: Bãi đã đầy!")
    
    def vehicle_exited(self):
        """
        Xử lý khi có 1 xe ra khỏi bãi
        """
        if self.vehicles_inside > 0:
            self.vehicles_inside -= 1
            print(f"[ParkingLot] Xe rời bãi - Số xe hiện tại: {self.vehicles_inside}/{self.total_slots}")
            self._update_led_status()
    
    def _update_led_status(self):
        """
        Cập nhật đèn LED báo trạng thái
        - Bãi đầy: LED sáng
        - Còn chỗ trống: LED tắt
        """
        if self.is_full():
            self.status_led.value(1)  # Bật LED
            print("[LED] Bãi đầy - Đèn SÁNG")
        else:
            self.status_led.value(0)  # Tắt LED
            print("[LED] Còn chỗ trống - Đèn TẮT")
    
    def get_status_summary(self):
        """
        Trả về thông tin tổng quan bãi đỗ
        """
        return {
            'total_slots': self.total_slots,
            'occupied': self.vehicles_inside,
            'available': self.get_available_slots(),
            'is_full': self.is_full()
        }
    
    def cleanup(self):
        """Dọn dẹp tài nguyên"""
        self.status_led.value(0)
        print("[ParkingLot] Đã dọn dẹp tài nguyên")
