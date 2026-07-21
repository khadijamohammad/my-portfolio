import sys
import time
import logging

# Configure logging format and level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("cyberrecon.log"),
        logging.StreamHandler()
    ]
)

# Example usage in your detection engine:
logging.info("CyberRecon scanner initialized successfully.")
logging.warning("Suspicious process spawn detected: PID 4120 (powershell.exe)")
logging.error("Failed to parse rule file: config/rules.json")

class Colors:
    """ANSI color codes for Windows Terminal formatting."""
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def show_progress(label, steps=20, delay=0.04):
    """Renders a fluid, commercial-grade terminal progress bar."""
    print(f"{Colors.CYAN}{label}{Colors.RESET}")
    for i in range(steps + 1):
        pct = int((i / steps) * 100)
        filled = "█" * i
        empty = "░" * (steps - i)
        
        # Color transitions dynamically based on progress percent
        color = Colors.RED if pct < 40 else Colors.YELLOW if pct < 80 else Colors.GREEN
        
        sys.stdout.write(f"\r[{color}{filled}{empty}{Colors.RESET}] {pct}%")
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")