import os
import json

class IOCIntelligenceEngine:
    def __init__(self):
        # High-performance lookup tables for direct targeting
        self.hash_watchlists = {}     # MD5 or SHA256 -> Threat Intel Metadata
        self.network_watchlists = {}  # IP addresses or Domains -> Threat Intel Metadata
        
    def load_intel_feed(self, feed_data: list):
        """
        Populates the engine watchlists from internal databases or Threat Intel providers.
        Expects a list of dictionaries containing threat intelligence.
        """
        for item in feed_data:
            indicator = item.get("indicator", "").strip().lower()
            if not indicator:
                continue
                
            # Direct routing based on typical indicator characteristics
            if len(indicator) in [32, 64] and not "." in indicator:
                self.hash_watchlists[indicator] = item
            else:
                self.network_watchlists[indicator] = item
                
        print(f"[*] IOC Engine loaded: {len(self.hash_watchlists)} hashes, {len(self.network_watchlists)} network markers.")

    def inspect_telemetry(self, event: dict) -> dict:
        """
        Scans inbound execution or network events against fast-lookup databases.
        """
        # 1. Inspect Process File Hashes (SHA256 / MD5)
        file_hash = event.get("sha256", event.get("md5", "")).lower().strip()
        if file_hash in self.hash_watchlists:
            return self.generate_ioc_alert(self.hash_watchlists[file_hash])
            
        # 2. Inspect Target Network Connections
        dest_ip = event.get("destination_ip", "").lower().strip()
        if dest_ip in self.network_watchlists:
            return self.generate_ioc_alert(self.network_watchlists[dest_ip])
            
        dest_domain = event.get("domain", "").lower().strip()
        if dest_domain in self.network_watchlists:
            return self.generate_ioc_alert(self.network_watchlists[dest_domain])
            
        return {"matched": False}

    def generate_ioc_alert(self, intel: dict) -> dict:
        """
        Formats matches into a clean structured response for your server dashboard.
        """
        return {
            "matched": True,
            "type": "IOC MATCH",
            "indicator": intel.get("indicator"),
            "threat_family": intel.get("family", "Unknown Threat"),
            "confidence": f"{intel.get('confidence', 80)}%",
            "recommendation": intel.get("remediation", "Isolate host and investigate immediately.")
        }