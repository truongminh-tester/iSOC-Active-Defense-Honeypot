import os
import time
import random

def simulate_ransomware(target_dir, num_files=8):
    print("==================================================")
    print("🔥 RANSOMWARE SIMULATOR (Dành cho mục đích Test) 🔥")
    print("==================================================\n")
    print(f"[*] Mục tiêu tấn công: {target_dir}")

    # Bước 1: Tạo các file mồi giả vờ là tài liệu quan trọng
    created_files = []
    print("\n[1] Đang sinh ra các tài liệu giả mạo...")
    for i in range(num_files):
        filename = f"Du_lieu_mat_ke_toan_T{i+1}.docx"
        filepath = os.path.join(target_dir, filename)
        try:
            with open(filepath, 'w') as f:
                f.write("Day la du lieu bao mat cap cao..." * 10)
            created_files.append(filepath)
            print(f"  + Đã tạo: {filename}")
        except Exception as e:
            print(f"  - Bỏ qua do lỗi quyền: {e}")

    if not created_files:
        print("[-] Không thể tạo file. Hãy kiểm tra lại quyền ghi trên thư mục Share.")
        return

    print("\n[*] Chờ 2 giây trước khi tiến hành mã hóa...")
    time.sleep(2)

    # Bước 2: Giả lập hành vi đổi tên file cực nhanh của Ransomware
    print("\n[2] BẮT ĐẦU TẤN CÔNG (ĐỔI TÊN HÀNG LOẠT)...")
    for filepath in created_files:
        encrypted_path = filepath + ".locked_by_hacker"
        try:
            os.rename(filepath, encrypted_path)
            print(f"  [!] Đã mã hóa -> {os.path.basename(encrypted_path)}")
            # Ransomware thường đổi tên file liên tục trong chưa tới 1 giây
            time.sleep(0.1) 
        except Exception as e:
            print(f"  - Không thể mã hóa: {e}")

    print("\n[V] Hoàn tất kịch bản giả lập!")
    print("[👉] Việc cần làm: Mở log của hệ thống iSOC xem IP của bạn đã bị block chưa nhé!")

if __name__ == "__main__":
    target_share = input("Nhập đường dẫn thư mục Share đang mount (VD: Z:\\tailieu hoặc /mnt/share): ")
    if os.path.exists(target_share):
        simulate_ransomware(target_share)
    else:
        print("Đường dẫn không tồn tại! Hãy chắc chắn bạn đã map ổ đĩa mạng.")