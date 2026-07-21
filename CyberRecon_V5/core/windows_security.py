import subprocess
import json
import platform
from CyberRecon_V5.core.scanner_base import BaseScanner
from CyberRecon_V5.core.utils import Colors, show_progress

class WindowsSecurityScanner(BaseScanner):
    """Diagnoses core Windows Defender Antivirus and Real-Time Protection states."""
    def __init__(self):
        super().__init__("Windows Security Core", "Defender")

    def run(self):
        show_progress("Interrogating Windows Security Agents...", steps=15, delay=0.04)
        
        if platform.system() != "Windows":
            self.findings.append("Skipped: Non-Windows OS detected.")
            return

        try:
            cmd = ["powershell", "-NoProfile", "-Command", 
                   "Get-MpComputerStatus | Select-Object -Property AMServiceEnabled, RealTimeProtectionEnabled | ConvertTo-Json"]
            
            out = subprocess.check_output(cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
            status = json.loads(out)
            
            service_running = status.get("AMServiceEnabled")
            realtime_active = status.get("RealTimeProtectionEnabled")

            def_ok = (service_running is True or str(service_running).lower() == "true")
            rt_ok = (realtime_active is True or str(realtime_active).lower() == "true")

            print(f"{Colors.BOLD}Windows Defender Status:{Colors.RESET}")
            print(f"  Malware Engine:     " + (f"{Colors.GREEN}🟢 Running{Colors.RESET}" if def_ok else f"{Colors.RED}🔴 Stopped{Colors.RESET}"))
            print(f"  Real-Time Shield:   " + (f"{Colors.GREEN}🟢 Active{Colors.RESET}" if rt_ok else f"{Colors.RED}🔴 Disabled{Colors.RESET}"))

            if not def_ok:
                self.risk_penalty += 25
                self.findings.append("Windows Defender service is completely stopped!")
            if not rt_ok:
                self.risk_penalty += 20
                self.findings.append("Real-Time protection shield is deactivated.")

        except Exception as e:
            self.risk_penalty += 15
            self.findings.append(f"Failed to query local threat agent telemetry: {str(e)}")
            print(f"{Colors.RED}🔴 Error executing core security diagnostic queries.{Colors.RESET}")