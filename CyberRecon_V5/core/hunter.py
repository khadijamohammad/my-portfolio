def trace_process_lineage(target_pid, pid_history_db):
    """
    Given a PID, builds a linear execution path from the initial root process
    Example: explorer.exe -> cmd.exe -> powershell.exe
    """
    lineage = []
    current_pid = target_pid
    
    # Traverse backwards up the execution tree using tracking maps
    while current_pid in pid_history_db and len(lineage) < 10:
        proc_node = pid_history_db[current_pid] # Contains name, pid, ppid
        lineage.insert(0, f"{proc_node['name']} ({current_pid})")
        current_pid = proc_node["ppid"]
        
    return " -> ".join(lineage)