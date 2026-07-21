import platform
import psutil
import datetime

def generate_forensic_bundle(trigger_event, rule_metadata):
    """Triggered instantly on critical alerts to snapshot volatile artifact data."""
    pid = trigger_event.get("pid")
    
    bundle = {
        "incident_id": f"CR-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "alert_context": {
            "rule_id": rule_metadata.get("id"),
            "severity": rule_metadata.get("severity"),
            "mitre_mapping": rule_metadata.get("mitre")
        },
        "host_telemetry": {
            "hostname": platform.node(),
            "os": platform.system(),
            "os_release": platform.release()
        },
        "volatile_evidence": {
            "target_process": trigger_event,
            "network_connections": [],
            "loaded_modules": []
        }
    }
    
    # Actively query the local host system for additional context before it vanishes
    try:
        proc = psutil.Process(pid)
        bundle["volatile_evidence"]["loaded_modules"] = [x.path for x in proc.memory_maps()]
        bundle["volatile_evidence"]["network_connections"] = [x._asdict() for x in proc.connections()]
    except Exception as e:
        bundle["volatile_evidence"]["error"] = f"Failed to acquire volatile process internals: {e}"
        
    return bundle