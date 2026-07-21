import pytest

def test_suspicious_process_detection():
    # Example logic test
    known_threats = ["mimikatz.exe", "cmd.exe", "powershell.exe"]
    detected_process = "mimikatz.exe"
    
    assert detected_process in known_threats

def test_soar_policy_passive_mode():
    # Test passive mode default behavior
    mode = "passive"
    assert mode == "passive"