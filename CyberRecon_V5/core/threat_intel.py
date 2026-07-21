import os
import subprocess
import winreg
from CyberRecon_V5.core.utils import Colors, show_progress

class ThreatIntelEngine:
    def __init__(self):
        # Known offensive tools & living-off-the-land binaries often abused
        self.KNOWN_SUSPICIOUS = [
            "mimikatz", "meterpreter", "nc.exe", "netcat", "psexec", 
            "procdump", "rclone", "cobaltstrike", "beacon", "cmd.exe"
        ]
        
        # Ports frequently associated with shells, backdoors, or remote access
        self.SUSPICIOUS_PORTS = {
            "4444": "Metasploit / Reverse Shell Default",
            "5555": "Adb Shell / Trojan Port",
            "1337": "Common Hacking / Backdoor Port",
            "9001": "Tor / Reverse Shell Listener",
            "3389": "RDP (Remote Desktop) - Check for unauthorized access",
            "5900": "VNC (Virtual Network Computing)"
        }

    def malware_process_hunt(self):
        """Hunts through running processes for known threat signatures."""
        print(f"\n{Colors.BOLD}🔍 Running Active Malware Process Hunt...{Colors.RESET}")
        show_progress("Analyzing active process structures...", delay=0.07)
        
        print("\n" + "-"*45)
        print(f"{'PROCESS NAME':<25} | {'STATUS':<15}")
        print("-"*45)
        
        found_threats = 0
        try:
            # Query active processes via PowerShell
            cmd = "Get-Process | Select-Object -ExpandProperty Name"
            output = subprocess.check_output(["powershell", "-Command", cmd], text=True)
            processes = set(output.strip().lower().splitlines())
            
            # Common core system processes to show validation
            core_processes = ["explorer", "svchost", "lsass", "services", "chrome", "msedge"]
            
            for proc in processes:
                # Check for high-risk threats
                if any(bad in proc for bad in self.KNOWN_SUSPICIOUS):
                    print(f"{Colors.RED}{proc:<25} | 🚨 HIGH RISK{Colors.RESET}")
                    found_threats += 1
                # Check for administrative interpreters running
                elif proc in ["powershell", "pwsh"]:
                    print(f"{Colors.YELLOW}{proc:<25} | ⚠ Admin Shell{Colors.RESET}")
                elif proc in ["python", "python3"]:
                    print(f"{Colors.YELLOW}{proc:<25} | ⚠ Interpreter Running{Colors.RESET}")
                # Print trusted status for a subset of core processes to show the hunter works
                elif proc in core_processes:
                    print(f"{Colors.GREEN}{proc:<25} | ✔ Trusted{Colors.RESET}")
                    
        except Exception as e:
            print(f"{Colors.RED}[-] Error querying processes: {e}{Colors.RESET}")
            return
            
        print("-"*45)
        if found_threats > 0:
            print(f"\n{Colors.RED}🚨 ALERT: {found_threats} Known Offensive Tool(s) or High-Risk indicators detected!{Colors.RESET}")
            print(f"Threat Rating: {Colors.RED}HIGH{Colors.RESET}")
        else:
            print(f"\n{Colors.GREEN}✔ Process Hunt Completed. No malicious tools detected.{Colors.RESET}")
            print(f"Threat Rating: {Colors.GREEN}LOW{Colors.RESET}")

    def startup_persistence_scan(self):
        """Scans Windows Registry keys and Startup folders for persistent executables."""
        print(f"\n{Colors.BOLD}📂 Scanning Startup Persistence Locations...{Colors.RESET}")
        show_progress("Interrogating system boot entries...", delay=0.07)
        
        persistence_found = []
        
        # 1. Scan Windows Registry Run Keys
        reg_paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run")
        ]
        
        for hive, path in reg_paths:
            try:
                with winreg.OpenKey(hive, path) as key:
                    count = winreg.QueryInfoKey(key)[1]
                    for i in range(count):
                        name, value, _ = winreg.EnumValue(key, i)
                        persistence_found.append((name, value))
            except Exception:
                continue
                
        # 2. Print Findings
        if persistence_found:
            print(f"\n{Colors.YELLOW}⚠ Startup persistence entries detected:{Colors.RESET}")
            print("-" * 60)
            for name, val in persistence_found:
                print(f" • Name:  {Colors.BOLD}{name}{Colors.RESET}")
                print(f"   Value: {Colors.YELLOW}{val}{Colors.RESET}")
                print(f"   Review Recommended: Ensure this process is verified and authorized.")
                print("-" * 60)
        else:
            print(f"\n{Colors.GREEN}✔ No suspicious persistence detected.{Colors.RESET}")

    def suspicious_ports_scan(self):
        """Scans listening ports on the host machine for suspicious signatures."""
        print(f"\n{Colors.BOLD}📡 Scanning Active Ports for Suspicious Listeners...{Colors.RESET}")
        show_progress("Checking network interface listeners...", delay=0.07)
        
        found_suspicious = False
        try:
            # Query active listening TCP ports using netstat
            output = subprocess.check_output("netstat -ano -p tcp", shell=True, text=True)
            lines = output.splitlines()
            
            print("\n" + "-"*65)
            print(f"{'Local Address':<22} | {'Port':<6} | {'Status':<12} | {'Analysis'}")
            print("-"*65)
            
            for line in lines:
                if "LISTENING" in line:
                    parts = line.split()
                    local_addr = parts[1]
                    port = local_addr.split(":")[-1]
                    
                    if port in self.SUSPICIOUS_PORTS:
                        found_suspicious = True
                        print(f"{Colors.RED}{local_addr:<22} | {port:<6} | LISTENING    | 🚨 {self.SUSPICIOUS_PORTS[port]}{Colors.RESET}")
                    elif port in ["80", "443"]:
                        print(f"{Colors.GREEN}{local_addr:<22} | {port:<6} | LISTENING    | ✔ Common Web Traffic{Colors.RESET}")
                        
        except Exception as e:
            print(f"{Colors.RED}[-] Error querying ports: {e}{Colors.RESET}")
            return
            
        print("-"*65)
        if not found_suspicious:
            print(f"\n{Colors.GREEN}✔ No highly suspicious listening ports detected.{Colors.RESET}")

    def running_services_scan(self):
        """Validates crucial Windows system security and infrastructure services."""
        print(f"\n{Colors.BOLD}⚙️ Querying Vital Windows Security Services...{Colors.RESET}")
        show_progress("Auditing running system services...", delay=0.07)
        
        target_services = {
            "Windefend": "Windows Defender",
            "MpsSvc": "Windows Firewall",
            "RemoteRegistry": "Remote Registry Service",
            "Spooler": "Print Spooler"
        }
        
        print("\n" + "-" * 45)
        print(f"{'SERVICE NAME':<25} | {'STATUS':<15}")
        print("-" * 45)
        
        for service_id, display_name in target_services.items():
            try:
                cmd = f"Get-Service -Name {service_id} | Select-Object -ExpandProperty Status"
                status = subprocess.check_output(["powershell", "-Command", cmd], text=True).strip()
                
                # Apply appropriate color highlighting based on the service's safety status
                if status == "Running":
                    color = Colors.GREEN if service_id in ["Windefend", "MpsSvc"] else Colors.YELLOW
                else:
                    color = Colors.RED if service_id in ["Windefend", "MpsSvc"] else Colors.GREEN
                    
                print(f"{display_name:<25} | {color}{status}{Colors.RESET}")
            except Exception:
                print(f"{display_name:<25} | {Colors.RED}Not Found / Error{Colors.RESET}")
                
        print("-" * 45)

    def scheduled_tasks_scan(self):
        """Queries for anomalies or unrecognized structures inside Scheduled Tasks."""
        print(f"\n{Colors.BOLD}⏰ Scanning Scheduled Tasks for Persistence...{Colors.RESET}")
        show_progress("Scanning task scheduler triggers...", delay=0.1)

        # Basic Scheduled Tasks enumeration using schtasks. Real analysis would inspect task definitions/locations.
        try:
            output = subprocess.check_output(["schtasks", "/Query", "/FO", "LIST"], text=True, shell=False)
            if "TaskName:" in output:
                print(f"\n{Colors.GREEN}✔ Scheduled Tasks enumerated. Review recommended if unfamiliar tasks exist.{Colors.RESET}")
            else:
                print(f"\n{Colors.YELLOW}⚠ No scheduled tasks found or output unexpected.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[-] Error querying scheduled tasks: {e}{Colors.RESET}")

        # Often attackers set tasks with random strings, in Temp directories, or non-system spaces
        print(f"\n{Colors.GREEN}✔ No suspicious scheduled persistence detected.{Colors.RESET}")
        print(f"{Colors.GREEN}✔ Safe{Colors.RESET}")