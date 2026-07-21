import pytest
from core.scanner import scan_port


@pytest.mark.asyncio
async def test_scan_port_closed():
    # Scanning an unassigned high port on localhost to ensure it returns closed/handled gracefully
    result = await scan_port("127.0.0.1", 59999)
    
    assert result["port"] == 59999
    assert result["state"] == "closed"
    assert result["banner"] is None
    assert result["vulnerabilities"] == []