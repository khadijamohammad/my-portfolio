import asyncio
import socket
from typing import List, Dict, Any

# Common high-risk ports to scan by default
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 1433, 3306, 3389, 8080]

async def scan_port(host: str, port: int, timeout: float = 1.0) -> Dict[str, Any]:
    """
    Attempts an async TCP connection to a specific host and port.
    Returns status and banner info if open.
    """
    result = {"port": port, "status": "closed", "banner": None}
    try:
        # Create socket connection with timeout
        conn = asyncio.open_connection(host, port)
        reader, writer = await asyncio.wait_for(conn, timeout=timeout)
        
        result["status"] = "open"
        
        # Attempt non-blocking banner grab
        try:
            writer.write(b"\r\n")
            await writer.drain()
            banner_bytes = await asyncio.wait_for(reader.read(1024), timeout=1.0)
            result["banner"] = banner_bytes.decode('utf-8', errors='ignore').strip()
        except Exception:
            result["banner"] = "No banner returned"

        writer.close()
        await writer.wait_closed()

    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        pass  # Port closed or filtered

    return result

async def run_async_scan(target_host: str, ports: List[int] = COMMON_PORTS) -> List[Dict[str, Any]]:
    """
    Scans multiple ports concurrently across a single target host.
    """
    print(f"[*] Starting async scan against {target_host} for {len(ports)} ports...")
    tasks = [scan_port(target_host, port) for port in ports]
    results = await asyncio.gather(*tasks)
    
    # Filter to show only open ports
    open_ports = [r for r in results if r["status"] == "open"]
    return open_ports

if __name__ == "__main__":
    # Self-test scanning local loopback
    target = "127.0.0.1"
    open_results = asyncio.run(run_async_scan(target))
    print(f"\n[+] Scan Complete for {target}. Open Ports:")
    for res in open_results:
        print(f"    - Port {res['port']}: OPEN | Banner: {res['banner']}")