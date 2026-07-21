import os
import glob
import json
import asyncio

class BehavioralDetectionEngine:
    def __init__(self, rules_dir=None):
        # Dynamically find the absolute path of the directory containing this file (core/)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        if rules_dir is None:
            self.rules_dir = os.path.abspath(os.path.join(base_dir, "rules"))
        else:
            self.rules_dir = rules_dir
            
        self.rules = []
        self.pid_map = {}
        
        # Track file modification times for the hot-reloader
        self.rules_snapshot = {}
        
        # Initial rules load
        self.load_rules()

    def load_rules(self):
        """Recursively discovers, validates, and loads JSON rules across ATT&CK tactic directories."""
        current_rules = []
        new_snapshot = {}
        
        # 🎯 Enterprise Upgrade: Scan recursively (**/*.json) to allow tactic subfolders
        search_path = os.path.join(self.rules_dir, "**", "*.json")
        
        for rule_file in glob.glob(search_path, recursive=True):
            try:
                mtime = os.path.getmtime(rule_file)
                new_snapshot[rule_file] = mtime
                
                with open(rule_file, 'r', encoding='utf-8') as f:
                    rule_data = json.load(f)
                    
                    if not rule_data.get("enabled", True):
                        continue
                        
                    current_rules.append(rule_data)
            except Exception as e:
                print(f"[!] Error loading rule file {rule_file}: {e}")
        
        if new_snapshot != self.rules_snapshot:
            self.rules = current_rules
            self.rules_snapshot = new_snapshot
            print(f"\n--- 🔄 ENTERPRISE SIGNATURE PIPELINE REFRESHED ---")
            print(f"[*] Total Active Signatures: {len(self.rules)}\n")

    async def start_hot_reloader(self, interval_seconds=2):
        """Asynchronous background loop that watches the rules directory for changes."""
        print("[*] Rule Hot-Reloader background process activated.")
        while True:
            try:
                # Check for updates natively without interrupting telemetry processing
                self.load_rules()
            except Exception as e:
                print(f"[!] Hot-reloader error: {e}")
            await asyncio.sleep(interval_seconds)

    def analyze(self, process_event):
        """Evaluates live telemetry against loaded v6.2 metadata rules framework."""
        pid = process_event["pid"]
        ppid = process_event["ppid"]
        name = process_event.get("process_name", "").lower()
        cmdline = process_event.get("commandline", "").lower()
        
        self.pid_map[pid] = name
        parent_name = str(self.pid_map.get(ppid, "unknown")).lower()

        for rule in self.rules:
            conditions = rule.get("conditions", {})
            target_parent = conditions.get("parent_name", "").lower()
            target_proc = conditions.get("process_name", "").lower()
            target_contains = conditions.get("commandline_contains", "").lower()
            
            # Match Parent and Process
            match = (parent_name == target_parent and name == target_proc)
            
            # v6.2 Feature: Check command line arguments if specified in rule conditions
            if match and target_contains:
                if target_contains not in cmdline:
                    match = False
            
            if match:
                return {
                    "alert_triggered": True,
                    "title": rule.get("title"),
                    "mitre": rule.get("mitre"),
                    "severity": rule.get("severity"),
                    "confidence": rule.get("confidence"),
                    "parent": parent_name,
                    "child": name,
                    "pid": pid,
                    "ppid": ppid,
                    "rule_id": rule.get("id"),
                    "response_actions": rule.get("response", {})
                }
                
        return {"alert_triggered": False}