import asyncio
from typing import Optional


async def grab_banner(ip: str, port: int, timeout: float = 2.0) -> Optional[str]:
    """
    Attempts an asynchronous TCP connection to grab a service banner.
    Returns the decoded banner string or None if connection fails.
    """
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port), timeout=timeout
        )
        
        # Send a generic probe if needed for protocols like HTTP
        if port in (80, 8080, 443):
            writer.write(b"HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n")
            await writer.drain()

        data: bytes = await asyncio.wait_for(reader.read(1024), timeout=timeout)
        writer.close()
        await writer.wait_closed()
        
        return data.decode("utf-8", errors="ignore").strip()
    except Exception:
        return None