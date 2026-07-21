import asyncio
from typing import Dict, Any

async def probe_http_banner(ip: str, port: int, timeout: float = 2.0) -> str:
    """Sends a raw HTTP HEAD request to extract Server header details."""
    request = f"HEAD / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: NetSentinel/1.0\r\nConnection: close\r\n\r\n"
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port), timeout=timeout
        )
        writer.write(request.encode())
        await writer.drain()

        response = await asyncio.wait_for(reader.read(1024), timeout=timeout)
        writer.close()
        await writer.wait_closed()

        response_text = response.decode('utf-8', errors='ignore')
        
        # Extract Server header if present
        for line in response_text.splitlines():
            if line.lower().startswith("server:"):
                return line.split(":", 1)[1].strip()
            
        # Return first line status if Server header isn't present
        first_line = response_text.splitlines()[0] if response_text.splitlines() else ""
        return first_line if first_line else "HTTP Service (No Server Header)"
    except Exception:
        return "HTTP Service (No response to HEAD request)"


async def probe_generic_banner(ip: str, port: int, timeout: float = 2.0) -> str:
    """Connects and listens for initial welcome banner (FTP, SSH, SMTP)."""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port), timeout=timeout
        )
        banner_bytes = await asyncio.wait_for(reader.read(512), timeout=timeout)
        writer.close()
        await writer.wait_closed()

        banner_str = banner_bytes.decode('utf-8', errors='ignore').strip()
        return banner_str if banner_str else "Standard Service"
    except Exception:
        return "Standard Service"


async def enrich_service_banner(target_ip: str, port: int, initial_banner: str = "") -> Dict[str, Any]:
    """
    Actively probes open ports to identify service details and banners.
    """
    banner_details = initial_banner.strip() if initial_banner else ""
    
    # Map common ports to names
    PORT_MAP = {
        21: "FTP", 22: "SSH", 23: "TELNET", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 135: "MSRPC", 139: "NETBIOS-SSN",
        143: "IMAP", 443: "HTTPS", 445: "MICROSOFT-DS", 3306: "MYSQL",
        3389: "RDP", 8080: "HTTP-ALT"
    }
    
    service_name = PORT_MAP.get(port, f"UNKNOWN-{port}")

    # Active probing if initial scan didn't grab a detailed banner
    if not banner_details or banner_details == "No banner returned":
        if port in [80, 443, 8080]:
            banner_details = await probe_http_banner(target_ip, port)
        elif port in [21, 22, 25, 110, 143]:
            banner_details = await probe_generic_banner(target_ip, port)
        else:
            banner_details = "Standard Service"

    return {
        "port": port,
        "service": service_name,
        "banner_details": banner_details
    }


def identify_service(port: int, banner: str = "") -> Dict[str, Any]:
    """Fallback synchronous wrapper for backwards compatibility."""
    return {
        "port": port,
        "service": "Service",
        "banner_details": banner if banner else "Standard Service"
    }