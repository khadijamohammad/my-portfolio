import os
import signal
import json
import logging
import sys
from pathlib import Path

# Tell Python to look inside the 'core' folder for imports
sys.path.append(str(Path(__file__).resolve().parent / "core"))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

# Mount the root directory so files like Wolfs.png can be served via /static/Wolfs.png
app.mount("/static", StaticFiles(directory="."), name="static")

from pathlib import Path

# ==========================================
# 🌐 0. HOME ROUTE (SERVES DASHBOARD UI)
# ==========================================
BASE_DIR = Path(__file__).resolve().parent

@app.get("/")
async def get_dashboard():
    # Looks for index.html in dashboard/ or directly in CyberRecon_V5/
    dashboard_path = BASE_DIR / "dashboard" / "index.html"
    root_path = BASE_DIR / "index.html"
    
    target_file = dashboard_path if dashboard_path.exists() else root_path

    if not target_file.exists():
        return HTMLResponse(
            content=f"<h3>Error: Could not find index.html at {target_file}</h3>", 
            status_code=404
        )

    with open(target_file, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())



# ==========================================
# 🛡️ 1. ENTERPRISE TELEMETRY NOISE FILTER
# ==========================================
NOISE_IGNORE_LIST = {
    "chrome.exe", "msedge.exe", "msedgewebview2.exe", "brave.exe", "firefox.exe",
    "dllhost.exe", "audiodg.exe", "searchfilterhost.exe", "searchprotocolhost.exe",
    "backgroundtaskhost.exe", "taskhostw.exe", "runtimebroker.exe", "siihost.exe"
}

def should_process_telemetry(event_data: dict) -> bool:
    """Returns False if process is known ambient noise, True if telemetry should be processed."""
    if not event_data or "process_name" not in event_data:
        return False
    process_name = event_data["process_name"].lower()
    if process_name in NOISE_IGNORE_LIST:
        return False
    return True


# ==========================================
# 🔌 2. WEBSOCKET CONNECTION MANAGER
# ==========================================
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


# ==========================================
# ⚡ 3. SOAR MITIGATION UTILITY
# ==========================================
def neutralize_threat(pid: int, process_name: str):
    """Active SOAR mitigation: Terminates a critical threat vector process."""
    try:
        print(f"[!] SOAR ACTION: Critical anomaly detected in {process_name} (PID: {pid})")
        os.kill(pid, signal.SIGTERM)
        print(f"[+] SOAR STATUS: Process {pid} neutralized successfully.")
    except Exception as e:
        print(f"[-] SOAR STATUS: Containment failed or process already dead: {e}")


# ==========================================
# 🎯 4. MAIN WEBSOCKET ROUTE
# ==========================================
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            event = json.loads(data)
            
            if event.get("event_type") == "PROCESS_SPAWNED":
                payload = event.get("data", {})
                
                # 🛡️ Step A: Run Noise Filter
                if not should_process_telemetry(payload):
                    continue  # Ignore background noise binaries
                
                # 🎯 Step B: Check for SOAR Trigger
                if payload.get("process_name") == "powershell.exe":
                    target_pid = payload.get("ppid")
                    neutralize_threat(target_pid, payload.get("parent_name", "Unknown Parent"))
            
            # 📊 Step C: Broadcast clean telemetry to UI
            await manager.broadcast(data)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)