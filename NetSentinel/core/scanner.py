import asyncio
from typing import Dict, List, Any, Optional
from core.banner_grabber import grab_banner
from core.cve_engine import check_vulnerabilities


async def scan_port(ip: str, port: int) -> Dict[str, Any]:
    """
    Scans a single TCP port, grabs service banner, and checks for vulnerabilities.
    """
    result: Dict[str, Any] = {
        "port": port,
        "state": "closed",
        "banner": None,
        "vulnerabilities": []
    }

    try:
        conn = asyncio.open_connection(ip, port)
        reader, writer = await asyncio.wait_for(conn, timeout=1.5)
        result["state"] = "open"
        writer.close()
        await writer.wait_closed()

        # Active banner grabbing
        banner: Optional[str] = await grab_banner(ip, port)
        result["banner"] = banner
        result["vulnerabilities"] = check_vulnerabilities(banner or "", port)

    except (asyncio.TimeoutError, OSError):
        pass

    return result


async def run_scan(target: str, ports: List[int]) -> List[Dict[str, Any]]:
    """
    Runs concurrent port scans against the target IP address.
    """
    tasks = [scan_port(target, port) for port in ports]
    results = await asyncio.gather(*tasks)
    return [r for r in results if r["state"] == "open"]