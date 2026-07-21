import subprocess
import json
import platform
import socket
from CyberRecon_V5.core.scanner_base import BaseScanner
from CyberRecon_V5.core.utils import Colors, show_progress

class NetworkScanner(BaseScanner):
    """Diagnoses active local network adapters and IP configurations."""
    def __init__(self):
        super().__init__("Network Interface Scanner", "Network")

    def run(self):
        show_progress("Interrogating Network Adapters...", steps=15, delay=0.04)
        
        # 1. Grab hostname & local IP address via sockets
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        except Exception:
            hostname = "Unknown"
            local_ip = "127.0.0.1"

        print(f"  Local Hostname:    {Colors.CYAN}{hostname}{Colors.RESET}")
        print(f"  Primary Local IP:  {Colors.CYAN}{local_ip}{Colors.RESET}")
        print("-" * 50)

        # 2. Grab detailed interface adapter status
        if platform.system() != "Windows":
            self.findings.append("Skipped adapter detail check: Non-Windows OS.")
            return

        try:
            cmd = ["powershell", "-NoProfile", "-Command", 
                   "Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike '127.*'} | Select-Object -Property InterfaceAlias, IPAddress | ConvertTo-Json"]
            
            out = subprocess.check_output(cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
            
            if out:
                adapters = json.loads(out)
                if isinstance(adapters, dict):
                    adapters = [adapters]
                
                print(f"{Colors.BOLD}{'Interface Alias':<20} | {'Assigned IP Address':<15}{Colors.RESET}")
                print("-" * 50)
                for adapter in adapters:
                    alias = adapter.get("InterfaceAlias", "Unknown")
                    ip = adapter.get("IPAddress", "Unknown")
                    print(f"{alias:<20} | {ip:<15}")
            else:
                print(f"{Colors.YELLOW}⚠️  No active physical IPv4 network adapters detected.{Colors.RESET}")
                self.risk_penalty += 10
                self.findings.append("No active physical IPv4 interfaces found.")

        except Exception as e:
            self.risk_penalty += 5
            self.findings.append(f"Network telemetry error: {str(e)}")
            print(f"{Colors.RED}🔴 Network telemetry scan interrupted.{Colors.RESET}")