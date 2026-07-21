import psutil

class TelemetryCollector:
    def __init__(self):
        self.known_pids = set(psutil.pids())

    def get_new_processes(self):
        """Returns structural data for newly spawned system tasks."""
        current_pids = set(psutil.pids())
        new_pids = current_pids - self.known_pids
        self.known_pids = current_pids
        
        events = []
        for pid in new_pids:
            try:
                proc = psutil.Process(pid)
                events.append({
                    "pid": pid,
                    "ppid": proc.ppid(),
                    "process_name": proc.name().lower()
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return events