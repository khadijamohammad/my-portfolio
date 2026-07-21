# 🛡️ NetSentinel

[![NetSentinel CI](https://github.com/khadijamohammad/my-portfolio/actions/workflows/test.yml/badge.svg)](https://github.com/khadijamohammad/my-portfolio/actions/workflows/test.yml)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 💡 Why I Built This

Traditional network reconnaissance tools can be slow, resource-heavy, or difficult to integrate into modern automated pipelines. **NetSentinel** was developed as an asynchronous, high-performance network vulnerability assessment scanner designed to accelerate local surface discovery while producing structured, actionable security reports.

I built NetSentinel to explore high-concurrency network scanning techniques and dynamic threat correlation. By leveraging non-blocking execution models, the tool efficiently interrogates network endpoints, correlates open services against vulnerability databases, and highlights potential security gaps without requiring heavy enterprise overhead.

This project showcases expertise in **asynchronous network programming (`asyncio` & sockets)**, **threat intelligence integration (CVE/IOC correlation)**, **automated reporting engines**, and **CI/CD integration using GitHub Actions**.

**NetSentinel** is an asynchronous Python-based network security utility designed for fast service reconnaissance, banner grabbing, vulnerability correlation, and automated security report generation.

---

## 📸 Demo & Preview

### Terminal Execution
![Terminal Scan Output](assets/terminal.png)

### Generated HTML Security Report
![HTML Scan Report](assets/dashboard.png)
## 🎯 Features

* ⚡ **Asynchronous Scanning:** Fast concurrent port scanning powered by Python's `asyncio`.
* 🔍 **Service Banner Detection:** Extracts banner info on open ports to identify running services.
* 🛡️ **CVE Risk Correlation:** Maps identified service banners against known vulnerability data.
* 📊 **HTML Dashboard Generation:** Generates clean, standalone HTML reports saving directly to disk.
* 🪵 **Structured Logging:** Timestamps and level-based console outputs for clear execution tracking.
* 🧪 **Automated CI/CD:** Covered by unit tests and validated on every commit via GitHub Actions.

---

## 🏗️ Architecture & Data Flow

```mermaid
graph TD
    A[CLI Entrypoint: main.py] --> B[Async Scanner: core/scanner.py]
    B -->|Network Connection| C[Target Network / Host]
    B -->|Banner Raw Data| D[CVE Engine: core/cve_engine.py]
    B -->|Scan Logs| E[Structured Logger: utils/logger.py]
    D -->|Vulnerability Matches| F[Report Generator: reports/generator.py]
    F -->|Render HTML| G[reports/scan_report_*.html]