# main.py - ESP32 Version
# Chương trình chính cho ESP32

import network
import time
from gate_controller import GateController
from parking_lot_manager import ParkingLotManager
from web_server import WebServer
import config

class SmartParkingSystem:
    """
    Hệ thống bãi đỗ xe thông minh cho ESP32
    """
    
    def __init__(self):
        print("=" * 50)
        print("HỆ THỐNG BÃI ĐỖ XE THÔNG MINH")
        print("ESP32 | MicroPython")
        print("=" * 50)
        
        # Kết nối WiFi
        self.connect_wifi()
        
        # Khởi tạo quản lý bãi đỗ
        self.parking_manager = ParkingLotManager()
        
        # Khởi tạo điều khiển cổng với callback
        self.gate_controller = GateController(
            on_vehicle_entered_callback=self.parking_manager.vehicle_entered
        )
        
        # Khởi tạo web server
        self.web_server = WebServer(self.parking_manager, port=config.WEB_PORT)
        self.web_server.start()
        
        print("\n✅ Hệ thống đã sẵn sàng!")
        print(f"📊 Truy cập dashboard tại: http://{self.get_ip()}")
        print("🔘 Bấm nút để mở cổng\n")
    
    def connect_wifi(self):
        """Kết nối WiFi"""
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        
        if not wlan.isconnected():
            print(f"[WiFi] Đang kết nối đến {config.WIFI_SSID}...")
            wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
            
            # Chờ kết nối (timeout 10s)
            timeout = 10
            while not wlan.isconnected() and timeout > 0:
                time.sleep(1)
                timeout -= 1
                print(".", end="")
            
            print()
        
        if wlan.isconnected():
            print(f"[WiFi] Đã kết nối! IP: {wlan.ifconfig()[0]}")
            self.wlan = wlan
        else:
            print("[WiFi] CẢNH BÁO: Không thể kết nối WiFi!")
            self.wlan = None
    
    def get_ip(self):
        """Lấy địa chỉ IP"""
        if self.wlan and self.wlan.isconnected():
            return self.wlan.ifconfig()[0]
        return "N/A"
    
    def run(self):
        """
        Vòng lặp chính của hệ thống
        """
        try:
            while True:
                # Cập nhật State Machine của cổng vào
                self.gate_controller.update()
                
                # Xử lý web request (non-blocking)
                self.web_server.handle_request()
                
                # Delay nhỏ để tránh CPU 100%
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            print("\n[System] Nhận lệnh dừng")
            self.cleanup()
        except Exception as e:
            print(f"\n[System] Lỗi: {e}")
            self.cleanup()
    
    def cleanup(self):
        """Dọn dẹp tài nguyên trước khi thoát"""
        print("[System] Đang dọn dẹp tài nguyên...")
        self.gate_controller.cleanup()
        self.parking_manager.cleanup()
        self.web_server.cleanup()
        print("[System] Hệ thống đã tắt an toàn. Tạm biệt!")


# Khởi động hệ thống
if __name__ == "__main__":
    system = SmartParkingSystem()
    system.run()
