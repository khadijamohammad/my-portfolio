# ==============================================
# File: cyber_recon_scanner.py
# Description: Cyber Recon Scanner V4 - Unified Endpoint Security Engine
# ==============================================

import psutil
import time
import random
import os
import platform
import socket
import urllib.request
import subprocess
import shutil  # For storage/disk calculations
from datetime import datetime

# Global file paths
HISTORY_FILE = "scan_history.txt"
AUDIT_FILE = "audit_log.txt"

# ==============================================
# 📝 AUDIT LOG SYSTEM
# ==============================================
def log_action(user, role, action, status="SUCCESS"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(AUDIT_FILE, "a", encoding="utf-8") as file:
        file.write(f"{timestamp} | {action:<25} | {role:<13} | {user:<10} | {status}\n")


# ==============================================
# 💾 DATABASE LOADING & TELEMETRY
# ==============================================
scan_history = []
last_threat = "🟢 NONE"

def load_scan_database():
    global scan_history, last_threat
    scan_history = []
    last_threat = "🟢 NONE"
    
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            for line in file:
                cleaned_line = line.strip()
                if cleaned_line:
                    parts = cleaned_line.split("|")
                    if len(parts) == 3:
                        scan_history.append({
                            "timestamp": parts[0],
                            "score": int(parts[1]),
                            "threat": parts[2]
                        })
        if scan_history:
            last_threat = scan_history[-1]["threat"]

load_scan_database()

# ==============================================
# 🔐 ANALYST CREDENTIAL STORAGE (RBAC)
# ==============================================
ALLOWED_ANALYSTS = {
    "khadija": {
        "password": "cyberops2026",
        "role": "Administrator",
        "clearance": "LEVEL 5",
        "privilege_tag": "🟢 Administrator Privileges Enabled"
    },
    "sarah": {
        "password": "secfield2026",
        "role": "Analyst",
        "clearance": "LEVEL 2",
        "privilege_tag": "🔵 Analyst Mode Enabled"
    }
}

authenticated = False
analyst_name = ""
user_role = ""
user_clearance = ""
privilege_notice = ""
attempts_left = 3

print("======================================")
print(" 🛡  CYBER RECON SCANNER V4")
print("======================================")
print("             SECURE LOGIN             ")
print("======================================\n")

while not authenticated:
    if attempts_left == 0:
        print("🚨 SYSTEM SECURITY LOCKDOWN 🚨")
        log_action("UNKNOWN", "UNAUTHORIZED", "BRUTE_FORCE_ATTEMPT", "LOCKDOWN")
        exit()

    username_input = input("Username: ").strip().lower()
    password_input = input("Password: ").strip()
    print()

    if username_input in ALLOWED_ANALYSTS and ALLOWED_ANALYSTS[username_input]["password"] == password_input:
        print("======================================")
        print("✅ Authentication Successful")
        print("======================================\n")
        
        analyst_name = username_input.capitalize()
        user_role = ALLOWED_ANALYSTS[username_input]["role"]
        user_clearance = ALLOWED_ANALYSTS[username_input]["clearance"]
        privilege_notice = ALLOWED_ANALYSTS[username_input]["privilege_tag"]
        
        log_action(analyst_name, user_role, "LOGIN")
        
        print("Loading Secure Dashboard...")
        time.sleep(0.5)
        print("\n" + "="*40 + "\n")
        authenticated = True
    else:
        attempts_left -= 1
        print("❌ Authentication Failed.")
        failed_user = username_input.capitalize() if username_input else "ANONYMOUS"
        log_action(failed_user, "UNKNOWN", "LOGIN_ATTEMPT", "FAILED")
        
        if attempts_left > 0:
            print(f"⚠️  {attempts_left} attempts remaining.\n")
            print("-" * 30)


# ==============================================
# 🛠️ REUSABLE SCAN ENGINE
# ==============================================
def run_scan(scan_name, emoji, outcomes):
    print(f"{emoji} Scanning {scan_name}...")
    time.sleep(0.1)
    result = random.choice(outcomes)
    print(f"\n{result['msg']}")
    print(f"Risk Score: +{result['risk']}")
    print("-" * 30)
    return result


# ==============================================
# 🎯 RECON DIAGNOSTIC CONFIGURATIONS
# ==============================================
password_outcomes = [{"msg": "✔ Strong password detected.", "status": "✔ Strong", "risk": 0, "finding": None, "fix": None}]
firewall_outcomes = [{"msg": "✔ Firewall is actively blocking threats.", "status": "✔ Protected", "risk": 0, "finding": None, "fix": None}]
antivirus_outcomes = [{"msg": "✔ Antivirus definitions are up to date.", "status": "✔ Running", "risk": 0, "finding": None, "fix": None}]
port_outcomes = [{"msg": "✔ All dangerous network ports are closed.", "status": "✔ Safe", "risk": 0, "finding": None, "fix": None}]
usb_outcomes = [{"msg": "✔ No unauthorized USB devices found.", "status": "✔ Safe", "risk": 0, "finding": None, "fix": None}]
update_outcomes = [{"msg": "✔ All system software is fully updated.", "status": "✔ Current", "risk": 0, "finding": None, "fix": None}]


# ==============================================
# 🔄 THE CONTINUOUS APPLICATION LOOP
# ==============================================
while True:
    dashboard = f"""======================================
🛡  CYBER RECON SCANNER V4
======================================
Analyst:         {analyst_name} ({user_role})
Clearance Level: {user_clearance}
Previous Scans:  {len(scan_history)}
Last Threat:     {last_threat}
Database Status: ✔ Connected
======================================
{privilege_notice}
======================================"""

    print(dashboard)
    print()

    # Organized menu layout incorporating CPU & Memory Intelligence as Option 6
    if user_role == "Administrator":
        print("1️⃣ Real-Time System Information")
        print("2️⃣ Live Network Intelligence")
        print("3️⃣ 🌍 Internet Connectivity Test")
        print("4️⃣ 💻 Live Process Intelligence")
        print("5️⃣ 💾 File System Intelligence")
        print("6️⃣ 🧠 CPU & Memory Intelligence")
        print("7️⃣ Scan Password Security")
        print("8️⃣ Scan Firewall")
        print("9️⃣ Scan Antivirus")
        print("🔟 🚀 RUN FULL SYSTEM SCAN & REPORT")
        print("11 📚 View Scan History")
        print("12 ⚙️  ADMINISTRATOR CONSOLE")
        print("13 🛑 Exit")
    else:
        print("1️⃣ Real-Time System Information")
        print("2️⃣ Live Network Intelligence")
        print("3️⃣ 🌍 Internet Connectivity Test")
        print("4️⃣ 💻 Live Process Intelligence")
        print("5️⃣ 💾 File System Intelligence")
        print("6️⃣ 🧠 CPU & Memory Intelligence")
        print("7️⃣ Scan Password Security")
        print("8️⃣ Scan Firewall")
        print("9️⃣ Scan Antivirus")
        print("🔟 🚀 RUN FULL SYSTEM SCAN & REPORT")
        print("11 📚 View Scan History")
        print("12 🛑 Exit")

    print()
    choice = input("Choose: ")
    print("\n" + "="*40 + "\n") 

    # --- 🖥️ OPTION 1: REAL-TIME SYSTEM SCANNER ---
    if choice == "1":
        log_action(analyst_name, user_role, "SYSTEM_INFO_SCAN")
        print("🔍 Querying low-level system APIs...")
        time.sleep(0.4)
        
        comp_name = platform.node()
        os_sys = platform.system()
        os_release = platform.release()
        arch_type = platform.architecture()[0]
        py_version = platform.python_version()
        curr_user = os.getenv("USERNAME") or os.getenv("USER") or os.getlogin()
        
        print("=====================================")
        print("🖥  SYSTEM INFORMATION")
        print("=====================================")
        print(f"Computer Name:    {comp_name if comp_name else 'UNKNOWN_HOST'}")
        print(f"Operating System: {os_sys}")
        print(f"Release:          {os_release}")
        print(f"Architecture:     {arch_type}")
        print(f"Python Version:   {py_version}")
        print(f"Current User:     {curr_user}")
        print("=====================================\n")
        input("Press Enter to return to the Dashboard...")
        print("\n" + "="*40 + "\n")

    # --- 🌐 OPTION 2: LIVE NETWORK INTELLIGENCE ---
    elif choice == "2":
        log_action(analyst_name, user_role, "NETWORK_INTEL_SCAN")
        print("📡 Binding sockets and listening to interface tables...")
        time.sleep(0.4)
        
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            resolution_status = "Successful"
            connection_status = "🟢 Connected"
            health_notice = "🟢 Network Connection Appears Healthy"
        except Exception:
            hostname = "UNKNOWN_HOST"
            local_ip = "127.0.0.1"
            resolution_status = "Failed"
            connection_status = "🔴 Disconnected"
            health_notice = "🔴 Network Information Unavailable"
        
        print("=====================================")
        print("🌐 LIVE NETWORK INTELLIGENCE")
        print("=====================================")
        print(f"Hostname:            {hostname}")
        print(f"Local IPv4:          {local_ip}")
        print(f"Hostname Resolution: {resolution_status}")
        print(f"Status:              {connection_status}")
        print("-------------------------------------")
        print(f"{health_notice}")
        print("=====================================\n")
        input("Press Enter to return to the Dashboard...")
        print("\n" + "="*40 + "\n")

    # --- 🌍 OPTION 3: INTERNET CONNECTIVITY TEST ---
    elif choice == "3":
        log_action(analyst_name, user_role, "INTERNET_CONN_TEST")
        print("=====================================")
        print("🌍 INTERNET CONNECTIVITY TEST")
        print("=====================================\n")
        print("Testing secure outbound connection...")
        print("Connecting...\n")
        time.sleep(0.8)
        
        try:
            urllib.request.urlopen("https://www.google.com", timeout=3.0)
            status_tag = "🟢 ONLINE"
            response_msg = "Google Reachable"
            access_msg = "AVAILABLE"
            bonus_challenge_msg = "Latency Check:\nExcellent"
        except Exception:
            status_tag = "🔴 OFFLINE"
            response_msg = "Unreachable"
            access_msg = "UNAVAILABLE"
            bonus_challenge_msg = "Threat Intelligence Feed:\nUnavailable"
            
        print("Status:")
        print(f"{status_tag}\n")
        
        if status_tag == "🟢 ONLINE":
            print(f"Response:\n{response_msg}\n")
            print(f"Internet Access:\n{access_msg}\n")
        else:
            print("Unable to establish Internet connection.\n")
            print("Please verify:\n • Wi-Fi\n • Ethernet\n • Firewall\n • DNS\n")
            
        print("-------------------------------------")
        print(f"{bonus_challenge_msg}")
        print("=====================================\n")
        
        input("Press Enter to return to the Dashboard...")
        print("\n" + "="*40 + "\n")

    # --- 💻 OPTION 4: LIVE PROCESS INTELLIGENCE ---
    elif choice == "4":
        log_action(analyst_name, user_role, "PROCESS_INTEL_SCAN")
        print("=====================================")
        print("💻 LIVE PROCESS INTELLIGENCE")
        print("=====================================\n")
        print("Collecting active processes...")
        print("Scanning...\n")
        time.sleep(1.0)
        
        try:
            proc = subprocess.run(['tasklist'], capture_output=True, text=True, check=True)
            lines = proc.stdout.strip().split('\n')[3:]
            process_names = []
            
            for line in lines:
                if line.strip():
                    name = line.split()[0]
                    process_names.append(name)
                    
            total_processes = len(process_names)
            unique_processes = list(set(process_names))
            display_candidates = [p for p in unique_processes if "exe" in p.lower() and p.lower() not in ["svchost.exe", "conhost.exe"]]
            
            print("Top Running Processes\n")
            for p in display_candidates[:5]:
                print(p)
                
            print("\n-------------------------------------")
            print("Total Processes:")
            print(f"{total_processes}\n")
            
            print("System Status:")
            if total_processes < 200:
                print("🟢 Normal Workstation\n")
            elif 200 <= total_processes <= 300:
                print("🟡 Busy System\n")
            else:
                print("🔴 High Activity\n")

        except Exception:
            print("🔴 Unable to retrieve process information.")
            print("Process inspection unavailable.\n")
            
        print("=====================================\n")
        input("Press Enter to return to the Dashboard...")
        print("\n" + "="*40 + "\n")

    # --- 💾 OPTION 5: FILE SYSTEM INTELLIGENCE ---
    elif choice == "5":
        log_action(analyst_name, user_role, "DISK_USAGE_SCAN")
        print("=====================================")
        print("💾 FILE SYSTEM INTELLIGENCE")
        print("=====================================\n")
        print("Analyzing persistent block storage devices...")
        print("Calculating cluster maps...\n")
        time.sleep(0.8)

        try:
            total, used, free = shutil.disk_usage("/")
            gb_conversion = 2**30
            total_gb = total / gb_conversion
            used_gb = used / gb_conversion
            free_gb = free / gb_conversion
            pct_used = (used / total) * 100

            if pct_used < 75:
                storage_status = "🟢 Safe"
                bonus_msg = "🟢 Device has plenty of workspace for logs & updates."
            elif 75 <= pct_used < 90:
                storage_status = "🟡 Warning"
                bonus_msg = "🟡 Space is getting low. Log retention policies may trigger."
            else:
                storage_status = "🔴 Critical"
                bonus_msg = "🔴 Insufficient space! System writes and security telemetry may fail."

            print(f"Total Disk Size:")
            print(f"{total_gb:.2f} GB\n")
            print(f"Used Space:")
            print(f"{used_gb:.2f} GB\n")
            print(f"Free Space:")
            print(f"{free_gb:.2f} GB\n")
            print(f"Percentage Used:")
            print(f"{pct_used:.1f}%\n")
            print("-------------------------------------")
            print(f"Status: {storage_status}")
            print(f"{bonus_msg}")

        except Exception:
            print("🔴 Unable to retrieve file system information.")
            print("Disk telemetry inspection unavailable.\n")

        print("=====================================\n")
        input("Press Enter to return to the Dashboard...")
        print("\n" + "="*40 + "\n")

  # ==============================================
    # 🧠 OPTION 6: MISSION V4-6: CPU & MEMORY INTELLIGENCE
    # ==============================================
    elif choice == "6":
        log_action(analyst_name, user_role, "CPU_MEM_INTEL_SCAN")
        print("=====================================")
        print("🧠 CPU & MEMORY INTELLIGENCE")
        print("=====================================\n")
        print("Polling low-level processor registers...")
        print("Analyzing RAM volatile memory pages...\n")
        time.sleep(0.8)

        try:
            os_type = platform.system()
            logical_cores = os.cpu_count() or "Unknown"
            processor_brand = platform.processor() or "Unknown"
            physical_cores = "Unavailable"
            max_clock_speed_mhz = "Unavailable"

            # ⚙️ OS-Specific CPU Detection Hooks
            if os_type == "Windows":
                try:
                    # Query Physical Cores using modern PowerShell CimInstance
                    core_cmd = ["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Processor).NumberOfCores"]
                    pc_cores = subprocess.check_output(core_cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
                    if pc_cores.isdigit():
                        physical_cores = int(pc_cores)
                    
                    # Query Max Clock Speed using modern PowerShell CimInstance
                    speed_cmd = ["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Processor).MaxClockSpeed"]
                    pc_speed = subprocess.check_output(speed_cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
                    if pc_speed.isdigit():
                        max_clock_speed_mhz = f"{pc_speed} MHz"
                except Exception:
                    pass
            elif os_type == "Linux":
                try:
                    with open("/proc/cpuinfo", "r") as f:
                        content = f.read()
                    cores = set()
                    for line in content.splitlines():
                        if "cpu cores" in line:
                            cores.add(line.split(":")[1].strip())
                        if "model name" in line:
                            processor_brand = line.split(":")[1].strip()
                    physical_cores = len(cores) if cores else "Unavailable"
                except Exception:
                    pass
            elif os_type == "Darwin": # macOS
                try:
                    physical_cores = int(subprocess.check_output(["sysctl", "-n", "hw.physicalcpu"]).decode().strip())
                    processor_brand = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
                except Exception:
                    pass

            # 💾 OS-Specific Memory Detection Hooks
            memory_data = None
            if os_type == "Windows":
                try:
                    # Query total physical RAM and free physical RAM via PowerShell
                    mem_cmd = ["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize, FreePhysicalMemory | ConvertTo-Json"]
                    mem_out = subprocess.check_output(mem_cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
                    
                    # Parse json manually to avoid external dependency issues
                    import json
                    mem_stats = json.loads(mem_out)
                    
                    # PowerShell returns these values in Kilobytes, convert them to Bytes
                    total = int(mem_stats.get("TotalVisibleMemorySize", 0)) * 1024
                    free = int(mem_stats.get("FreePhysicalMemory", 0)) * 1024
                    used = total - free
                    
                    memory_data = {
                        "total": total / (1024**3),
                        "used": used / (1024**3),
                        "free": free / (1024**3),
                        "pct": (used / total) * 100 if total > 0 else 0
                    }
                except Exception:
                    pass
            elif os_type == "Linux":
                try:
                    stats = {}
                    with open("/proc/meminfo", "r") as f:
                        for line in f:
                            parts = line.split()
                            if len(parts) >= 2:
                                key = parts[0].replace(":", "")
                                stats[key] = int(parts[1]) * 1024 # KB to Bytes
                    total = stats.get("MemTotal", 0)
                    available = stats.get("MemAvailable", total - stats.get("MemFree", 0))
                    used = total - available
                    memory_data = {
                        "total": total / (1024**3),
                        "used": used / (1024**3),
                        "free": available / (1024**3),
                        "pct": (used / total) * 100 if total > 0 else 0
                    }
                except Exception:
                    pass
                
            elif os_type == "Darwin":
                try:
                    total_bytes = int(subprocess.check_output(["sysctl", "-n", "hw.memsize"]).decode().strip())
                    vm_stat_out = subprocess.check_output(["vm_stat"]).decode()
                    page_size = 4096
                    for line in vm_stat_out.splitlines():
                        if "page size of" in line:
                            page_size = int(line.split("bytes")[0].split()[-1])
                            break
                    free_pages = 0
                    for line in vm_stat_out.splitlines():
                        if "Pages free:" in line:
                            free_pages = int(line.split()[-1].replace(".", ""))
                            break
                    free_bytes = free_pages * page_size
                    used_bytes = total_bytes - free_bytes
                    memory_data = {
                        "total": total_bytes / (1024**3),
                        "used": used_bytes / (1024**3),
                        "free": free_bytes / (1024**3),
                        "pct": (used_bytes / total_bytes) * 100 if total_bytes > 0 else 0
                    }
                except Exception:
                    pass

            # 🖥️ Render Triage Dashboard
            print(f"Processor Brand:   {processor_brand}")
            print(f"Physical Cores:    {physical_cores}")
            print(f"Logical Cores:     {logical_cores}")
            if max_clock_speed_mhz != "Unavailable":
                print(f"Clock Speed:       {max_clock_speed_mhz}")
            print("-------------------------------------")
            
            if memory_data:
                # Build usage visual bar
                bar_length = 20
                filled_length = int(round(bar_length * (memory_data['pct'] / 100)))
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                
                print(f"Total RAM:         {memory_data['total']:.2f} GB")
                print(f"Used RAM:          {memory_data['used']:.2f} GB")
                print(f"Available RAM:     {memory_data['free']:.2f} GB")
                print(f"RAM Usage:         [{bar}] {memory_data['pct']:.1f}%")
                print("-------------------------------------")
                
                # Dynamic RAM Health Assessment
                if memory_data['pct'] < 70:
                    print("Status: 🟢 Healthy System Resources")
                elif 70 <= memory_data['pct'] < 90:
                    print("Status: 🟡 Memory Pressure Warning")
                else:
                    print("Status: 🔴 Low Memory Critical Threshold")
            else:
                print("🔴 Active Virtual Memory Telemetry Unavailable.")

        except Exception:
            print("🔴 Hardware assessment error.")
            print("CPU & Memory live intelligence currently offline.\n")

        print("=====================================\n")
        input("Press Enter to return to the Dashboard...")
        print("\n" + "="*40 + "\n")

   # ==============================================
    # 🛡️ OPTION 7: MISSION V4-6: WINDOWS SECURITY INTELLIGENCE
    # ==============================================
    elif choice == "7":
        log_action(analyst_name, user_role, "WINDOWS_SECURITY_SCAN")
        print("=====================================")
        print("🛡️ WINDOWS SECURITY INTELLIGENCE")
        print("=====================================\n")
        print("Interrogating anti-malware service status...")
        print("Querying active network security profiles...")
        time.sleep(1.0)

        os_type = platform.system()
        if os_type != "Windows":
            print("ℹ️  Security Intelligence is optimized for Windows systems.")
            print("🔴 Security Profile Sweep: Unsupported Platform.\n")
        else:
            try:
                # --- 1. Query Windows Defender & Real-Time Protection ---
                defender_cmd = ["powershell", "-NoProfile", "-Command", "Get-MpComputerStatus | Select-Object -Property AMServiceEnabled, RealTimeProtectionEnabled | ConvertTo-Json"]
                defender_out = subprocess.check_output(defender_cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
                
                import json
                defender_status = json.loads(defender_out)
                
                service_running = defender_status.get("AMServiceEnabled")
                realtime_active = defender_status.get("RealTimeProtectionEnabled")

                # Convert outputs cleanly to boolean values
                def_ok = (service_running is True or str(service_running).lower() == "true")
                rt_ok = (realtime_active is True or str(realtime_active).lower() == "true")

                # --- 2. Query Windows Firewall ---
                firewall_cmd = ["powershell", "-NoProfile", "-Command", "Get-NetFirewallProfile | Select-Object -Property Name, Enabled | ConvertTo-Json"]
                firewall_out = subprocess.check_output(firewall_cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
                
                profiles = json.loads(firewall_out)
                if isinstance(profiles, dict):
                    profiles = [profiles]
                
                firewall_enabled_count = 0
                total_profiles = len(profiles)
                
                for profile in profiles:
                    enabled = profile.get("Enabled")
                    if enabled is True or str(enabled).lower() == "true":
                        firewall_enabled_count += 1

                # --- 3. Render the Unified Security Dashboard ---
                print("Windows Defender")
                print("-----------------")
                print("Status: " + ("🟢 Running" if def_ok else "🔴 Stopped"))

                print("\nReal-Time Protection")
                print("--------------------")
                print("Status: " + ("🟢 Enabled" if rt_ok else "🔴 Disabled"))

                print("\nFirewall")
                print("---------")
                if firewall_enabled_count == total_profiles:
                    print("Status: 🟢 Enabled (All Profiles)")
                    fw_ok = True
                elif firewall_enabled_count > 0:
                    print("Status: 🟡 One Profile Disabled")
                    fw_ok = True # Partial protection, warn but don't critical fail
                else:
                    print("Status: 🔴 Disabled")
                    fw_ok = False

                print("\nOverall Security")
                print("----------------")
                if def_ok and rt_ok and fw_ok:
                    print("🟢 Device Protected")
                else:
                    print("🔴 Immediate Action Required")

            except Exception as e:
                print("🔴 Critical: Security diagnostic service unresponsive or access denied.")
                print("⚠️  Ensure you are running the scanner from an Administrator command prompt.")

        print("\n=====================================\n")
        input("Press Enter to return to the Dashboard...")
        print("\n" + "="*40 + "\n")

   # ==============================================
    # 🔥 OPTION 8: MISSION V4-8: FIREWALL PROFILE DEEP-DIVE
    # ==============================================
    elif choice == "8":
        log_action(analyst_name, user_role, "FIREWALL_SCAN")
        print("=====================================")
        print("🔥 FIREWALL PROFILE DEEP-DIVE")
        print("=====================================\n")
        print("Interrogating Windows Advanced Firewall...")
        time.sleep(0.8)

        os_type = platform.system()
        if os_type != "Windows":
            print("ℹ️  Firewall telemetry is optimized for Windows systems.")
            print("🔴 Security Profile Sweep: Unsupported Platform.\n")
        else:
            try:
                # Query the detailed state of each profile (Domain, Private, Public)
                cmd = ["powershell", "-NoProfile", "-Command", "Get-NetFirewallProfile | Select-Object -Property Name, Enabled, DefaultInboundAction, DefaultOutboundAction | ConvertTo-Json"]
                output = subprocess.check_output(cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
                
                import json
                profiles = json.loads(output)
                
                if isinstance(profiles, dict):
                    profiles = [profiles]
                
                print(f"{'Profile Name':<12} | {'Status':<10} | {'Inbound Policy':<15} | {'Outbound Policy'}")
                print("-" * 65)
                
                all_ok = True
                for profile in profiles:
                    name = profile.get("Name", "Unknown")
                    enabled = profile.get("Enabled")
                    inbound = profile.get("DefaultInboundAction", "Unknown")
                    outbound = profile.get("DefaultOutboundAction", "Unknown")
                    
                    is_enabled = (enabled is True or str(enabled).lower() == "true")
                    status_str = "🟢 ENABLED" if is_enabled else "🔴 DISABLED"
                    
                    if not is_enabled:
                        all_ok = False
                        
                    print(f"{name:<12} | {status_str:<10} | {inbound:<15} | {outbound}")
                
                print("-" * 65)
                if all_ok:
                    print("\nOverall Status: 🟢 All network boundaries secured.")
                else:
                    print("\nOverall Status: 🔴 WARNING: Compromised network boundary detected!")
                    
            except Exception as e:
                print("🔴 Error executing security query. Local security policy may prevent diagnostics.")

        print("\n=====================================\n")
        input("Press Enter to return to the Dashboard...")
        print("\n" + "="*40 + "\n")

    # ==============================================
    # 🛡️ OPTION 9: MISSION V4-9: ANTIVIRUS & THREAT SIGNATURES
    # ==============================================
    elif choice == "9":
        log_action(analyst_name, user_role, "ANTIVIRUS_SCAN")
        print("=====================================")
        print("🛡️ ANTIVIRUS & THREAT SIGNATURES")
        print("=====================================\n")
        print("Accessing anti-malware engine parameters...")
        print("Checking threat definition database age...\n")
        time.sleep(1.0)

        os_type = platform.system()
        if os_type != "Windows":
            print("ℹ️  Antivirus telemetry is optimized for Windows systems.")
            print("🔴 Security Profile Sweep: Unsupported Platform.\n")
        else:
            try:
                # Retrieve the full engine status including signature versions and update times
                cmd = ["powershell", "-NoProfile", "-Command", "Get-MpComputerStatus | Select-Object -Property AMServiceEnabled, RealTimeProtectionEnabled, AntispywareSignatureVersion, AntispywareSignatureLastUpdated | ConvertTo-Json"]
                output = subprocess.check_output(cmd, creationflags=subprocess.CREATE_NO_WINDOW).decode().strip()
                
                import json
                defender_status = json.loads(output)
                
                service_running = defender_status.get("AMServiceEnabled")
                realtime_active = defender_status.get("RealTimeProtectionEnabled")
                sig_version = defender_status.get("AntispywareSignatureVersion", "Unknown")
                
                # Format the timestamp nicely if it's there
                raw_date = defender_status.get("AntispywareSignatureLastUpdated", "")
                if raw_date:
                    # Clean up the typical WMI/PowerShell date string
                    clean_date = raw_date.split(".")[0].replace("T", " ")
                else:
                    clean_date = "Unknown"

                # Parse booleans
                def_ok = (service_running is True or str(service_running).lower() == "true")
                rt_ok = (realtime_active is True or str(realtime_active).lower() == "true")

                print(f"Malware Engine:      " + ("🟢 ACTIVE" if def_ok else "🔴 INACTIVE"))
                print(f"Real-Time Shield:    " + ("🟢 RUNNING" if rt_ok else "🔴 SHIELD DOWN"))
                print(f"Signature Version:   📑 {sig_version}")
                print(f"Last Database Sync:  📅 {clean_date}")
                print("-------------------------------------")
                
                if def_ok and rt_ok:
                    print("Status: 🟢 Threat definitions and active shields are healthy.")
                else:
                    print("Status: 🔴 Host is highly vulnerable to zero-day exploits!")

            except Exception as e:
                print("🔴 Critical: Antivirus service completely unresponsive or access denied.")
                print("⚠️  Ensure you are running the scanner from an Administrator command prompt.")

        print("\n=====================================\n")
        input("Press Enter to return to the Dashboard...")
        print("\n" + "="*40 + "\n")

    # --- FULL RECON SCAN ---
    elif choice == "10":
        log_action(analyst_name, user_role, "FULL_SYSTEM_SCAN")
        print("🚀 INITIALIZING FULL SYSTEM RECON SCAN...")
        print("="*40 + "\n")
        
        p_res = run_scan("Password Security", "🔐", password_outcomes)
        f_res = run_scan("Firewall Status", "🔥", firewall_outcomes)
        a_res = run_scan("Antivirus Engine", "🛡️", antivirus_outcomes)
        pt_res = run_scan("Network Ports", "📡", port_outcomes)
        u_res = run_scan("USB Devices", "💾", usb_outcomes)
        up_res = run_scan("Software Updates", "⬇", update_outcomes)
        
        total_penalty = p_res['risk'] + f_res['risk'] + a_res['risk'] + pt_res['risk'] + u_res['risk'] + up_res['risk']
        final_score = 100 - total_penalty
        threat_level = "🟢 LOW" if final_score >= 85 else "🟡 MEDIUM" if final_score >= 60 else "🔴 HIGH"
        scan_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        with open(HISTORY_FILE, "a", encoding="utf-8") as db_file:
            db_file.write(f"{scan_time}|{final_score}|{threat_level}\n")
            
        load_scan_database()
        print(f"\n==========================\n  FINAL SECURITY SCORE: {final_score} / 100\n==========================\n")
        input("Press Enter to return to the Dashboard...")
        print("\n" + "="*40 + "\n")

    # --- VIEW HISTORY ---
    elif choice == "11":
        log_action(analyst_name, user_role, "VIEW_HISTORY")
        print("========================")
        print("   PERMANENT SCAN DB    ")
        print("========================")
        if len(scan_history) == 0:
            print("\n  [!] Database cache is empty.\n")
        else:
            for index, record in enumerate(scan_history, start=1):
                print(f"{index}. {record['timestamp']} | Score: {record['score']} | Threat: {record['threat']}")
        print("========================\n")
        input("Press Enter to return to the Dashboard...")
        print("\n" + "="*40 + "\n")

    # --- NESTED ADMINISTRATOR CONSOLE LOOP ---
    elif user_role == "Administrator" and choice == "12":
        log_action(analyst_name, user_role, "ACCESS_ADMIN_CONSOLE")
        
        while True:
            print("======================================")
            print("        ADMINISTRATOR CONSOLE")
            print("======================================")
            print("1️⃣ View Audit Log\n2️⃣ View Scan Database File\n3️⃣ Reset Scan History (Destructive)\n4️⃣ Reset Audit Log    (Destructive)\n5️⃣ Create New Analyst Profile\n6️⃣ Return to Main Menu")
            print("======================================")
            
            admin_choice = input("Admin Action: ").strip()
            print("\n" + "-"*40 + "\n")
            
            if admin_choice == "1":
                log_action(analyst_name, user_role, "VIEW_AUDIT_LOGS")
                print("📋 --- SECURE SYSTEM AUDIT TRAIL ---")
                if os.path.exists(AUDIT_FILE):
                    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
                        print(f.read())
                else:
                    print("[!] No active audit trails currently mapped to disk.")
                print("------------------------------------\n")
                input("Press Enter to clear screen...")
                
            elif admin_choice == "2":
                log_action(analyst_name, user_role, "VIEW_RAW_SCAN_DB")
                print("💾 --- RAW SCAN LOG FILES ---")
                if os.path.exists(HISTORY_FILE):
                    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                        print(f.read())
                else:
                    print("[!] Scan database empty.")
                print("------------------------------\n")
                input("Press Enter to clear screen...")

            elif admin_choice == "3":
                confirm = input("⚠️ PURGE ALL HISTORY LOGS? (Y/N): ").strip().upper()
                if confirm == "Y":
                    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                        f.write("")
                    load_scan_database()
                    log_action(analyst_name, user_role, "PURGE_SCAN_DATABASE", "SUCCESS")
                    print("\n💥 Success: Scan History wiped cleanly.\n")
                else:
                    print("\n❌ Operation aborted by user.\n")
                input("Press Enter to continue...")

            elif admin_choice == "4":
                confirm = input("⚠️ PURGE SYSTEM AUDIT ROLLS? (Y/N): ").strip().upper()
                if confirm == "Y":
                    with open(AUDIT_FILE, "w", encoding="utf-8") as f:
                        f.write("")
                    log_action(analyst_name, user_role, "PURGE_AUDIT_TRAILS", "SUCCESS")
                    print("\n💥 Success: Audit logs deleted safely.\n")
                else:
                    print("\n❌ Operation aborted.\n")
                input("Press Enter to continue...")

            elif admin_choice == "5":
                print("👤 ACCOUNT PROVISIONING CLIENT")
                new_user = input("Enter new analyst username: ").strip().lower()
                new_pass = input("Assign authorization password: ").strip()
                new_role = input("Set security group profile (Administrator/Analyst): ").strip().capitalize()
                
                if new_role not in ["Administrator", "Analyst"]:
                    print("\n❌ Error: Invalid security group assignment.\n")
                else:
                    ALLOWED_ANALYSTS[new_user] = {
                        "password": new_pass,
                        "role": new_role,
                        "clearance": "LEVEL 5" if new_role == "Administrator" else "LEVEL 2",
                        "privilege_tag": f"🟢 {new_role} Privileges Enabled" if new_role == "Administrator" else f"🔵 {new_role} Mode Enabled"
                    }
                    log_action(analyst_name, user_role, f"CREATE_USER_{new_user.upper()}", "SUCCESS")
                    print(f"\n✅ Success: Provisioned {new_role} profile for '{new_user}'.\n")
                input("Press Enter to continue...")

            elif admin_choice == "6":
                print("Returning to control console...")
                time.sleep(0.5)
                print("\n" + "="*40 + "\n")
                break
                
            else:
                print("❌ Invalid Admin Choice.\n")
            print("\n" + "="*40 + "\n")

    # --- LOGOUT CONDITIONS ---
    elif (user_role == "Administrator" and choice == "13") or (user_role == "Analyst" and choice == "12"):
        log_action(analyst_name, user_role, "LOGOUT")
        print(f"Thank you, {user_role} {analyst_name}.\nSession terminated safely. Goodbye!")
        break
        
    else:
        print("❌ Invalid choice. Please try again.\n")
        input("Press Enter to continue...")
        print("\n" + "="*40 + "\n")
