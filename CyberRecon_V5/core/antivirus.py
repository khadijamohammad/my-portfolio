import subprocess
import json
import platform
from CyberRecon_V5.core.scanner_base import BaseScanner
from CyberRecon_V5.core.utils import Colors, show_progress

class AntivirusScanner(BaseScanner):
    """Validates real-time antivirus software signature version database age."""
    def __init__(self):
        super().__init__("Threat Signatures", "Signatures")

    def run(self):
        show_progress("Checking Threat Signature Age...", steps=15, delay=0.04)

        if platform.system() != "Windows":
            self.findings.append("Skipped: Non-Windows OS detected.")
            return

        try:
            cmd = ["powershell", "-NoProfile", "-Command", 
                   "Get-MpComputerStatus | Select-Object -Property AMServiceEnabled, AntispywareSignatureVersion, AntispywareSignatureLastUpdated | ConvertTo-Json"]
            
            out = subprocess.check_output(cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
            status = json.loads(out)
            
            service_running = status.get("AMServiceEnabled")
            sig_version = status.get("AntispywareSignatureVersion", "Unknown")
            raw_date = status.get("AntispywareSignatureLastUpdated", "")
            
            clean_date = raw_date.split(".")[0].replace("T", " ") if raw_date else "Unknown"
            def_ok = (service_running is True or str(service_running).lower() == "true")

            print(f"  Malware Engine:     " + (f"{Colors.GREEN}🟢 ACTIVE{Colors.RESET}" if def_ok else f"{Colors.RED}🔴 INACTIVE{Colors.RESET}"))
            print(f"  Signature Version:  📑 {Colors.CYAN}{sig_version}{Colors.RESET}")
            print(f"  Database Sync:      📅 {Colors.YELLOW}{clean_date}{Colors.RESET}")

            if not def_ok:
                self.risk_penalty += 20
                self.findings.append("Antivirus scanner engine is completely offline.")

        except Exception as e:
            self.risk_penalty += 15
            self.findings.append(f"Could not retrieve security signature state: {str(e)}")
            print(f"{Colors.RED}🔴 Signature intelligence telemetry unavailable.{Colors.RESET}")