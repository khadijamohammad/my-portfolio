import sys
import time
import os
import platform
from CyberRecon_V5.core.utils import Colors, show_progress
from authentication import AuthenticationSystem
from reports import ReportGenerator

# Import our custom object-oriented scanner modules
from CyberRecon_V5.core.windows_security import WindowsSecurityScanner
from CyberRecon_V5.core.firewall import FirewallScanner
from CyberRecon_V5.core.antivirus import AntivirusScanner
from CyberRecon_V5.core.network import NetworkScanner
from CyberRecon_V5.core.hardware import HardwareScanner
# Import our threat intelligence engine
from CyberRecon_V5.core.threat_intel import ThreatIntelEngine
from CyberRecon_V5.core.incident_engine import IncidentCorrelationEngine
from edr_monitor import EDRMonitor

def clear_screen():
    """Cleans up terminal view depending on Operating System."""
    os.system("cls" if platform.system() == "Windows" else "clear")

def run_targeted_scan(scanner_instance, analyst_name, reporter):
    """Orchestrates running an individual modular security scan."""
    clear_screen()
    print(f"{Colors.BOLD}====================================={Colors.RESET}")
    print(f"📡  RUNNING TARGETED SECURITY SCAN")
    print(f"{Colors.BOLD}====================================={Colors.RESET}\n")
    
    # Run the live scanner checks
    scanner_instance.run()
    results = scanner_instance.get_results()
    
    # Calculate localized scores
    score = max(0, 100 - results["penalty"])
    threat_level = "🟢 LOW" if score >= 85 else "🟡 MEDIUM" if score >= 65 else "🔴 HIGH"
    
    print("\n" + "-" * 40)
    print(f"Scan Scope:   {Colors.BOLD}{results['scanner']}{Colors.RESET}")
    print(f"Score:        {Colors.BOLD}{score}/100{Colors.RESET}")
    print(f"Threat Level: {threat_level}")
    
    # Write findings to the JSON Database
    reporter.save_report(
        analyst=analyst_name,
        score=score,
        threat_level=threat_level,
        findings=results["findings"]
    )
    
    print("-" * 40 + "\n")
    input("Press Enter to return to the Dashboard...")

def run_full_scan(analyst_name, reporter):
    """Runs all security scanning modules, generating a risk matrix and actionable remediation plan."""
    clear_screen()
    print(f"{Colors.BOLD}====================================={Colors.RESET}")
    print(f"🚀  RUNNING FULL RECON SECURITY SCAN")
    print(f"{Colors.BOLD}====================================={Colors.RESET}\n")
    
    scanners = [
        WindowsSecurityScanner(),
        FirewallScanner(),
        AntivirusScanner(),
        NetworkScanner(),
        HardwareScanner()
    ]
    
    results_list = []
    total_penalty = 0
    all_findings = []
    
    # 1. Run Scans
    for scanner in scanners:
        scanner.run()
        res = scanner.get_results()
        results_list.append(res)
        total_penalty += res["penalty"]
        all_findings.extend(res["findings"])
        print("\n" + "=" * 50 + "\n")
        time.sleep(0.4)
        
    final_score = max(0, 100 - total_penalty)
    threat_level = "🟢 LOW" if final_score >= 85 else "🟡 MEDIUM" if final_score >= 60 else "🔴 HIGH"
    
    # 2. Render Risk Matrix
    print(f"\n{Colors.BOLD}RISK MATRIX{Colors.RESET}")
    print("=======================================")
    print(f"{'Category':<24} | {'Status':<10}")
    print("-" * 39)
    for res in results_list:
        category = res["category"]
        penalty = res["penalty"]
        status = f"{Colors.GREEN}🟢 PASS{Colors.RESET}" if penalty == 0 else f"{Colors.RED}🔴 FAIL{Colors.RESET}"
        print(f"{category:<24} | {status:<10}")
    print("=======================================\n")

    # 3. Render Scoring Breakdown
    print(f"{Colors.BOLD}SECURITY SCORE BREAKDOWN{Colors.RESET}")
    print("-" * 39)
    for res in results_list:
        category = res["category"]
        penalty = res["penalty"]
        print(f"{category:<28} ... +{penalty}")
    print("-" * 39)
    print(f"Total Risk Deductions:       ... +{total_penalty}")
    print(f"{Colors.BOLD}Final Score:                 ... {final_score}/100{Colors.RESET}")
    print("-" * 39 + "\n")

    # 4. Generate Remediation Plan Dynamically
    remediations = []
    
    # Analyze findings to generate tailored remediation steps
    for res in results_list:
        cat = res["category"]
        findings = res["findings"]
        
        if cat == "Firewall" and res["penalty"] > 0:
            remediations.append({
                "priority": "Priority 1 (Critical)",
                "issue": "Active network boundaries are open (Firewall profiles disabled).",
                "action": "Enable Domain, Private, and Public Firewall profiles.",
                "remediation": "Set-NetFirewallProfile -Profile Domain,Private,Public -Enabled True",
                "recovery": res["penalty"]
            })
            
        if cat == "Defender" and res["penalty"] > 0:
            remediations.append({
                "priority": "Priority 1 (Critical)",
                "issue": "Windows Defender or Real-Time shields are deactivated.",
                "action": "Start the Anti-Malware Service and enable Real-Time scanning.",
                "remediation": "Set-MpPreference -DisableRealtimeMonitoring $false",
                "recovery": res["penalty"]
            })

        if cat == "Hardware" and "storage" in "".join(findings).lower():
            remediations.append({
                "priority": "Priority 2 (High)",
                "issue": "Primary storage space is severely depleted (Under 10% free).",
                "action": "Trigger disk cleanup or expand disk space.",
                "remediation": "Cleanmgr.exe /sagerun:1  (Or run manual user directory audits)",
                "recovery": res["penalty"]
            })

    if remediations:
        print(f"{Colors.BOLD}REMEDIATION PLAN{Colors.RESET}")
        print("=======================================")
        for plan in remediations:
            print(f"\n⚡ {Colors.BOLD}{plan['priority']}{Colors.RESET}")
            print(f"  • Issue:      {Colors.RED}{plan['issue']}{Colors.RESET}")
            print(f"  • Directive:  {plan['action']}")
            print(f"  • PowerShell Execution Command:")
            print(f"    {Colors.CYAN}{plan['remediation']}{Colors.RESET}")
            print(f"  • Potential Recovery: {Colors.GREEN}+{plan['recovery']} Points{Colors.RESET}")
            print("-" * 39)
    else:
        print(f"{Colors.GREEN}🟢 Overall status is nominal. No urgent remediations required.{Colors.RESET}")

    # 5. Save report to modern JSON DB
    reporter.save_report(
        analyst=analyst_name,
        score=final_score,
        threat_level=threat_level,
        findings=all_findings
    )

    print("\n=======================================\n")

