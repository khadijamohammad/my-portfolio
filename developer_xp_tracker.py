xp = 0
achievements = []

try:
    with open("xp.txt", "r") as file:
        xp = int(file.read())

except:
    xp = 0

def check_achievements():

    global achievements


    if xp >= 1:

        if "🏅 First XP" not in achievements:

            achievements.append(
                "🏅 First XP"
            )


    if xp >= 100:

        if "🥉 Level Up" not in achievements:

            achievements.append(
                "🥉 Level Up"
            )


    if xp >= 300:

        if "🥈 Builder" not in achievements:

            achievements.append(
                "🥈 Builder"
            )


    if xp >= 500:

        if "🥇 Coding Machine" not in achievements:

            achievements.append(
                "🥇 Coding Machine"
            )
while True:

    print("\n====================")
    print("🎮 DEVELOPER XP TRACKER")
    print("====================")

    print("1 ➜ Add XP")
    print("2 ➜ View XP")
    print("3 ➜ Level Check")
    print("4 ➜ Achievements")

    print("5 ➜ Exit")

    choice = input("\nChoose: ")


    if choice == "1":

        earned = int(
            input(
                "🏆 XP Earned: "
            )
        )

        xp += earned

        check_achievements()


        with open(
            "xp.txt",
            "w"
        ) as file:

            file.write(
                str(
                    xp
                )
            )

        print(
            "\n🔥 XP Added!"
        )


    elif choice == "2":

        print(
            f"\n🏆 Current XP: {xp}"
        )


    elif choice == "3":

        level = xp // 100 + 1

        print(
            "\n================"
        )

        print(
            f"⭐ LEVEL {level}"
        )

        print(
            f"⚡ XP: {xp}"
        )

        print(
            "================"
        )

    elif choice == "4":

        print(
            "\n🏆 ACHIEVEMENTS"
        )

        print(
            "================"
        )


        if achievements:

            for badge in achievements:

                print(
                    badge
                )

        else:

            print(
                "No achievements yet."
            )
    elif choice == "5":

        print(
            "\n🌙 Keep Building"
        )

        break


    else:

        print(
            "\n❌ Invalid option"
        )