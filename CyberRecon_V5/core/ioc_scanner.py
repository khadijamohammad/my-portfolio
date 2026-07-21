import os
import hashlib
import json

class IOCScanner:
    def __init__(self, db_path="ioc_db.json"):
        self.db_path = db_path
        self.load_database()

    def load_database(self):
        """Loads malicious indicators into runtime state."""
        try:
            with open(self.db_path, "r") as f:
                self.db = json.load(f)
        except Exception:
            self.db = {"malicious_hashes": {}, "suspicious_filenames": [], "suspicious_extensions": []}

    def calculate_sha256(self, file_path):
        """Computes the SHA-256 hash of a file efficiently by reading in chunks."""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except (PermissionError, FileNotFoundError):
            return None

    def scan_directory(self, target_directory):
        """Scans a directory path and yields tracking hits."""
        print(f"\n🔍 [IOC SCAN] Starting evaluation of target path: {target_directory}")
        hits_found = 0

        for root, dirs, files in os.walk(target_directory):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Check 1: Filename Match
                if file.lower() in [f.lower() for f in self.db["suspicious_filenames"]]:
                    print(f"  [!] MATCH: Suspicious Filename detected -> {file_path}")
                    hits_found += 1
                
                # Check 2: Hash Check for Binary Assets
                if any(file.endswith(ext) for ext in self.db["suspicious_extensions"]):
                    file_hash = self.calculate_sha256(file_path)
                    if file_hash in self.db["malicious_hashes"]:
                        malware_type = self.db["malicious_hashes"][file_hash]
                        print(f"  [🚨] ALARM: Known Malicious Hash ({malware_type}) matched at -> {file_path}")
                        hits_found += 1
                        
        print(f"🏁 [IOC SCAN] Routine finished. Total hits triggered: {hits_found}\n")
        return hits_found

if __name__ == "__main__":
    # Test execution against your current working space
    scanner = IOCScanner()
    scanner.scan_directory(".")