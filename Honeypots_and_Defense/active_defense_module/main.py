#!/usr/bin/env python3
import os
import time
import shutil
import hashlib
import subprocess
import random
import json
from typing import Optional, Dict, Set

# [QUAN TRỌNG] Nhập module responder do ta tự viết
from responder import block_ip_ufw, write_log

# Đọc cấu hình từ file config.json
with open('config.json', 'r') as f:
    config = json.load(f)

# Gán biến từ config
BAIT_DIR = config["SYSTEM"]["BAIT_DIR"]
BACKUP_DIR = config["SYSTEM"]["BACKUP_DIR"]
EVIDENCE_DIR = config["SYSTEM"]["EVIDENCE_DIR"]
LOG_FILE = config["SYSTEM"]["LOG_FILE"]
IDS_LOG_FILE = config["SYSTEM"]["IDS_LOG_FILE"]

FORGIVE_TIMEOUT = config["DEFENSE"]["FORGIVE_TIMEOUT"]
RESTORE_DELAY_MIN = config["DEFENSE"]["RESTORE_DELAY_MIN"]
RESTORE_DELAY_MAX = config["DEFENSE"]["RESTORE_DELAY_MAX"]
RANSOMWARE_THRESHOLD = config["DEFENSE"]["RANSOMWARE_THRESHOLD"]

# --- CÁC HÀM TIỆN ÍCH (HELPER) ---
def normalize_name(p: str) -> str:
    return os.path.basename(p.strip().strip('"').strip("'"))

def is_ignored(filename: str) -> bool:
    IGNORE_EXTENSIONS = ('.tmp', '.swp', '.ini', '.db', '.part', '.crdownload')
    IGNORE_FILES = ('desktop.ini', 'Thumbs.db')
    f = filename.lower()
    if f in {x.lower() for x in IGNORE_FILES}: return True
    return f.endswith(tuple(x.lower() for x in IGNORE_EXTENSIONS))

def md5_file_safe(path: str, chunk_size: int = 1024 * 1024) -> Optional[str]:
    h = hashlib.md5()
    try:
        with open(path, "rb") as f:
            while True:
                b = f.read(chunk_size)
                if not b: break
                h.update(b)
        return h.hexdigest()
    except Exception:
        return None

def wait_file_stable(path: str, checks: int = 3, interval: float = 0.5) -> bool:
    try:
        if not os.path.exists(path): return False
        prev = os.path.getsize(path)
        for _ in range(checks):
            time.sleep(interval)
            if not os.path.exists(path): return False
            cur = os.path.getsize(path)
            if cur != prev:
                prev = cur
                continue
        return True
    except Exception:
        return False

def parse_audit_line(line: str) -> Optional[dict]:
    if "smbd_audit|" not in line: return None
    try:
        content = line.split("smbd_audit|", 1)[1].strip()
        parts = content.split('|')
        if len(parts) < 5: return None
        user, ip, machine, share, action = parts[0:5]
        
        status = "unknown"
        args = []
        if len(parts) > 5:
            potential_status = parts[5]
            if potential_status in ('ok', 'fail', 'denied') or potential_status.startswith('NT_STATUS'):
                status = potential_status
                args = parts[6:]
            else:
                args = parts[5:]

        return {
            "identity": f"{user}|{ip}|{machine}",
            "ip": ip,
            "action": action,
            "status": status,
            "args": args
        }
    except Exception:
        return None

# --- LOGIC CỐT LÕI (CORE LOGIC) ---
attacker_memory: Dict[str, float] = {}
deleted_baits: Set[str] = set()
renamed_baits: Set[str] = set()
collected_cache: Set[str] = set()

def mark_destructive(identity: str):
    attacker_memory[identity] = time.time()

def should_restore_for(identity: str) -> bool:
    now = time.time()
    if identity not in attacker_memory: return True
    if (now - attacker_memory[identity]) < FORGIVE_TIMEOUT:
        return False
    del attacker_memory[identity]
    return True

