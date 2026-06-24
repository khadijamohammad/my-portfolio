import getpass
username = "Khadija"
password = "Secure123!"

attempts = 3

print("================================")
print("🔐 SECURE LOGIN SYSTEM")
print("================================")

while attempts > 0:

    user = input("Username: ")
    user_password = getpass.getpass("Password: ")

    if user == username and user_password == password:
        print("\n✅ Access Granted")
        print(f"Welcome back, {user}!")

        print("Login time recorded.")
        print("Security Level: HIGH 🔐")

        with open("login_history.txt", "a") as file:
            file.write(f"{user} logged in\n")

        
     
        break

    else:
        attempts -= 1

        print("\n❌ Wrong username or password")

        if attempts > 0:
            print(f"Attempts left: {attempts}")

if attempts == 0:
    print("\n🚨 ACCOUNT LOCKED")
    print("Access blocked for 10 seconds...")