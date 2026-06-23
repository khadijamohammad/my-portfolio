import random
import string


while True:

    print("\nCYBER TOOL")
    print("1 - Generate Password")
    print("2 - Check Password Strength")
    print("3 - Exit")

    choice = input("Choose: ")


    if choice == "1":

        length = int(input("Choose password length: "))

        characters = (
            string.ascii_letters +
            string.digits +
            "!@#$%^&*"
        )

        password = ""

        for i in range(length):
            password += random.choice(characters)

        print("\nGenerated Password:")
        print(password)


    elif choice == "2":

        password = input("Enter password: ")

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

        elif score <= 4:
            print("Medium Password")

        else:
            print("Strong Password")


    elif choice == "3":

        print("Goodbye!")
        break


    else:
        print("Invalid choice")