# parking_lot_manager.py
# Quản lý toàn bộ bãi đỗ xe

from gpiozero import LED
from parking_slot import ParkingSlot
import config

class ParkingLotManager:
    """
    Quản lý toàn bộ bãi đỗ xe
    - Theo dõi số xe trong bãi
    - Quản lý các slot đỗ
    - Điều khiển đèn LED báo trạng thái
    """
    
    def __init__(self):
        self.total_slots = config.TOTAL_SLOTS
        self.vehicles_inside = 0  # Số xe hiện tại trong bãi
        
        # Khởi tạo đèn LED báo trạng thái
        self.status_led = LED(config.LED_PIN)
        
        # Khởi tạo các slot đỗ (demo với 1 cảm biến IR)
        # Trong thực tế, mỗi slot cần 1 cảm biến riêng
        self.slots = [
            ParkingSlot(slot_id=1, ir_pin=config.IR_SENSOR_PIN)
        ]
        
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
            self.status_led.on()
            print("[LED] Bãi đầy - Đèn SÁNG")
        else:
            self.status_led.off()
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
        self.status_led.close()
        for slot in self.slots:
            slot.cleanup()
        print("[ParkingLot] Đã dọn dẹp tài nguyên")
