import asyncio
import json
import psutil
import websockets

async def send_simulated_alert():
    # 1. Dynamically target an active process (cmd.exe or python.exe)
    target_pid = None
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'cmd.exe':
            target_pid = proc.info['pid']
            break
            
    if not target_pid:
        target_pid = 12345

    print(f"[*] Dynamically targeted active host PID: {target_pid}")
    
    # 2. Construct simulated threat payload
    payload = {
        "event_type": "PROCESS_SPAWNED",
        "data": {
            "process_name": "powershell.exe",
            "parent_name": "cmd.exe",
            "ppid": target_pid,
            "pid": 99999,
            "severity": "CRITICAL",
            "title": "Encoded PowerShell Execution [CR-014]"
        }
    }

    # 3. Connect to WebSocket server and send payload
    uri = "ws://127.0.0.1:8000/ws"
    print(f"[*] Sending simulated threat vector telemetry to CyberRecon...")
    
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(payload))
            print("[+] Payload successfully delivered to server!")
    except Exception as e:
        print(f"[-] Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(send_simulated_alert())