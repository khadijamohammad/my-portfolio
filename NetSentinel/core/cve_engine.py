from typing import List, Dict, Any
import asyncio

async def check_smbv1_enabled(ip: str, port: int = 445, timeout: float = 3.0) -> bool:
    """Sends a raw SMBv1 Negotiate packet to verify if SMBv1 is active."""
    netbios_header = b"\x00\x00\x00\x45"
    smb1_header = (
        b"\xffSMB\x72\x00\x00\x00\x00\x18\x01\xc8"
        b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x00\x00\x00\x00\x00\x00\x00\x00"
    )
    smb1_payload = b"\x00\x0c\x00\x02NT LM 0.12\x00"
    request_packet = netbios_header + smb1_header + smb1_payload

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port), timeout=timeout
        )
        writer.write(request_packet)
        await writer.drain()

        response = await asyncio.wait_for(reader.read(1024), timeout=timeout)
        writer.close()
        await writer.wait_closed()

        if len(response) >= 8 and response[4:8] == b"\xffSMB":
            return True
    except (asyncio.TimeoutError, ConnectionResetError, OSError):
        pass

    return False


# Local CVE and misconfiguration signature database
VULN_DATABASE = {
    135: {
        "cve_id": "MISCONFIG-135",
        "title": "Exposed Microsoft RPC Endpoint Mapper",
        "severity": "MEDIUM",
        "description": "MSRPC (Port 135) is visible to network probes. Allows remote attackers to enumerate DCOM interface bindings.",
        "remediation": "Restrict Port 135 via Windows Firewall to trusted administrative IP subnets."
    },
    21: {
        "cve_id": "MISCONFIG-021",
        "title": "Unencrypted Cleartext FTP Service",
        "severity": "HIGH",
        "description": "FTP transmits credentials in cleartext over the wire.",
        "remediation": "Migrate to SFTP (Port 22) or enforce FTPS (Explicit TLS)."
    },
    23: {
        "cve_id": "MISCONFIG-023",
        "title": "Legacy Telnet Protocol Active",
        "severity": "HIGH",
        "description": "Telnet communicates in unencrypted plain text, enabling credential sniffing.",
        "remediation": "Disable Telnet service and utilize SSH for remote administration."
    },
    3389: {
        "cve_id": "CVE-2019-0708",
        "title": "Exposed RDP / BlueKeep Vulnerability Indicator",
        "severity": "HIGH",
        "description": "Exposed Remote Desktop Protocol (RDP) service reachable across network boundary.",
        "remediation": "Enable Network Level Authentication (NLA) and restrict RDP access behind VPN."
    }
}


async def analyze_vulnerabilities(open_port_results: List[Dict[str, Any]], target_ip: str = "127.0.0.1") -> List[Dict[str, Any]]:
    """
    Evaluates open ports, active probes, and banners against known CVE signatures.
    """
    findings = []
    
    for item in open_port_results:
        port = item.get("port")
        banner = item.get("banner", "")
        
        # --- Active Probe for Port 445 (SMB) ---
        if port == 445:
            smbv1_active = await check_smbv1_enabled(target_ip, port=445)
            
            if smbv1_active:
                findings.append({
                    "cve_id": "CVE-2017-0144",
                    "title": "EternalBlue / SMBv1 Remote Code Execution Risk",
                    "severity": "CRITICAL",
                    "description": "Target actively responds to SMBv1 dialect negotiations.",
                    "remediation": "Disable SMBv1 via DISM / PowerShell and enforce SMB signing.",
                    "matched_port": 445
                })
            else:
                findings.append({
                    "cve_id": "SEC-CONFIG-445",
                    "title": "Exposed SMB Service (SMBv1 Disabled)",
                    "severity": "INFO",
                    "description": "Port 445 is open for SMBv2/v3, but target correctly rejected SMBv1 negotiations.",
                    "remediation": "Ensure SMB signing is required and restrict access via firewall.",
                    "matched_port": 445
                })
        
        # --- Check standard static database for other ports ---
        elif port in VULN_DATABASE:
            vuln = VULN_DATABASE[port].copy()
            vuln["matched_port"] = port
            findings.append(vuln)
        
        # --- Banner-specific rule matching ---
        if "OpenSSH_8.2" in str(banner):
            findings.append({
                "cve_id": "INFO-SSH-8.2",
                "title": "Outdated OpenSSH Version Banner Detected",
                "severity": "LOW",
                "description": f"Target returns banner '{banner}'. Ensure OS security updates are applied.",
                "remediation": "Keep OpenSSH upgraded to the latest distribution package.",
                "matched_port": port
            })
            
    return findings


if __name__ == "__main__":
    async def test_run():
        sample_scan = [
            {"port": 135, "status": "open", "banner": "No banner returned"},
            {"port": 445, "status": "open", "banner": "No banner returned"},
            {"port": 22, "status": "open", "banner": "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5"}
        ]
        
        results = await analyze_vulnerabilities(sample_scan, "127.0.0.1")
        print(f"[+] Found {len(results)} vulnerability correlation matches:\n")
        for r in results:
            print(f"[{r['severity']}] {r['title']} ({r['cve_id']}) on Port {r['matched_port']}")

    asyncio.run(test_run())