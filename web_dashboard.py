# web_dashboard.py
# Web Dashboard hiển thị trạng thái bãi đỗ

from flask import Flask, render_template, jsonify
import threading

class WebDashboard:
    """
    Web Server hiển thị trạng thái bãi đỗ
    Sử dụng Flask để tạo dashboard đơn giản
    """
    
    def __init__(self, parking_manager, host='0.0.0.0', port=5000):
        self.parking_manager = parking_manager
        self.host = host
        self.port = port
        
        # Khởi tạo Flask app
        self.app = Flask(__name__)
        
        # Đăng ký routes
        self._setup_routes()
        
        print(f"[WebDashboard] Khởi tạo tại http://{host}:{port}")
    
    def _setup_routes(self):
        """Thiết lập các routes cho web"""
        
        @self.app.route('/')
        def index():
            """Trang chủ hiển thị dashboard"""
            return render_template('index.html')
        
        @self.app.route('/api/status')
        def get_status():
            """API trả về trạng thái bãi đỗ (JSON)"""
            status = self.parking_manager.get_status_summary()
            return jsonify(status)
    
    def start(self):
        """
        Khởi động web server trong thread riêng
        Để không block main loop
        """
        def run_server():
            self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        print(f"[WebDashboard] Server đang chạy tại http://{self.host}:{self.port}")
