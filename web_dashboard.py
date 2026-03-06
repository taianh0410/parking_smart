 
# Web Dashboard hiển thị trạng thái bãi đỗ

from flask import Flask, render_template, jsonify
import threading

class WebDashboard:
   
    
    def __init__(self, parking_manager, host='0.0.0.0', port=5000):
        self.parking_manager = parking_manager
        self.host = host
        self.port = port
        
        
        self.app = Flask(__name__)
        
       
        self._setup_routes()
        
        print(f"[WebDashboard] Khởi tạo tại http://{host}:{port}")
    
    def _setup_routes(self):
     
        
        @self.app.route('/')
        def index():
            
            return render_template('index.html')
        
        @self.app.route('/api/status')
        def get_status():
           
            status = self.parking_manager.get_status_summary()
            return jsonify(status)
    
    def start(self):
        
        def run_server():
            self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        print(f"[WebDashboard] Server đang chạy tại http://{self.host}:{self.port}")
