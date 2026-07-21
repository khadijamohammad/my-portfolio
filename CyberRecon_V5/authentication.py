import time
from CyberRecon_V5.core.utils import Colors

class AuthenticationSystem:
    """Manages role-based authorization, analyst credentials, and access locks."""
    def __init__(self):
        # Database of authorized users: (Password, Role)
        self.user_db = {
            "khadija": ("superadmin123", "Lead Security Engineer"),
            "analyst": ("secops2026", "Security Analyst"),
            "guest": ("guest", "Guest Observer")
        }

    def authenticate_user(self):
        """Standard login logic with security role identification."""
        print(f"{Colors.BOLD}====================================={Colors.RESET}")
        print(f"🔒  {Colors.BLUE}CYBER RECON SYSTEM v5.0 - SECURITY RECON{Colors.RESET}")
        print(f"{Colors.BOLD}====================================={Colors.RESET}\n")

        attempts = 3
        while attempts > 0:
            username = input("Analyst Username: ").strip().lower()
            password = input("Access Key/Password: ").strip()

            if username in self.user_db and self.user_db[username][0] == password:
                role = self.user_db[username][1]
                print(f"\n{Colors.GREEN}🟢 Authentication Successful.{Colors.RESET}")
                print(f"Welcome back, {Colors.BOLD}{username.capitalize()}{Colors.RESET} [{Colors.YELLOW}{role}{Colors.RESET}]\n")
                time.sleep(0.8)
                return username, role
            else:
                attempts -= 1
                print(f"\n{Colors.RED}❌ Access Denied. Invalid credentials. ({attempts} attempts remaining){Colors.RESET}\n")
        
        print(f"{Colors.RED}🚨 CRITICAL: Intrusion Prevention Lockout Activated.{Colors.RESET}")
        print("Closing diagnostic channels...")
        time.sleep(1.5)
        return None, None