def smart_restore(identity: str):
    if not deleted_baits: return
    if not should_restore_for(identity): return

    time.sleep(random.uniform(RESTORE_DELAY_MIN, RESTORE_DELAY_MAX))
    
    for filename in list(deleted_baits):
        if filename in renamed_baits: continue
        src = os.path.join(BACKUP_DIR, filename)
        dst = os.path.join(BAIT_DIR, filename)

        if not os.path.exists(src): continue
        if not os.path.exists(dst):
            try:
                shutil.copy2(src, dst)
                os.chmod(dst, 0o777)
                deleted_baits.discard(filename)
                write_log(f"[INFO] SYSTEM_SELF_HEALING_ACTIVATED | File: {filename} | Action: Restored_from_Backup")
            except Exception as e:
                print(f"Lỗi restore: {e}")
        else:
            deleted_baits.discard(filename)

def collect_evidence_for_path(filename: str, reason: str):
    if not filename or is_ignored(filename): return
    full_path = os.path.join(BAIT_DIR, filename)
    if not wait_file_stable(full_path): return
    md5 = md5_file_safe(full_path)
    if not md5: return

    key = f"{md5}|{filename}"
    if key in collected_cache: return

    dst = os.path.join(EVIDENCE_DIR, f"{md5}_{filename}")
    if not os.path.exists(dst):
        try:
            shutil.copy2(full_path, dst)
            collected_cache.add(key)
            print(f"[FORENSICS] Capture success: {filename}")
        except Exception: pass

# --- VÒNG LẶP CHÍNH ---
def monitor_logs():
    if not os.path.exists(IDS_LOG_FILE):
        with open(IDS_LOG_FILE, 'w') as f: f.write("")
    os.chmod(IDS_LOG_FILE, 0o666)

    print(f"--- SAMBA GUARD PRO STARTED (Active Defense Mode) ---")

    rename_counter = 0
    last_rename_time = time.time()

    proc = subprocess.Popen(['tail', '-F', '-n', '0', LOG_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        while True:
            line_bytes = proc.stdout.readline()
            if not line_bytes:
                time.sleep(0.1)
                continue
            try:
                line = line_bytes.decode('utf-8', errors='ignore')
            except: continue

            data = parse_audit_line(line)
            if not data: continue

            identity = data['identity']
            attacker_ip = data['ip']
            action = data['action']
            status = data['status']
            args = data['args']

            if status and status not in ('ok', 'success'): continue

            path = args[0] if args else ""
            filename = normalize_name(path)

            if filename and ("BI_MAT" in filename.upper() or "MAT_KHAU" in filename.upper()):
                write_log(f"[CRITICAL] DATA_EXFILTRATION_DETECTED | Src: {identity} | Target: {filename}")

            if action in ('unlink', 'unlinkat'):
                write_log(f"[HIGH] UNAUTHORIZED_FILE_DELETION | Src: {identity} | Target: {filename}")
                mark_destructive(identity)
                if filename: deleted_baits.add(filename)

            elif action in ('rename', 'renameat'):
                if len(args) >= 2:
                    old_name = normalize_name(args[0])
                    new_name = normalize_name(args[1])
                    write_log(f"[WARNING] RANSOMWARE_BEHAVIOR | Src: {identity} | Rename: {old_name} -> {new_name}")

                    mark_destructive(identity)
                    deleted_baits.add(old_name)
                    renamed_baits.add(old_name)
                    collect_evidence_for_path(new_name, reason="ransomware_rename")

                    current_time = time.time()
                    if current_time - last_rename_time < 2.0:
                        rename_counter += 1
                    else:
                        rename_counter = 1

                    last_rename_time = current_time

                    if rename_counter >= RANSOMWARE_THRESHOLD:
                        block_ip_ufw(attacker_ip)

            elif action in ('opendir', 'connect', 'chdir'):
                smart_restore(identity)

            elif action in ('close', 'pwrite', 'write'):
                if action == 'close':
                    collect_evidence_for_path(filename, reason="upload_close")
                    write_log(f"[INFO] MALWARE_SAMPLE_CAPTURED | Src: {identity} | File: {filename} | Action: Uploaded")

    except KeyboardInterrupt:
        write_log("\n[STOP] Samba Guard Service Stopped.")
        proc.terminate()

if __name__ == "__main__":
    monitor_logs()