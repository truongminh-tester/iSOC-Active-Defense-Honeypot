# 🛡️ iSOC - Intelligent Security Operations Center & Active Defense

![Build Status](https://img.shields.io/badge/Status-Completed-success)
![Platform](https://img.shields.io/badge/Platform-Ubuntu%20Linux-orange)
![Tech Stack](https://img.shields.io/badge/Stack-ELK%20%7C%20Python%20%7C%20Flask-blue)
![Testing](https://img.shields.io/badge/Testing-Security%20%7C%20Red%20Team-red)

## 📌 Project Overview
**iSOC (Intelligent Security Operations Center)** is a comprehensive cybersecurity defense system featuring high-interaction honeypots, automated threat mitigation, and centralized logging. Designed specifically to mimic financial and banking infrastructures, the system detects, analyzes, and proactively blocks cyber threats in real-time. 

This project bridges **Red Team offensive simulations** with **Blue Team defensive architectures**, demonstrating a strong foundation in Information Security and Quality Assurance (QA).

## 🚀 Key Features
* **Multi-Layered Honeypot Network:** * **Samba File Share:** Decoy storage to capture and analyze Ransomware behavior.
  * **Cowrie SSH:** Traps brute-force attempts and logs unauthorized command executions.
  * **Financial Web Fake (Flask):** Simulated banking login and search portals to capture SQL Injection (SQLi) and Credential Stuffing payloads.
* **Active Defense Mechanism:** A Python-based daemon that continuously parses security logs. Upon detecting anomalous patterns (e.g., mass file renaming, failed SSH logins), it automatically triggers UFW (Uncomplicated Firewall) to drop the attacker's IP and dispatches real-time Slack Webhook alerts.
* **Centralized SIEM (ELK Stack):** Utilizes Filebeat to ship distributed logs to an Elasticsearch cluster, visualized through custom Kibana Dashboards for immediate threat intelligence.

## 📂 Repository Structure
```text
📦 iSOC_Project
 ┣ 📂 1_Node_Honeypots_and_Defense/    # Sensor Node: Decoys, Active Defense Bot & Log Shippers
 ┣ 📂 2_SIEM_ELK_Stack/                # Analytics Node: Elasticsearch, Kibana & Dashboards
 ┣ 📂 attack_simulation/               # QA & Red Team Automation Scripts
 ┃ ┣ 📜 ransomware_sim.py              # Ransomware encryption behavior simulator
 ┃ ┣ 📜 ssh_hydra_bruteforce.sh        # Hydra brute-force test script
 ┃ ┣ 📜 web_sqli_attack.py             # SQL Injection payload generator
 ┃ ┗ 📜 network_nmap_scan.sh           # Nmap stealth scanning script
 ┣ 📜 TEST_CASES.md                    # [QA] Security test cases & defense validation flows
 ┣ 📜 BUG_REPORT.md                    # [QA] Vulnerability reports & system optimizations
 ┗ 📜 README.md                        # Project documentation

```

## 🎯 Security Testing Strategy (QA Focus)

* **Security & Penetration Testing:** Automated execution of Red Team scripts (`attack_simulation/`) to validate the sensitivity and accuracy of honeypot sensors against web and system-level exploits.
* **Integration Testing:** Verifying the integrity of the data pipeline from Filebeat (Node 1) to the Kibana Dashboard (Node 2) ensuring zero log drop rates.
* **Resilience & SLA Testing:** Simulating Ransomware attacks to measure the system's automated self-healing capabilities and restoration delay metrics.
* **Alerting Flow Validation:** Confirming real-time Webhook dispatch to Slack channels with accurate attacker IP extraction within a < 1-second threshold.

## ⚙️ Setup & Deployment

1. Provision two separate environments/VMs for **Node 1 (Honeypot)** and **Node 2 (ELK)**.
2. Configure `systemd` services and `.yml` configurations as per the repository documentation.
3. Execute `main.py` to initialize the Active Defense gatekeeper.
4. Import `iSOC_Dashboard.ndjson` into the Kibana interface to setup analytics.
5. Run the provided Python/Bash scripts in `attack_simulation` to validate system defense capabilities.

---

**Author:** NGUYEN PHUC TRUONG MINH - Information Security Major, VNU-IS

```
