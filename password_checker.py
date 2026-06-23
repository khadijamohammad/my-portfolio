password = input("Enter a password: ")

score = 0

if len(password) >= 8:
    score += 1

if any(char.isupper() for char in password):
    score += 1

if any(char.islower() for char in password):
    score += 1

if any(char.isdigit() for char in password):
    score += 1

if any(not char.isalnum() for char in password):
    score += 1


print("\nResult:")

if score <= 2:
    print("Weak Password")

elif score == 3 or score == 4:
    print("Medium Password")

else:
    print("Strong Password")