#!/usr/bin/env python3
import os, json, time, collections, requests
from dateutil import parser as dateparser

# config từ env (được load bởi systemd)
WEBHOOK = os.environ.get("WEBHOOK")
FAIL_WINDOW = int(os.environ.get("FAIL_WINDOW", "300"))
FAIL_THRESHOLD = int(os.environ.get("FAIL_THRESHOLD", "5"))
SUPPRESS_WINDOW = int(os.environ.get("SUPPRESS_WINDOW", "600"))
LOGFILE = "/home/cowrie/cowrie/var/log/cowrie/cowrie.json"

buckets = collections.defaultdict(list)  # ip -> [timestamps]
suppressed = {}  # ip -> until_timestamp

def send_slack(text):
    if not WEBHOOK:
        print("No WEBHOOK set, skip send")
        return
    try:
        r = requests.post(WEBHOOK, json={"text": text}, timeout=5)
        if r.status_code >= 400:
            print("Slack returned", r.status_code, r.text)
    except Exception as e:
        print("Slack error:", e)

def prune_old(lst, now):
    return [t for t in lst if t >= now - FAIL_WINDOW]

def process_event(ev):
    evt = ev.get("eventid","")
    if evt not in ("cowrie.login.failed","cowrie.login.success"):
        return

    ip = ev.get("src_ip")
    if not ip:
        return

    # parse timestamp robust
    ts = ev.get("timestamp") or ev.get("time") or time.time()
    try:
        tsf = dateparser.parse(ts).timestamp() if isinstance(ts, str) else float(ts)
    except Exception:
        tsf = time.time()

    now = time.time()

    # if suppressed -> ignore
    if now < suppressed.get(ip, 0):
        return

    lst = buckets[ip]
    lst.append(tsf)
    lst = prune_old(lst, now)
    buckets[ip] = lst

    if len(lst) >= FAIL_THRESHOLD:
        user = ev.get("username","")
        pw = ev.get("password","")
        evt_type = evt
        msg = f"[ALERT] {evt_type} from {ip} attempts={len(lst)} latest_user={user} latest_pass={pw} time={time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))}"
        print(msg)
        send_slack(msg)
        suppressed[ip] = now + SUPPRESS_WINDOW
        buckets[ip] = []  # reset to avoid repeated alerts

def follow(fileobj):
    fileobj.seek(0, 2)
    while True:
        line = fileobj.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

def main():
    if not os.path.exists(LOGFILE):
        print("Log file not found:", LOGFILE)
        return

    with open(LOGFILE, "r", encoding="utf-8", errors="ignore") as f:
        for line in follow(f):
            ev = None # Khởi tạo ev là None
            try:
                # Cố gắng parse JSON
                parsed_json = json.loads(line)
                # Chỉ gán nếu kết quả là dictionary
                if isinstance(parsed_json, dict):
                    ev = parsed_json
                else:
                    # Ghi log nếu parse ra không phải dictionary (tùy chọn)
                    print(f"Warning: Parsed line is not a dictionary: {line.strip()}")
            except json.JSONDecodeError as e:
                # Ghi log nếu parse JSON thất bại (tùy chọn)
                print(f"Warning: Failed to parse JSON line: {e} - Line: {line.strip()}")
                continue # Bỏ qua dòng lỗi

            # Chỉ gọi process_event nếu ev là dictionary hợp lệ
            if ev:
                process_event(ev)

if __name__ == "__main__":
    main()