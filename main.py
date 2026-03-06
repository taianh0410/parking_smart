 
from gate_controller import GateController
from parking_lot_manager import ParkingLotManager
from web_dashboard import WebDashboard
from time import sleep
import signal
import sys

class SmartParkingSystem:
    
    
    def __init__(self):
        print("=" * 50)
        print("HỆ THỐNG BÃI ĐỖ XE THÔNG MINH")
        print("Raspberry Pi 3 B+ | Python + gpiozero")
        print("=" * 50)
        
        
        self.parking_manager = ParkingLotManager()
        
        
        self.gate_controller = GateController(
            on_vehicle_entered_callback=self.parking_manager.vehicle_entered
        )
        
       
        self.web_dashboard = WebDashboard(self.parking_manager)
        
        
        signal.signal(signal.SIGINT, self._signal_handler)
        
        print("\n Hệ thống đã sẵn sàng!")
        print(f" Truy cập dashboard tại: http://localhost:5000")
        print(" Bấm nút GPIO 21 để mở cổng\n")
    
    def _signal_handler(self, sig, frame):
        """Xử lý khi nhận tín hiệu thoát (Ctrl+C)"""
        print("\n\n[System] Đang tắt hệ thống...")
        self.cleanup()
        sys.exit(0)
    
    def run(self):
        
       
        self.web_dashboard.start()
        
        try:
            while True:
                
                self.gate_controller.update()
                
                
                sleep(0.1)
                
        except KeyboardInterrupt:
            print("\n[System] Nhận lệnh dừng từ bàn phím")
            self.cleanup()
    
    def cleanup(self):
         
        print("[System] Đang dọn dẹp tài nguyên...")
        self.gate_controller.cleanup()
        self.parking_manager.cleanup()
        print("[System] Hệ thống đã tắt an toàn.  ")


if __name__ == "__main__":
    # Khởi tạo và chạy hệ thống
    system = SmartParkingSystem()
    system.run()
