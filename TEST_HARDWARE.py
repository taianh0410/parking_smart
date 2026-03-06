# TEST_HARDWARE.py
# Script test từng linh kiện riêng lẻ trước khi chạy hệ thống chính

from gpiozero import Servo, Button, DistanceSensor, LED, InputDevice
from time import sleep
import config

def test_servo():
    """Test servo mở/đóng cổng"""
    print("\n" + "="*50)
    print("TEST 1: SERVO (GPIO 6)")
    print("="*50)
    
    try:
        servo = Servo(config.SERVO_PIN)
        
        print("Đóng cổng (0°)...")
        servo.min()
        sleep(2)
        
        print("Mở cổng (90°)...")
        servo.max()
        sleep(2)
        
        print("Đóng lại...")
        servo.min()
        sleep(1)
        
        servo.close()
        print("✅ Servo hoạt động tốt!")
        return True
    except Exception as e:
        print(f"❌ Lỗi servo: {e}")
        return False

def test_button():
    """Test nút bấm"""
    print("\n" + "="*50)
    print("TEST 2: NÚT BẤM (GPIO 21)")
    print("="*50)
    print("Bấm nút trong 5 giây...")
    
    try:
        button = Button(config.BUTTON_PIN, bounce_time=0.3)
        count = 0
        
        def on_press():
            nonlocal count
            count += 1
            print(f"  → Nút được bấm lần {count}")
        
        button.when_pressed = on_press
        
        sleep(5)
        button.close()
        
        if count > 0:
            print(f"✅ Nút bấm hoạt động tốt! (Đã bấm {count} lần)")
            return True
        else:
            print("⚠️ Không phát hiện nút bấm. Kiểm tra kết nối!")
            return False
    except Exception as e:
        print(f"❌ Lỗi nút bấm: {e}")
        return False

def test_ultrasonic():
    """Test cảm biến siêu âm"""
    print("\n" + "="*50)
    print("TEST 3: CẢM BIẾN SIÊU ÂM (GPIO 15, 4)")
    print("="*50)
    print("Đo khoảng cách trong 5 giây...")
    print("(Đưa tay vào trước cảm biến để test)")
    
    try:
        sensor = DistanceSensor(
            echo=config.ULTRASONIC_ECHO,
            trigger=config.ULTRASONIC_TRIGGER,
            max_distance=4
        )
        
        for i in range(10):
            distance_m = sensor.distance
            distance_cm = distance_m * 100
            
            if distance_cm < config.DISTANCE_THRESHOLD:
                print(f"  → Khoảng cách: {distance_cm:.1f} cm ⚠️ PHÁT HIỆN VẬT THỂ!")
            else:
                print(f"  → Khoảng cách: {distance_cm:.1f} cm")
            
            sleep(0.5)
        
        sensor.close()
        print("✅ Cảm biến siêu âm hoạt động tốt!")
        return True
    except Exception as e:
        print(f"❌ Lỗi cảm biến siêu âm: {e}")
        print("   Kiểm tra:")
        print("   - Kết nối TRIGGER (GPIO 15) và ECHO (GPIO 4)")
        print("   - Điện trở phân áp cho chân ECHO (5V → 3.3V)")
        return False

def test_ir_sensor():
    """Test cảm biến hồng ngoại"""
    print("\n" + "="*50)
    print("TEST 4: CẢM BIẾN HỒNG NGOẠI IR (GPIO 22)")
    print("="*50)
    print("Đọc trạng thái trong 5 giây...")
    print("(Đưa tay che cảm biến để test)")
    
    try:
        ir_sensor = InputDevice(config.IR_SENSOR_PIN, pull_up=True)
        
        for i in range(10):
            value = ir_sensor.value
            
            if value == 0:
                print(f"  → Trạng thái: {value} ⚠️ PHÁT HIỆN VẬT CẢN!")
            else:
                print(f"  → Trạng thái: {value} (Không có vật cản)")
            
            sleep(0.5)
        
        ir_sensor.close()
        print("✅ Cảm biến IR hoạt động tốt!")
        return True
    except Exception as e:
        print(f"❌ Lỗi cảm biến IR: {e}")
        return False

def test_led():
    """Test đèn LED"""
    print("\n" + "="*50)
    print("TEST 5: ĐÈN LED (GPIO 13)")
    print("="*50)
    
    try:
        led = LED(config.LED_PIN)
        
        print("Bật LED...")
        led.on()
        sleep(2)
        
        print("Tắt LED...")
        led.off()
        sleep(1)
        
        print("Nhấp nháy 3 lần...")
        for i in range(3):
            led.on()
            sleep(0.3)
            led.off()
            sleep(0.3)
        
        led.close()
        print("✅ LED hoạt động tốt!")
        return True
    except Exception as e:
        print(f"❌ Lỗi LED: {e}")
        return False

def main():
    """Chạy tất cả test"""
    print("\n" + "="*60)
    print("   KIỂM TRA PHẦN CỨNG - BÃI ĐỖ XE THÔNG MINH")
    print("="*60)
    print("Script này sẽ test từng linh kiện riêng lẻ")
    print("Đảm bảo đã kết nối đúng theo sơ đồ GPIO!")
    print()
    input("Nhấn Enter để bắt đầu...")
    
    results = []
    
    # Test từng linh kiện
    results.append(("Servo", test_servo()))
    results.append(("Nút bấm", test_button()))
    results.append(("Cảm biến siêu âm", test_ultrasonic()))
    results.append(("Cảm biến IR", test_ir_sensor()))
    results.append(("LED", test_led()))
    
    # Tổng kết
    print("\n" + "="*60)
    print("   KẾT QUẢ KIỂM TRA")
    print("="*60)
    
    for name, result in results:
        status = "✅ OK" if result else "❌ LỖI"
        print(f"{name:20s} : {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("="*60)
    print(f"Tổng kết: {passed}/{total} linh kiện hoạt động tốt")
    
    if passed == total:
        print("\n🎉 Tất cả linh kiện OK! Sẵn sàng chạy hệ thống chính.")
        print("   Chạy lệnh: python3 main.py")
    else:
        print("\n⚠️ Một số linh kiện chưa hoạt động. Kiểm tra lại kết nối!")
    
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[Test] Đã dừng test")
    except Exception as e:
        print(f"\n\n[Test] Lỗi: {e}")
