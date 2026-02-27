import requests
import time

print("==================================================")
print("🔥 WEB HONEYPOT ATTACK SIMULATOR (Brute-force)  🔥")
print("==================================================\n")

# Thay bằng URL Web Honeypot của bạn
TARGET_URL = "http://192.168.x.x:5000/login"

# Danh sách mật khẩu phổ biến
passwords = ["123456", "admin123", "password", "qwerty", "letmein", "P@ssw0rd"]

print(f"[*] Mục tiêu: {TARGET_URL}")
print("[*] Đang nã request liên tục vào form đăng nhập...\n")

for pwd in passwords:
    # Giả lập payload gửi lên form đăng nhập
    payload = {
        "username": "admin",
        "password": pwd
    }
    try:
        print(f"  [>] Thử payload: admin / {pwd}")
        response = requests.post(TARGET_URL, data=payload, timeout=3)
        
        # Ngay khi có request chọc vào, Filebeat sẽ gom log gửi về ELK
        time.sleep(0.5) 
    except requests.exceptions.RequestException as e:
        print(f"  [X] Không thể kết nối: {e}")
        break

print("\n[V] Đã hoàn thành đợt nã đạn HTTP POST!")
print("[👉] Mở Kibana Dashboard lên, bạn sẽ thấy biểu đồ Spike (tăng vọt) lượng Failed Login.")