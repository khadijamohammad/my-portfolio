import subprocess
import json
import platform
from CyberRecon_V5.core.scanner_base import BaseScanner
from CyberRecon_V5.core.utils import Colors, show_progress

class FirewallScanner(BaseScanner):
    """Scans and parses Windows Advanced Firewall profiles and connection policies."""
    def __init__(self):
        super().__init__("Network Boundary Firewall", "Firewall")

    def run(self):
        show_progress("Analyzing Advanced Firewall Boundaries...", steps=15, delay=0.04)

        if platform.system() != "Windows":
            self.findings.append("Skipped: Non-Windows OS detected.")
            return

        try:
            cmd = ["powershell", "-NoProfile", "-Command", 
                   "Get-NetFirewallProfile | Select-Object -Property Name, Enabled, DefaultInboundAction, DefaultOutboundAction | ConvertTo-Json"]
            
            out = subprocess.check_output(cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
            profiles = json.loads(out)
            
            if isinstance(profiles, dict):
                profiles = [profiles] # Normalize single-profile structures

            print(f"{Colors.BOLD}{'Profile Name':<12} | {'Status':<10} | {'Inbound Policy':<15} | {'Outbound Policy'}{Colors.RESET}")
            print("-" * 65)

            disabled_profiles = []
            for profile in profiles:
                name = profile.get("Name", "Unknown")
                enabled = profile.get("Enabled")
                inbound = profile.get("DefaultInboundAction", "Unknown")
                outbound = profile.get("DefaultOutboundAction", "Unknown")

                is_enabled = (enabled is True or str(enabled).lower() == "true")
                status_str = f"{Colors.GREEN}🟢 ENABLED{Colors.RESET}" if is_enabled else f"{Colors.RED}🔴 DISABLED{Colors.RESET}"

                if not is_enabled:
                    disabled_profiles.append(name)
                    self.risk_penalty += 15

                print(f"{name:<12} | {status_str:<10} | {inbound:<15} | {outbound}")

            print("-" * 65)

            if disabled_profiles:
                self.findings.append(f"Firewall profiles are disabled: {', '.join(disabled_profiles)}")
            else:
                print(f"\n{Colors.GREEN}🟢 All network firewall boundaries are locked down and operational.{Colors.RESET}")

        except Exception as e:
            self.risk_penalty += 15
            self.findings.append(f"Failed to query network firewall profiles: {str(e)}")
            print(f"{Colors.RED}🔴 Error: Network security policy prevents hardware firewall queries.{Colors.RESET}")