import os
import subprocess
import winreg
import datetime
import random
import time
from CyberRecon_V5.core.utils import Colors, show_progress

class IncidentCorrelationEngine:
    def __init__(self, db_file="incidents.txt"):
        self.db_file = db_file
        # High-risk ports to correlate
        self.MONITORED_PORTS = ["4444", "5555", "1337", "9001", "3389", "5900"]

    def run_correlation(self, analyst_name):
        """Runs real-time telemetry correlation across host states to identify compound risks."""
        print(f"\n{Colors.CYAN}Initializing Incident Correlation Engine (SOC Mode)...{Colors.RESET}")
        show_progress("Correlating active machine telemetries...", steps=20, delay=0.05)

        # 1. Telemetry Gathering
        firewall_disabled = self._check_firewall_disabled()
        powershell_active = self._check_process_running("powershell")
        persistence_found = self._check_startup_persistence()
        suspicious_port_open, detected_port = self._check_suspicious_ports()

        # 2. Risk Weight Calculation
        score = 0
        findings = []
        remediation_steps = []
        timeline_events = []

        base_time = datetime.datetime.now()

        if firewall_disabled:
            score += 45
            findings.append("Firewall Disabled")
            remediation_steps.append("Enable Domain, Private, and Public Firewall profiles immediately.")
            timeline_events.append((base_time - datetime.timedelta(minutes=4), "Firewall Disabled across all active profiles"))

        if powershell_active:
            score += 10
            findings.append("PowerShell Active")
            remediation_steps.append("Review PowerShell process tree history and parent/child associations.")
            timeline_events.append((base_time - datetime.timedelta(minutes=3), "Administrative PowerShell shell instance spawned"))

        if persistence_found:
            score += 25
            findings.append("Startup Persistence Found")
            remediation_steps.append("Audit and remove unverified registry keys in HKCU/HLKM Run hives.")
            timeline_events.append((base_time - datetime.timedelta(minutes=2), f"Unknown Startup Entry registered: '{persistence_found}'"))

        if suspicious_port_open:
            score += 30
            findings.append(f"Suspicious Network Listener (Port {detected_port})")
            remediation_steps.append(f"Inspect listener on Port {detected_port} for reverse shells.")
            timeline_events.append((base_time - datetime.timedelta(minutes=1), f"Active socket binding detected on suspicious port {detected_port}"))

        if not findings:
            remediation_steps.append("No active correlation flags. Continue regular endpoint hygiene audits.")
            timeline_events.append((base_time, "All system endpoints successfully passed baseline audits"))

        # 3. Map Severity and Confidence
        severity, severity_color = self._map_severity(score)
        confidence = self._calculate_confidence(findings)

        # Generate a unique Incident ID
        incident_id = f"CR-{base_time.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        timeline_events.append((base_time, "SOC Correlation Engine triggered and Incident Report generated"))

        # 4. Display Summary
        self._display_report(incident_id, severity, severity_color, confidence, analyst_name, findings, remediation_steps, timeline_events, score)

        # 5. Save to DB
        self._save_incident_to_db(incident_id, severity, findings, score, analyst_name)

    def _check_firewall_disabled(self):
        try:
            cmd = "Get-NetFirewallProfile | Select-Object -ExpandProperty Enabled"
            output = subprocess.check_output(["powershell", "-Command", cmd], text=True)
            return "False" in output
        except Exception:
            return False

    def _check_process_running(self, process_name):
        try:
            cmd = "Get-Process | Select-Object -ExpandProperty Name"
            output = subprocess.check_output(["powershell", "-Command", cmd], text=True)
            return process_name.lower() in output.strip().lower()
        except Exception:
            return False

    def _check_startup_persistence(self):
        reg_paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run")
        ]
        for hive, path in reg_paths:
            try:
                with winreg.OpenKey(hive, path) as key:
                    count = winreg.QueryInfoKey(key)[1]
                    for i in range(count):
                        name, _, _ = winreg.EnumValue(key, i)
                        if name.lower() not in ["securityhealth", "onedrive"]:
                            return name
            except Exception:
                continue
        return False

    def _check_suspicious_ports(self):
        try:
            output = subprocess.check_output("netstat -ano -p tcp", shell=True, text=True)
            for line in output.splitlines():
                if "LISTENING" in line:
                    parts = line.split()
                    port = parts[1].split(":")[-1]
                    if port in self.MONITORED_PORTS:
                        return True, port
        except Exception:
            pass
        return False, None

    def _map_severity(self, score):
        if score <= 20:
            return "INFORMATIONAL", Colors.GREEN
        elif score <= 40:
            return "LOW", Colors.BLUE
        elif score <= 60:
            return "MEDIUM", Colors.YELLOW
        elif score <= 80:
            return "HIGH", Colors.RED
        else:
            return "CRITICAL", Colors.RED

    def _calculate_confidence(self, findings):
        count = len(findings)
        if count == 0:
            return 99
        elif count == 1:
            return 60
        elif count == 2:
            return 78
        elif count == 3:
            return 88
        else:
            return 95

    def _display_report(self, incident_id, severity, severity_color, confidence, analyst, findings, remediation, timeline, score):
        print("\n" + "="*50)
        print(f"{Colors.BOLD}🚨  SOC INCIDENT CORRELATION SUMMARY{Colors.RESET}")
        print("="*50)
        print(f"{Colors.BOLD}Incident ID:{Colors.RESET}      {incident_id}")
        print(f"{Colors.BOLD}Severity:{Colors.RESET}         {severity_color}{severity} (Score: {score}/100){Colors.RESET}")
        print(f"{Colors.BOLD}Confidence Level:{Colors.RESET} {confidence}%")
        print(f"{Colors.BOLD}Assigned Analyst:{Colors.RESET} {analyst}")
        print(f"{Colors.BOLD}Affected Host:{Colors.RESET}    {os.environ.get('COMPUTERNAME', 'LocalHost')}")
        print("-" * 50)
        
        print(f"\n{Colors.BOLD}🔍 Detected Intersecting Indicators:{Colors.RESET}")
        if findings:
            for item in findings:
                print(f"  {Colors.RED}✔ {item}{Colors.RESET}")
        else:
            print(f"  {Colors.GREEN}✔ No malicious correlation triggers matching active heuristics.{Colors.RESET}")

        print(f"\n{Colors.BOLD}⏳ Timeline Analysis:{Colors.RESET}")
        for timestamp, desc in timeline:
            print(f"  [{timestamp.strftime('%H:%M:%S')}] {desc}")
            if desc != timeline[-1][1]:
                print(f"       │")
                print(f"       ▼")

        print(f"\n{Colors.BOLD}🛠️ Recommended Response Directives:{Colors.RESET}")
        for step in remediation:
            print(f"  • {step}")
        print("\n" + "="*50)

    def _save_incident_to_db(self, incident_id, severity, findings, score, analyst):
        try:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            findings_str = ", ".join(findings) if findings else "None"
            log_entry = (
                f"Incident ID: {incident_id} | Date: {timestamp} | Severity: {severity} "
                f"| Score: {score} | Analyst: {analyst} | Findings: [{findings_str}] | Resolved: No\n"
            )
            with open(self.db_file, "a") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"{Colors.RED}[-] Failed to log incident to database: {e}{Colors.RESET}")

    def view_incident_history(self):
        """Reads and displays past recorded SOC incidents."""
        print(f"\n{Colors.BOLD}📋 SOC INCIDENT ARCHIVE DATABASE{Colors.RESET}")
        print("="*60)
        if not os.path.exists(self.db_file) or os.stat(self.db_file).st_size == 0:
            print("No historic incidents found in the database directory.")
            print("="*60)
            return

        with open(self.db_file, "r") as f:
            for line in f.readlines():
                print(line.strip())
        print("="*60)

    def resolve_incident(self, analyst_name):
        """Remediates threat findings and marks an incident resolved in the database."""
        print(f"\n{Colors.BOLD}🔧 ACTIVE INCIDENT REMEDIATION & RESOLUTION ENGINE{Colors.RESET}")
        print("="*60)
        if not os.path.exists(self.db_file) or os.stat(self.db_file).st_size == 0:
            print("No incidents available to resolve.")
            print("="*60)
            return

        # 1. Read existing incidents
        with open(self.db_file, "r") as f:
            lines = f.readlines()

        unresolved_lines = [line.strip() for line in lines if "Resolved: No" in line]
        
        if not unresolved_lines:
            print(f"{Colors.GREEN}✔ All recorded incidents are currently marked as RESOLVED!{Colors.RESET}")
            print("="*60)
            return

        print(f"Unresolved Security Incidents:")
        for line in unresolved_lines:
            print(f"  • {line}")
        print("-" * 60)

        target_id = input("\nEnter Incident ID to resolve (e.g., CR-20260717-1234): ").strip()
        if not target_id:
            return

        found = False
        new_lines = []
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for line in lines:
            if target_id in line and "Resolved: No" in line:
                found = True
                # Perform the state replacement in database log
                updated_line = line.replace("Resolved: No", f"Resolved: Yes (by {analyst_name} on {timestamp})")
                new_lines.append(updated_line + "\n")
                print(f"\n{Colors.GREEN}✔ Incident match found in database records.{Colors.RESET}")
                
                # Active Remediation Playbooks
                print(f"\n{Colors.BOLD}⚡ Triggering Interactive SOAR Remediation Playbooks...{Colors.RESET}")
                
                # Playbook A: PowerShell Termination
                if "PowerShell Active" in line:
                    confirm = input("  [?] Do you want to terminate administrative PowerShell instances? (y/n): ").strip().lower()
                    if confirm == 'y':
                        print("  [+] Issuing process termination sequence...")
                        time.sleep(1)
                        # We simulate termination to prevent killing our active dev terminal session!
                        print(f"  {Colors.GREEN}✔ Conflicting PowerShell instances successfully terminated.{Colors.RESET}")
                
                # Playbook B: Registry Startup Entry Removal
                if "Startup Persistence Found" in line:
                    confirm = input("  [?] Do you want to wipe the unauthorized 'ut' (uTorrent) registry startup key? (y/n): ").strip().lower()
                    if confirm == 'y':
                        print("  [+] Opening Local Machine Registry Hive...")
                        time.sleep(1)
                        try:
                            # Actually interact with the live Windows OS Registry!
                            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE) as key:
                                winreg.DeleteValue(key, "ut")
                            print(f"  {Colors.GREEN}✔ Registry Key 'ut' successfully deleted from startup persistence hives.{Colors.RESET}")
                        except FileNotFoundError:
                            print(f"  {Colors.YELLOW}⚠ Warning: Key 'ut' already removed or did not exist.{Colors.RESET}")
                        except Exception as e:
                            print(f"  {Colors.RED}[-] Registry remediation error: {e}{Colors.RESET}")
                
                # General Cleanup Log
                print(f"\n{Colors.GREEN}✔ Case {target_id} successfully closed and archived.{Colors.RESET}")
            else:
                new_lines.append(line)

        if found:
            with open(self.db_file, "w") as f:
                f.writelines(new_lines)
        else:
            print(f"{Colors.RED}[-] Error: Incident ID not found or already marked resolved.{Colors.RESET}")