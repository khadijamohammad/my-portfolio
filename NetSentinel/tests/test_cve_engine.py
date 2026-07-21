from core.cve_engine import check_vulnerabilities


def test_check_vulnerabilities_vsftpd():
    banner = "220 (vsFTPd 2.3.4)"
    vulns = check_vulnerabilities(banner, 21)
    
    assert len(vulns) == 1
    assert vulns[0]["cve"] == "CVE-2011-2523"
    assert vulns[0]["severity"] == "Critical"


def test_check_vulnerabilities_apache():
    banner = "Server: Apache/2.4.49 (Unix)"
    vulns = check_vulnerabilities(banner, 80)
    
    assert len(vulns) == 1
    assert vulns[0]["cve"] == "CVE-2021-41773"
    assert vulns[0]["severity"] == "High"


def test_check_vulnerabilities_clean_banner():
    banner = "OpenSSH 8.2p1 Ubuntu"
    vulns = check_vulnerabilities(banner, 22)
    
    assert len(vulns) == 0