import re

def check_password(password):
    # Rule validation using regular expressions
    if len(password) < 8:
        return False, "Too short! Must be at least 8 characters."
    if not any(c.isupper() for c in password):
        return False, "Missing an uppercase letter!"
    if not any(c.isdigit() for c in password):
        return False, "Missing a number!"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_+-=~`[\]\\]", password):
        return False, "Missing a special character!"
    
    return True, "Access Granted."

def cyber_escape_challenge():
    print("=========================================")
    print("🔒 SYSTEM LOCKED: ENTER THE DECRYPTION CODE")
    print("=========================================")
    print("Rules:")
    print(" - Minimum 8 characters")
    print(" - At least 1 uppercase letter")
    print(" - At least 1 lowercase letter")
    print(" - At least 1 number")
    print(" - At least 1 special character")
    print("🚨 WARNING: You only have 3 attempts before lockout.\n")

    attempts = 3

    while attempts > 0:
        guess = input(f"Enter Code [{attempts} attempts remaining]: ")
        
        is_valid, message = check_password(guess)
        
        if is_valid:
            print("\n🔓 ACCESS GRANTED. Welcome back, Agent.")
            print("The escape pod coordinates have been downloaded. RUN!")
            return
        else:
            attempts -= 1
            print(f"❌ ACCESS DENIED: {message}")
            if attempts > 0:
                print("Try again...\n")
            
    print("\n🚨 SYSTEM LOCKOUT ACTIVATED 🚨")
    print("Access blocked for 10 seconds...")
    print("Alarms are sounding. The mainframe has melted down. Game Over.")

# Run the challenge
if __name__ == "__main__":
    cyber_escape_challenge()