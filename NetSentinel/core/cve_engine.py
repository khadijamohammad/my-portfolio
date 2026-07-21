from typing import Dict, List, Any


def check_vulnerabilities(banner: str, port: int) -> List[Dict[str, Any]]:
    """
    Correlates banners and port numbers against known common vulnerabilities/misconfigurations.
    """
    vulnerabilities: List[Dict[str, Any]] = []

    if not banner and port == 21:
        vulnerabilities.append({
            "cve": "N/A",
            "severity": "Medium",
            "description": "FTP Service detected without banner response. Potential unencrypted authentication risk."
        })

    if banner:
        banner_lower: str = banner.lower()
        if "vsftpd 2.3.4" in banner_lower:
            vulnerabilities.append({
                "cve": "CVE-2011-2523",
                "severity": "Critical",
                "description": "vsftpd 2.3.4 Backdoor Command Execution vulnerability."
            })
        if "apache/2.4.49" in banner_lower:
            vulnerabilities.append({
                "cve": "CVE-2021-41773",
                "severity": "High",
                "description": "Apache HTTP Server 2.4.49 Path Traversal and Remote Code Execution."
            })

    return vulnerabilities