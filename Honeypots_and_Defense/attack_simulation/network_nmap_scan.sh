#!/bin/bash
echo "=================================================="
echo "🔥 RECONNAISSANCE SIMULATOR (Nmap Stealth Scan) 🔥"
echo "=================================================="

# Thay IP bằng IP máy ảo Honeypot
TARGET_IP="192.168.x.x"

echo "[*] Đang tiến hành quét cổng toàn diện trên mục tiêu $TARGET_IP..."
echo "[!] Hành vi này sẽ tạo ra hàng loạt log kết nối (Connect) trong hệ thống."
sleep 2

# Quét phát hiện hệ điều hành, version dịch vụ và chạy script mặc định
nmap -A -T4 -p- $TARGET_IP

echo -e "\n[V] Hoàn tất quá trình dò thám. Các dịch vụ đang mở đã bị lộ diện!"