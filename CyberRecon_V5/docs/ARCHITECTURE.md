# CyberRecon Architecture & Data Flow

This document details the telemetry ingestion and visualization pipeline of the CyberRecon EDR system.

## 📊 Telemetry Lifecycle
1. **Collection Engine (`test_alert.py`):** Captures local process execution states and maps the tracking lineages (PID/PPID mapping).
2. **Ingestion Middleware (`server.py`):** Runs an asynchronous FastAPI WebSocket server. It routes incoming telemetry through an enterprise-grade noise filter list to discard transient system binaries (e.g., `dllhost.exe`, `msedgewebview2.exe`).
3. **Visualization Matrix (Frontend UI):** Receives the filtered telemetry packet and dynamically updates an interactive tree topology graph using D3.js.