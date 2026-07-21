import platform
import shutil
import subprocess
import os
from CyberRecon_V5.core.scanner_base import BaseScanner
from CyberRecon_V5.core.utils import Colors, show_progress

class HardwareScanner(BaseScanner):
    """Gathers authentic hardware inventory, system resources, and disk storage."""
    def __init__(self):
        super().__init__("Hardware Diagnostics", "Hardware")

    def run(self):
        show_progress("Gathering Hardware Inventory...", steps=15, delay=0.04)

        # 1. OS details
        os_name = platform.system()
        os_release = platform.release()
        print(f"  Operating System:  {Colors.BOLD}{os_name} {os_release}{Colors.RESET}")

        # 2. CPU logic cores
        cpu_cores = os.cpu_count()
        print(f"  CPU Logical Cores: {Colors.CYAN}{cpu_cores}{Colors.RESET}")

        # 3. Live Disk usage on root
        try:
            # Check the primary drive ('C:\' on Windows, '/' on Unix)
            root_drive = "C:\\" if os_name == "Windows" else "/"
            total, used, free = shutil.disk_usage(root_drive)
            
            # Convert bytes to Gigabytes
            total_gb = total // (2**30)
            used_gb = used // (2**30)
            free_gb = free // (2**30)
            free_pct = int((free / total) * 100)

            print(f"  Storage ({root_drive}):      {Colors.CYAN}{used_gb} GB / {total_gb} GB Used ({free_pct}% Free){Colors.RESET}")
            
            if free_pct < 10:
                self.risk_penalty += 15
                self.findings.append(f"Primary storage partition ({root_drive}) is critical: Under 10% space free!")
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  Could not retrieve storage metrics: {str(e)}{Colors.RESET}")

        # 4. Total Installed RAM (Windows Specific check)
        if os_name == "Windows":
            try:
                cmd = ["powershell", "-NoProfile", "-Command", 
                       "(Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum).Sum"]
                out = subprocess.check_output(cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
                if out:
                    total_bytes = int(out)
                    total_ram_gb = total_bytes // (1024**3)
                    print(f"  Installed RAM:     {Colors.CYAN}{total_ram_gb} GB{Colors.RESET}")
                    
                    if total_ram_gb < 8:
                        self.risk_penalty += 5
                        self.findings.append("System installed RAM is below minimum recommended 8 GB.")
            except Exception:
                pass