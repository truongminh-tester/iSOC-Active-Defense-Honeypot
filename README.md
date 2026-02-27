🎯 Security Testing Strategy (QA Focus)
Security & Penetration Testing: Automated execution of Red Team scripts (attack_simulation/) to validate the sensitivity and accuracy of honeypot sensors against web and system-level exploits.

Integration Testing: Verifying the integrity of the data pipeline from Filebeat (Node 1) to the Kibana Dashboard (Node 2) ensuring zero log drop rates.

Resilience & SLA Testing: Simulating Ransomware attacks to measure the system's automated self-healing capabilities and restoration delay metrics.

Alerting Flow Validation: Confirming real-time Webhook dispatch to Slack channels with accurate attacker IP extraction within a < 1-second threshold.

⚙️ Setup & Deployment
Provision two separate environments/VMs for Node 1 (Honeypot) and Node 2 (ELK).

Configure systemd services and .yml configurations as per the repository documentation.

Execute main.py to initialize the Active Defense gatekeeper.

Import iSOC_Dashboard.ndjson into the Kibana interface to setup analytics.

Run the provided Python/Bash scripts in attack_simulation to validate system defense capabilities.

Author: NGUYEN PHUC TRUONG MINH - Information Security Major, VNU-IS