def main():
    """Main execution point: Handles login authentication and menu navigation."""
    auth = AuthenticationSystem()
    reporter = ReportGenerator()
    intel = ThreatIntelEngine()
    soc_engine = IncidentCorrelationEngine()
    edr = EDRMonitor() # Instantiate the continuous monitoring sensor
    
    clear_screen()
    print(f"{Colors.BOLD}====================================={Colors.RESET}")
    print(f"🔒  CYBER RECON SYSTEM v5.0 - LOGIN")
    print(f"{Colors.BOLD}====================================={Colors.RESET}\n")
    
    # Run login validation
    login_result = auth.authenticate_user()
    if not login_result:
        print(f"{Colors.RED}Access Denied. Exiting security environment.{Colors.RESET}")
        return
        
    if isinstance(login_result, tuple):
        analyst_name = login_result[0]
    else:
        analyst_name = login_result
        
    # Open Enterprise Dashboard Interface
    while True:
        clear_screen()
        print(f"{Colors.BOLD}====================================={Colors.RESET}")
        print(f"🛡️  CYBER RECON v5.0 - ENTERPRISE EDR")
        print(f"Active Security Analyst: {Colors.GREEN}{analyst_name}{Colors.RESET}")
        print(f"{Colors.BOLD}====================================={Colors.RESET}\n")
        print("1. 🚀 Run Full Security Recon Scan")
        print("2. 📡 Run Targeted Module Scan")
        print("3. 🕵️  Threat Intelligence Hunt")
        print("4. 🚨 SOC Incident Center")
        print("5. 👁️  LIVE EDR TELEMETRY MONITOR")
        print("6. 📊 View System Scan Reports")
        print("7. ⚙️  Console Settings")
        print("8. ❌ Exit System")
        print("\n" + "=====================================")
        
        choice = input("Select an option (1-8): ").strip()
        
        if choice == "1":
            try:
                run_full_scan(analyst_name, reporter)
                print(f"\n{Colors.BOLD}====================================={Colors.RESET}")
                input("Scan complete! Press Enter to return to the Dashboard...")
            except Exception as e:
                print(f"\n{Colors.RED}⚠️ An error occurred during the scan:{Colors.RESET}")
                print(e)
                input("\nPress Enter to return to Dashboard...")
                
        elif choice == "2":
            clear_screen()
            print(f"{Colors.BOLD}SELECT TARGET MODULE SCANNER{Colors.RESET}")
            print("=====================================")
            print("1. Windows Security Shield")
            print("2. Network Boundary Firewall")
            print("3. Real-Time Antivirus Protection")
            print("4. Network Port/IP Status")
            print("5. Storage & Hardware Diagnostics")
            print("6. Cancel and Return to Dashboard")
            print("=====================================")
            
            sub_choice = input("\nEnter module selection (1-6): ").strip()
            try:
                if sub_choice == "1":
                    run_targeted_scan(WindowsSecurityScanner(), analyst_name, reporter)
                elif sub_choice == "2":
                    run_targeted_scan(FirewallScanner(), analyst_name, reporter)
                elif sub_choice == "3":
                    run_targeted_scan(AntivirusScanner(), analyst_name, reporter)
                elif sub_choice == "4":
                    run_targeted_scan(NetworkScanner(), analyst_name, reporter)
                elif sub_choice == "5":
                    run_targeted_scan(HardwareScanner(), analyst_name, reporter)
            except Exception as e:
                print(f"\n{Colors.RED}⚠️ An error occurred during the targeted scan:{Colors.RESET}")
                print(e)
                input("\nPress Enter to return to Dashboard...")
                
        elif choice == "3":
            while True:
                clear_screen()
                print(f"{Colors.BOLD}====================================={Colors.RESET}")
                print(f"🕵️  THREAT INTELLIGENCE HUNT ENGINE")
                print(f"{Colors.BOLD}====================================={Colors.RESET}\n")
                print("1. 👾 Malware Process Hunt")
                print("2. 🕳️  Suspicious Network Ports")
                print("3. 📌 Startup Persistence Scan")
                print("4. ⚙️  Running Services Audit")
                print("5. ⏰ Scheduled Tasks Scan")
                print("6. ↩️  Return to Main Dashboard")
                print("\n=====================================")
                
                intel_choice = input("Select hunt module (1-6): ").strip()
                if intel_choice == "1":
                    intel.malware_process_hunt()
                    input("\nHunt complete. Press Enter to return to Threat Intel Menu...")
                elif intel_choice == "2":
                    intel.suspicious_ports_scan()
                    input("\nHunt complete. Press Enter to return to Threat Intel Menu...")
                elif intel_choice == "3":
                    intel.startup_persistence_scan()
                    input("\nHunt complete. Press Enter to return to Threat Intel Menu...")
                elif intel_choice == "4":
                    intel.running_services_scan()
                    input("\nHunt complete. Press Enter to return to Threat Intel Menu...")
                elif intel_choice == "5":
                    intel.scheduled_tasks_scan()
                    input("\nHunt complete. Press Enter to return to Threat Intel Menu...")
                elif intel_choice == "6":
                    break
                    
        elif choice == "4":
            while True:
                clear_screen()
                print(f"{Colors.BOLD}====================================={Colors.RESET}")
                print(f"🚨  SOC INCIDENT CENTER")
                print(f"{Colors.BOLD}====================================={Colors.RESET}\n")
                print("1. 🧠 Run Real-Time Incident Correlation")
                print("2. 📁 View Incident Database Archives")
                print("3. 🔧 Resolve & Remediate Active Incident")
                print("4. ↩️  Return to Main Dashboard")
                print("\n=====================================")
                
                soc_choice = input("Select an option (1-4): ").strip()
                if soc_choice == "1":
                    soc_engine.run_correlation(analyst_name)
                    input("\nEngine complete. Press Enter to return to SOC Center...")
                elif soc_choice == "2":
                    soc_engine.view_incident_history()
                    input("\nPress Enter to return to SOC Center...")
                elif soc_choice == "3":
                    soc_engine.resolve_incident(analyst_name)
                    input("\nPress Enter to return to SOC Center...")
                elif soc_choice == "4":
                    break
                    
        elif choice == "5":
            # --- LAUNCH CONTINUOUS LIVE MONITORING ---
            edr.start_detection_loop()
            input("\nPress Enter to head back to the Enterprise Dashboard...")
            
        elif choice == "6":
            input("\nReports engine legacy dashboard coming soon! Press Enter to return to Dashboard...")
        elif choice == "7":
            input("\nSettings configurations coming soon! Press Enter to return to Dashboard...")
        elif choice == "8":
            print(f"\n{Colors.GREEN}Secure sessions terminated. Safe hacking, Analyst!{Colors.RESET}\n")
            break
        else:
            input("\nInvalid option! Press Enter to refresh dashboard...")
# This is the "on-switch" that fires up the program when you run 'python main.py'
if __name__ == "__main__":
    main()