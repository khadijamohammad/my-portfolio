import random
import string


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