import os
import sys
import time
import datetime
import subprocess
import winreg
import msvcrt
import re
import logging

# Standardized logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("cyberrecon.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

try:
    from CyberRecon_V5.core.utils import Colors
except ImportError:
    # Fallback color class if utils isn't found
    class Colors:
        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        CYAN = "\033[96m"
        BOLD = "\033[1m"
        RESET = "\033[0m"


class SOAREngine:
    """Configurable SOAR engine demonstrating safe enterprise response policies."""
    def __init__(self, mode="passive"):
        """
        Supported modes:
          - "passive"    : Logs alerts without taking action.
          - "interactive": Prompts operator for confirmation before terminating processes.
          - "automatic"  : Automatically terminates matching malicious PIDs.
        """
        self.mode = mode.lower()

    def handle_threat(self, pid: int, process_name: str):
        logging.warning(f"SOAR Threat Evaluation Triggered: {process_name} (PID: {pid})")

        if self.mode == "passive":
            logging.info(f"[SOAR: PASSIVE] Alert logged. No automated containment for PID {pid}.")

        elif self.mode == "interactive":
            try:
                user_input = input(f"[SOAR: INTERACTIVE] Terminate process '{process_name}' (PID: {pid})? (y/n): ")
                if user_input.strip().lower() == 'y':
                    self._terminate_process(pid, process_name)
                else:
                    logging.info(f"[SOAR: INTERACTIVE] Action declined by operator for PID {pid}.")
            except EOFError:
                logging.warning("[SOAR: INTERACTIVE] No interactive terminal available. Defaulting to safe passive logging.")

        elif self.mode == "automatic":
            logging.warning(f"[SOAR: AUTOMATIC] Containment triggered on PID {pid}...")
            self._terminate_process(pid, process_name)

        else:
            logging.error(f"[SOAR] Unknown mode '{self.mode}'. Defaulting to passive logging.")

    def _terminate_process(self, pid: int, process_name: str):
        try:
            import signal
            os.kill(pid, signal.SIGTERM)
            logging.info(f"[SOAR] Successfully terminated process '{process_name}' (PID {pid}).")
        except Exception as e:
            logging.error(f"[SOAR] Failed to terminate process '{process_name}' (PID {pid}): {e}")


