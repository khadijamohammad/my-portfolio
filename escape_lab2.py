import time
play_again = "yes"
print("================================")
print("🧪 ESCAPE THE LAB 2")
print("================================")

name = input("Enter your name: ")

print(f"\nWelcome {name}.")
print("You wake up inside a locked cyber lab.")

# Game tracking variables
has_usb = False
has_key_code = False  # Tracks if they found the password text
usb_unlocked = False  # Tracks if they successfully decrypted the USB
computer_attempts = 3
door_attempts = 2
window_attempts = 1

# Main game loop
while play_again == "yes":
    choice = input("\nChoose where to look [door / computer / window / search room]: ").lower()

    # --- SEARCH ROOM PATH ---
    if choice == "search room":
        if not has_usb:
            print("\n🔍 You rummage through a desk drawer and find a USB drive!")
            print("⚠️ The USB is heavily encrypted. A red warning light flashes on it. You pocket it.")
            has_usb = True
        elif has_usb and not has_key_code:
            print("\n🔍 You continue searching the room...")
            print("📄 Hidden behind a server rack, you find a scrap of paper with a handwritten note:")
            print("   'Bypass key for drive encryption: CYBER2026'")
            has_key_code = True
        else:
            print("\nYou already searched the room thoroughly. There's nothing else useful here.")

    # --- COMPUTER PATH ---
    elif choice == "computer":
        if not has_usb:
            print("\n❌ NO USB DETECTED. The screen reads: 'Insert authorized hardware token to proceed.'")
            print("You need to find a USB drive first!")

        elif has_usb and not usb_unlocked:
            print("\n💻 You plug in the USB. The screen flashes: 'DEVICE ENCRYPTED.'")
            print("Enter the hardware decryption bypass code to unlock the drive.")

            if not has_key_code:
                print("\n🚫 ACCESS BLOCKED")
                print("The terminal refuses manual input.")
                print("💡 Search the room for the official bypass key.")
            else:
                user_key = input("Enter USB Decryption Code: ")
                if user_key == "CYBER2026":
                    print("\n🔐 Code Accepted! Initializing decryption protocol...")
                    for percent in [10, 25, 60, 100]:
                        print(f"█ {percent}%")
                        time.sleep(0.5)
                    print("\n🔓 USB successfully unlocked!")
                    usb_unlocked = True
                else:
                    print("\n❌ INVALID DECRYPTION CODE. Access to the USB drive is denied.")

        elif has_usb and usb_unlocked:
            print("\n💻 ACCESS GRANTED! The unlocked USB initializes the terminal.")
            time.sleep(1)
            print("\n✅ System Ready")

            # Sub-loop for the computer's 3 attempts
            while computer_attempts > 0:
                print(f"[Attempts remaining: {computer_attempts}]")
                print("The screen glows: 'SYSTEM LOCKED. Enter the 4-digit decryption code to override the main locks.'")
                print("Hint: It's the year the first computer virus 'Creeper' was created (1971).")

                code = input("Enter decryption code: ")
                if code == "1971":
                    print("\nSUCCESS! The computer overrides the facility locks. The main doors hiss open. You escape!")
                    play_again = input("\n🔁 Play again? [yes / no]: ").lower()
                    if play_again != "yes":
                        print("\n🧪 Thanks for playing Escape The Lab!")
                        exit()
                    else:
                        # Reset all variables for a new game
                        has_usb = False
                        has_key_code = False
                        usb_unlocked = False
                        computer_attempts = 3
                        door_attempts = 2
                        window_attempts = 1
                        break
                else:
                    computer_attempts -= 1
                    if computer_attempts > 0:
                        print("\n❌ WRONG CODE! The firewall blocked the attempt. Try again.\n")
                    else:
                        print("\n🚨 WRONG CODE! 0 attempts left. An alarm blares and lockdown gas fills the room. Game Over.")
                        play_again = input("\n🔁 Play again? [yes / no]: ").lower()
                        if play_again != "yes":
                            print("\n🧪 Thanks for playing Escape The Lab!")
                            exit()
                        has_usb = False
                        has_key_code = False
                        usb_unlocked = False
                        computer_attempts = 3
                        door_attempts = 2
                        window_attempts = 1
                        break

    # --- DOOR PATH ---
    elif choice == "door":
        while door_attempts > 0:
            print(f"\n[Attempts remaining: {door_attempts}]")
            print("The heavy steel door has a keypad. A sticky note reads:")
            print("'Password must contain: Uppercase, Lowercase, Special Character, and a Digit.'")
            print("Available options on the note: [ Admin123! / password / 12345 ]")

            password = input("Enter the correct password option: ")
            if password == "Admin123!":
                print("\n*Click* The heavy steel door swings open. You run down the hallway to freedom!")
                play_again = input("\n🔁 Play again? [yes / no]: ").lower()
                if play_again != "yes":
                    print("\n🧪 Thanks for playing Escape The Lab!")
                    exit()
                else:
                    has_usb = False
                    has_key_code = False
                    usb_unlocked = False
                    computer_attempts = 3
                    door_attempts = 2
                    window_attempts = 1
                    break
            else:
                door_attempts -= 1
                if door_attempts > 0:
                    print("\n❌ INVALID PASSWORD! The keypad beeps aggressively. Try again.")
                else:
                    print("\n⚡ INVALID PASSWORD! 0 attempts left. The keypad electrocutes you for tampering. Game Over.")
                    play_again = input("\n🔁 Play again? [yes / no]: ").lower()
                    if play_again != "yes":
                        print("\n🧪 Thanks for playing Escape The Lab!")
                        exit()
                    has_usb = False
                    has_key_code = False
                    usb_unlocked = False
                    computer_attempts = 3
                    door_attempts = 2
                    window_attempts = 1
                    break

    # --- WINDOW PATH ---
    elif choice == "window":
        print(f"\n[Attempts remaining: {window_attempts}]")
        print("The window is reinforced glass, but there is a Secure Login System terminal next to it.")
        print("It asks a security question: 'What protocol secures website traffic? [HTTP / HTTPS]'")

        protocol = input("Your answer: ").upper()
        if protocol == "HTTPS":
            print("\nCorrect! The secure login bypasses the window's electronic shutters. They slide open, letting you escape!")
            play_again = input("\n🔁 Play again? [yes / no]: ").lower()
            if play_again != "yes":
                print("\n🧪 Thanks for playing Escape The Lab!")
                exit()
            else:
                has_usb = False
                has_key_code = False
                usb_unlocked = False
                computer_attempts = 3
                door_attempts = 2
                window_attempts = 1
        else:
            print("\n💥 Incorrect. The terminal flags you as an intruder and locks down permanently. You are trapped. Game Over.")
            play_again = input("\n🔁 Play again? [yes / no]: ").lower()
            if play_again != "yes":
                print("\n🧪 Thanks for playing Escape The Lab!")
                exit()
            has_usb = False
            has_key_code = False
            usb_unlocked = False
            computer_attempts = 3
            door_attempts = 2
            window_attempts = 1

    # --- INVALID CHOICE ---
    else:
        print(f"\nInvalid choice. The lab is ticking down, try looking somewhere real!")