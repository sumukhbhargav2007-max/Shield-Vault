# 🛡️ ShieldVault: Enterprise AI Threat Intelligence & Log Analyzer

ShieldVault is a high-performance Security Operations Center (SOC) dashboard designed to ingest, parse, and analyze server access logs in real time. Built for rapid incident response, it automatically flags brute-force attacks, unauthorized access vectors, and suspicious HTTP status codes (such as `401` and `403`).

---

## 🚀 Key Features

* **SOC Multi-Page Interface:** Interactive dark-mode dashboard featuring deep blue infrastructure styling, glassmorphic metric cards, and embossed navigation controls.
* **Automated Threat Detection:** Flags repeated failed authentication attempts (`401 Unauthorized`) based on customizable sensitivity thresholds.
* **Attack Distribution Matrix:** Visualizes source IP telemetry and tracks unique attack vectors dynamically.
* **Live Telemetry & Log Explorer:** Real-time stream console with built-in search filters for rapid forensic investigation.
* **Audit & Compliance Reporting:** Instant incident report generation with one-click CSV export capabilities.

---

## 🛠️ Tech Stack
* **Python** (Core logic & regex parsing)
* **Streamlit** (Interactive web application framework)
* **Pandas** (Data aggregation and matrix processing)

---

## ⚙️ Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/ShieldVault.git](https://github.com/your-username/ShieldVault.git)
   cd ShieldVault