class EDRMonitor:
    def __init__(self, event_log="events.txt", soar_mode="passive"):
        self.event_log = event_log
        self.is_monitoring = False
        
        # Initialize Configurable SOAR Engine
        self.soar = SOAREngine(mode=soar_mode)
        
        # Callback hook for web-streaming
        self.on_telemetry_callback = None
        
        # 1. PERSISTENT STATE ENGINE: Initialize EID by reading database history
        self.current_eid = self._load_last_eid()
        
        # Baselines
        self.process_baseline = {}
        self.registry_baseline = set()
        self.firewall_baseline = True

        # Sliding memory buffer for behavioral correlation
        self.telemetry_buffer = []

        # MITRE ATT&CK Matrix
        self.mitre_matrix = {
            "powershell": {"id": "T1059.001", "name": "Command and Scripting Interpreter: PowerShell"},
            "cmd": {"id": "T1059.003", "name": "Command and Scripting Interpreter: Windows Command Shell"},
            "reg_add": {"id": "T1547.001", "name": "Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder"},
            "firewall_disable": {"id": "T1562.004", "name": "ImpairDefenses: Disable or Modify System Firewall"}
        }

    def _load_last_eid(self):
        """Scans events.txt to maintain persistent EID sequencing across sessions."""
        default_start = 1000
        if not os.path.exists(self.event_log):
            return default_start
        try:
            with open(self.event_log, "r") as f:
                lines = f.readlines()
                for line in reversed(lines):
                    match = re.search(r"\[EID-(\d+)\]", line)
                    if match:
                        return int(match.group(1))
        except Exception:
            pass
        return default_start

    def _get_active_processes(self):
        """Polls OS and uses unique PIDs as keys to track multiple instances of the same process."""
        process_map = {}
        try:
            cmd = "Get-CimInstance Win32_Process | Select-Object Name, ProcessId, ParentProcessId | ConvertTo-Json"
            output = subprocess.check_output(["powershell", "-Command", cmd], text=True)
            
            import json
            data = json.loads(output)
            
            # Ensure data is always a list even if a single item is returned
            if isinstance(data, dict):
                data = [data]
                
            pid_to_name = {proc["ProcessId"]: proc["Name"].lower() for proc in data if "ProcessId" in proc and proc.get("Name")}
            
            for proc in data:
                if "ProcessId" in proc and proc.get("Name"):
                    pid = proc["ProcessId"]
                    name = proc["Name"].lower()
                    p_pid = proc.get("ParentProcessId", 0)
                    parent_name = pid_to_name.get(p_pid, "explorer.exe")
                    
                    process_map[pid] = {"name": name, "parent": parent_name}
            return process_map
        except Exception:
            return {}

    def _get_registry_startup(self):
        found_keys = set()
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
                        found_keys.add(name.lower())
            except Exception:
                continue
        return found_keys

    def _get_firewall_status(self):
        try:
            cmd = "Get-NetFirewallProfile | Select-Object -ExpandProperty Enabled"
            output = subprocess.check_output(["powershell", "-Command", cmd], text=True)
            return "False" not in output
        except Exception:
            return True

    def _log_event(self, event_type, details, severity, mitre_id="-", mitre_name="-", pid=None):
        """Formats telemetry logs, writes to console, buffers for SIEM rules, and streams to web."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        self.current_eid += 1
        eid_str = f"EID-{self.current_eid}"
        
        # Color coding
        if severity == "HIGH":
            color = Colors.RED
        elif severity == "MEDIUM":
            color = Colors.YELLOW
        else:
            color = Colors.RESET

        mitre_display = mitre_id if mitre_id else "-"
        print(f"{eid_str:<10} [{timestamp}] {color}{event_type:<18} {details:<38} {mitre_display:<10} {severity:<8}{Colors.RESET}")
        if mitre_name and mitre_name != "-":
            print(f"   └── {Colors.CYAN}MITRE Context Detonated: {mitre_name}{Colors.RESET}")

        event_payload = {
            "eid": eid_str,
            "time": timestamp,
            "type": event_type,
            "details": details,
            "mitre": mitre_id,
            "severity": severity,
            "pid": pid
        }
        self.telemetry_buffer.append(event_payload)
        
        # Evaluate correlation
        self._evaluate_behavioral_correlation()

        # Web Dashboard dispatch
        if hasattr(self, 'on_telemetry_callback') and self.on_telemetry_callback:
            payload = {
                "event_type": "TELEMETRY",
                "data": {
                    "eid": eid_str,
                    "time": timestamp,
                    "classification": event_type,
                    "context": details,
                    "mitre": mitre_id,
                    "severity": severity
                }
            }
            try:
                self.on_telemetry_callback(payload)
            except Exception:
                pass

        return timestamp, eid_str

    def _evaluate_behavioral_correlation(self):
        """SIEM Correlation Engine: Evaluates rule logic and hands actionable threats to SOAR policy engine."""
        rule1_evidence = [
            e for e in self.telemetry_buffer
            if "cmd.exe" in str(e.get("details", "")).lower()
            or "powershell.exe" in str(e.get("details", "")).lower()
        ]

        has_cmd = any("cmd.exe" in str(e.get("details", "")).lower() for e in rule1_evidence)
        has_ps  = any("powershell.exe" in str(e.get("details", "")).lower() for e in rule1_evidence)

        if has_cmd and has_ps:
            evidence_eids = [e["eid"] for e in rule1_evidence]
            if self.on_telemetry_callback:
                self.on_telemetry_callback({
                    "event_type": "CORRELATION_ALERT",
                    "data": {"rule": "Rule-001", "title": "Suspicious Administrative Execution Sequence", "evidence": evidence_eids}
                })

            print(f"\n🚨 {Colors.RED}{Colors.BOLD}BEHAVIORAL CORRELATION ALERT: Rule-001 Triggered{Colors.RESET}")
            print(f"   └── {Colors.YELLOW}Title: Suspicious Administrative Execution Sequence{Colors.RESET}")
            print(f"   └── Confidence: {Colors.BOLD}88%{Colors.RESET}")
            print(f"   └── {Colors.RED}Evidence Chain: {', '.join(evidence_eids)}{Colors.RESET}")
            for e in rule1_evidence:
                print(f"      └── [{e['eid']}] {e['details']}")
            print(f"   └── Mapped Techniques: T1059.001, T1059.003")
            print(f"   └── {Colors.CYAN}Evaluating SOAR Response Policy...{Colors.RESET}\n")

            # Trigger SOAR evaluation for suspect processes in evidence chain
            for item in rule1_evidence:
                if item.get("pid"):
                    proc_name = item.get("details", "").split("->")[-1].strip()
                    self.soar.handle_threat(pid=item["pid"], process_name=proc_name)

            self.telemetry_buffer.clear()

    def start_detection_loop(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Colors.BOLD}========================================================================{Colors.RESET}")
        print(f"🛡️  CYBERRECON ENTERPRISE: CORRELATION & BEHAVIORAL MONITOR")
        print(f"{Colors.BOLD}========================================================================{Colors.RESET}")
        print(f"\n{Colors.CYAN}[*] Recovering session historical logs... Next Event ID will be: EID-{self.current_eid + 1}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Active SOAR Policy Mode: {self.soar.mode.upper()}{Colors.RESET}")
        
        self.process_baseline = self._get_active_processes()
        self.registry_baseline = self._get_registry_startup()
        self.firewall_baseline = self._get_firewall_status()
        
        print(f"{Colors.GREEN}✔ Persistent State Restored & Baselines Hooked!{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Core correlation rules engine live. Watching behaviors...{Colors.RESET}")
        print(f"{Colors.BOLD}👉 Press 'Q' to terminate telemetry context.{Colors.RESET}\n")
        
        print(f"{Colors.BLUE}{'Event ID':<10} {'Time':<10} {'Classification':<18} {'Process Relationship / Context':<38} {'MITRE ID':<10} {'Severity':<8}{Colors.RESET}")
        print("-" * 100)

        self.is_monitoring = True
        
        while self.is_monitoring:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                if key == 'q':
                    print(f"\n\n{Colors.YELLOW}[!] Suspending Enterprise EDR Context...{Colors.RESET}")
                    self.is_monitoring = False
                    break

            # 1. Advanced Process Tracking (PID Aware)
            current_processes = self._get_active_processes()
            new_pids = set(current_processes.keys()) - set(self.process_baseline.keys())
            
            if new_pids:
                for pid in new_pids:
                    proc_data = current_processes[pid]
                    proc_name = proc_data["name"]
                    base_name = proc_name.split(".exe")[0]
                    parent = proc_data["parent"]
                    relationship = f"{parent} -> {proc_name}"
                    
                    if "python.exe -> powershell.exe" in relationship:
                        continue
                    
                    mitre_info = self.mitre_matrix.get(base_name, {"id": "-", "name": "-"})
                    severity = "LOW"
                    if base_name in ["powershell", "cmd"]:
                        severity = "MEDIUM"
                    
                    t, eid = self._log_event("PROCESS_CREATED", relationship, severity, mitre_info["id"], mitre_info["name"], pid=pid)
                
                self.process_baseline = current_processes

            # 2. Firewall Status Polling
            current_fw = self._get_firewall_status()
            if current_fw != self.firewall_baseline:
                if not current_fw:
                    mitre_info = self.mitre_matrix["firewall_disable"]
                    t, eid = self._log_event("FIREWALL_DISABLED", "System Firewall turned OFF", "HIGH", mitre_info["id"], mitre_info["name"])
                else:
                    t, eid = self._log_event("FIREWALL_ENABLED", "System Firewall turned ON", "LOW")
                
                self.firewall_baseline = current_fw

            time.sleep(1)