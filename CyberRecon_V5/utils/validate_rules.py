import os
import json
import glob

REQUIRED_FIELDS = ["id", "title", "author", "version", "severity", "confidence", "mitre", "conditions"]

def validate_pipeline(rules_directory):
    errors = 0
    search_path = os.path.join(rules_directory, "**", "*.json")
    
    print("[*] Starting automated rule validation checks...")
    for rule_file in glob.glob(search_path, recursive=True):
        try:
            with open(rule_file, 'r') as f:
                data = json.load(f)
            
            missing = [field for field in REQUIRED_FIELDS if field not in data]
            if missing:
                print(f"[❌] {os.path.basename(rule_file)}: Missing fields {missing}")
                errors += 1
                
            # Validate MITRE format
            if "mitre" in data and not isinstance(data["mitre"], list):
                print(f"[❌] {os.path.basename(rule_file)}: 'mitre' field must be an array.")
                errors += 1
                
        except json.JSONDecodeError:
            print(f"[❌] {os.path.basename(rule_file)}: Invalid JSON Syntax.")
            errors += 1
            
    print(f"\n[+] Validation Complete. Errors found: {errors}")
    return errors == 0