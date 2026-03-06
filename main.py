# main.py
# Chương trình chính - Tích hợp tất cả module

from gate_controller import GateController
from parking_lot_manager import ParkingLotManager
from web_dashboard import WebDashboard
from time import sleep
import signal
import sys

class SmartParkingSystem:
    """
    Hệ thống bãi đỗ xe thông minh
    Tích hợp tất cả các module
    """
    
    def __init__(self):
        print("=" * 50)
        print("HỆ THỐNG BÃI ĐỖ XE THÔNG MINH")
        print("Raspberry Pi 3 B+ | Python + gpiozero")
        print("=" * 50)
        
        # Khởi tạo quản lý bãi đỗ
        self.parking_manager = ParkingLotManager()
        
        # Khởi tạo điều khiển cổng với callback
        self.gate_controller = GateController(
            on_vehicle_entered_callback=self.parking_manager.vehicle_entered
        )
        
        # Khởi tạo web dashboard
        self.web_dashboard = WebDashboard(self.parking_manager)
        
        # Đăng ký xử lý tín hiệu thoát (Ctrl+C)
        signal.signal(signal.SIGINT, self._signal_handler)
        
        print("\n✅ Hệ thống đã sẵn sàng!")
        print(f"📊 Truy cập dashboard tại: http://localhost:5000")
        print("🔘 Bấm nút GPIO 21 để mở cổng\n")
    
    def _signal_handler(self, sig, frame):
        """Xử lý khi nhận tín hiệu thoát (Ctrl+C)"""
        print("\n\n[System] Đang tắt hệ thống...")
        self.cleanup()
        sys.exit(0)
    
    def run(self):
        """
        Vòng lặp chính của hệ thống
        """
        # Khởi động web server
        self.web_dashboard.start()
        
        try:
            while True:
                # Cập nhật State Machine của cổng vào
                self.gate_controller.update()
                
                # Delay nhỏ để tránh CPU 100%
                sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n[System] Nhận lệnh dừng từ bàn phím")
            self.cleanup()
    
    def cleanup(self):
        """Dọn dẹp tài nguyên trước khi thoát"""
        print("[System] Đang dọn dẹp tài nguyên...")
        self.gate_controller.cleanup()
        self.parking_manager.cleanup()
        print("[System] Hệ thống đã tắt an toàn. Tạm biệt!")


if __name__ == "__main__":
    # Khởi tạo và chạy hệ thống
    system = SmartParkingSystem()
    system.run()
