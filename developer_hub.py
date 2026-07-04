import subprocess
import sys
import webbrowser
from pathlib import Path
while True:

    print("\n================================")
    print("💻 KHADIJA'S DEVELOPER HUB")
    print("================================")

    print("1 📋 Job Application Tracker")
    print("2 🎮 Developer XP Tracker")
    print("3 🧪 Escape The Lab")
    print("4 🌐 Portfolio")
    print("5 🚪 Exit")

    choice = input("\nChoose: ")

    if choice == "1":
        print("\n📋 Opening Job Application Tracker...")
        subprocess.run(
            [sys.executable, "job_tracker.py"]
        )

    elif choice == "2":
        print("\n🎮 Opening Developer XP Tracker...")
        subprocess.run(
            [sys.executable, "developer_xp_tracker.py"]
        )

    elif choice == "3":
        print("\n🧪 Opening Escape The Lab...")
        subprocess.run(
            [sys.executable, "escape_the_lab.py"]
        )

    elif choice == "4":
        print("\n🌐 Opening Portfolio...")
        portfolio = Path("index.html").resolve()

        webbrowser.open(portfolio.as_uri())

    elif choice == "5":
        print("\n👋 Have a great coding day, Khadija!")
        break

    else:
        print("\n❌ Invalid choice.")