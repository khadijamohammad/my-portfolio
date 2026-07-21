# 🛡️ NetSentinel

> **Asynchronous Network Vulnerability Scanner & Service Reconnaissance Engine**

NetSentinel is a high-performance, asynchronous network security scanner built with Python. It performs non-blocking TCP port scanning, active protocol banner grabbing, CVE vulnerability correlation, and generates structured report outputs in both HTML and JSON.

---

## 📐 Architecture Overview

```text
               +----------------------------------+
               |        NetSentinel CLI           |
               +----------------------------------+
                                |
                                v
               +----------------------------------+
               |   Async Scan Orchestrator        |
               +----------------------------------+
                                |
            +-------------------+-------------------+
            |                                       |
            v                                       v
+-----------------------+               +-----------------------+
|  Async TCP Port       |               | Banner Grabber &      |
|  Scanner              |               | Service Detection     |
+-----------------------+               +-----------------------+
            |                                       |
            +-------------------+-------------------+
                                |
                                v
               +----------------------------------+
               |   CVE & Misconfig Correlation    |
               +----------------------------------+
                                |
            +-------------------+-------------------+
            |                                       |
            v                                       v
+-----------------------+               +-----------------------+
|  JSON Data Exporter   |               |  HTML Dashboard      |
|                       |               |  Generator            |
+-----------------------+               +-----------------------+