import os
import subprocess
import requests
import json
from datetime import datetime

# Đọc cấu hình từ config.json
with open('config.json', 'r') as f:
    config = json.load(f)

BLOCK_ENABLED = config["DEFENSE"]["BLOCK_ENABLED"]
SLACK_WEBHOOK = config["ALERTS"]["SLACK_WEBHOOK"]
IDS_LOG_FILE = config["SYSTEM"]["IDS_LOG_FILE"]

def write_log(message):
    print(message)
    try:
        with open(IDS_LOG_FILE, "a") as f:
            timestamp = datetime.now().strftime("%b %d %H:%M:%S")
            f.write(f"{timestamp} honeypot-vm SIEM_IDS: {message}\n")
    except Exception as e:
        print(f"Lỗi ghi file log: {e}")

def block_ip_ufw(ip_address):
    if not BLOCK_ENABLED: return
    try:
        # Kiểm tra xem IP đã bị chặn chưa
        check = subprocess.run(['sudo', 'ufw', 'status'], capture_output=True, text=True)
        if ip_address in check.stdout:
            return

        print(f"\n[!!!] KÍCH HOẠT PHÒNG THỦ: Đang chặn IP {ip_address}...")
        os.system(f"sudo ufw insert 1 deny from {ip_address} to any")
        write_log(f"[ACTIVE_DEFENSE] BLOCKED_ATTACKER_IP | Target: {ip_address}")

        # Gửi cảnh báo Slack
        slack_msg = {
            "text": f"🚨 *HỆ THỐNG PHÒNG THỦ KÍCH HOẠT!* 🚨\n• *IP Kẻ tấn công:* `{ip_address}`\n• *Hành động:* Đã chặn IP (UFW)."
        }
        
        # Chỉ gửi nếu user đã thay thế link Webhook thật
        if "YOUR_WORKSPACE" not in SLACK_WEBHOOK:
            requests.post(SLACK_WEBHOOK, data=json.dumps(slack_msg), headers={'Content-Type': 'application/json'}, timeout=5)
            print("[SUCCESS] Đã gửi thông báo Slack!")
            
    except Exception as e:
        print(f"Lỗi khi chặn IP: {e}")