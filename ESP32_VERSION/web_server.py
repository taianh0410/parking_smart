# web_server.py - ESP32 Version
# Web Server đơn giản cho ESP32 (không dùng Flask)

import socket
import json

class WebServer:
    """
    Web Server đơn giản cho ESP32
    Không dùng Flask, chỉ dùng socket thuần
    """
    
    def __init__(self, parking_manager, port=80):
        self.parking_manager = parking_manager
        self.port = port
        self.socket = None
        
        print(f"[WebServer] Khởi tạo tại port {port}")
    
    def start(self):
        """Khởi động web server"""
        try:
            # Tạo socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('', self.port))
            self.socket.listen(5)
            self.socket.setblocking(False)  # Non-blocking mode
            
            print(f"[WebServer] Server đang chạy tại port {self.port}")
        except Exception as e:
            print(f"[WebServer] Lỗi khởi động: {e}")
    
    def handle_request(self):
        """
        Xử lý request (gọi trong vòng lặp chính)
        Non-blocking để không làm treo hệ thống
        """
        try:
            conn, addr = self.socket.accept()
            conn.settimeout(1.0)
            
            # Đọc request
            request = conn.recv(1024).decode('utf-8')
            
            # Parse request line
            if request:
                request_line = request.split('\r\n')[0]
                method, path, _ = request_line.split(' ')
                
                # Xử lý routing
                if path == '/':
                    response = self._serve_html()
                elif path == '/api/status':
                    response = self._serve_api()
                else:
                    response = self._serve_404()
                
                # Gửi response
                conn.send(response.encode('utf-8'))
            
            conn.close()
        except OSError:
            # Không có connection mới (non-blocking)
            pass
        except Exception as e:
            print(f"[WebServer] Lỗi xử lý request: {e}")
    
    def _serve_html(self):
        """Trả về trang HTML"""
        html = """HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8

<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bãi Đỗ Xe Thông Minh - ESP32</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 24px;
        }
        .status-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
        }
        .status-number {
            font-size: 72px;
            font-weight: bold;
            margin: 20px 0;
        }
        .status-label {
            font-size: 18px;
            opacity: 0.9;
        }
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 20px;
        }
        .info-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .info-box .label {
            color: #666;
            font-size: 14px;
            margin-bottom: 8px;
        }
        .info-box .value {
            color: #333;
            font-size: 24px;
            font-weight: bold;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚗 Bãi Đỗ Xe Thông Minh</h1>
        
        <div class="status-card">
            <div class="status-label">Số chỗ trống hiện tại</div>
            <div class="status-number" id="available">-</div>
            <div class="status-label" id="status">Đang tải...</div>
        </div>
        
        <div class="info-grid">
            <div class="info-box">
                <div class="label">Tổng số chỗ</div>
                <div class="value" id="total">-</div>
            </div>
            <div class="info-box">
                <div class="label">Đang sử dụng</div>
                <div class="value" id="occupied">-</div>
            </div>
        </div>
        
        <div class="footer">
            Cập nhật mỗi 2 giây | ESP32
        </div>
    </div>
    
    <script>
        function updateStatus() {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('available').textContent = data.available;
                    document.getElementById('total').textContent = data.total_slots;
                    document.getElementById('occupied').textContent = data.occupied;
                    document.getElementById('status').textContent = data.is_full ? 'Bãi đầy' : 'Còn chỗ trống';
                })
                .catch(e => console.error('Lỗi:', e));
        }
        updateStatus();
        setInterval(updateStatus, 2000);
    </script>
</body>
</html>"""
        return html
    
    def _serve_api(self):
        """Trả về API JSON"""
        status = self.parking_manager.get_status_summary()
        json_data = json.dumps(status)
        
        response = f"""HTTP/1.1 200 OK
Content-Type: application/json

{json_data}"""
        return response
    
    def _serve_404(self):
        """Trả về 404"""
        return """HTTP/1.1 404 Not Found
Content-Type: text/plain

404 Not Found"""
    
    def cleanup(self):
        """Dọn dẹp tài nguyên"""
        if self.socket:
            self.socket.close()
        print("[WebServer] Đã dọn dẹp tài nguyên")
