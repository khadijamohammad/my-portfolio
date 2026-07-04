from pathlib import Path
from datetime import datetime

project_folder = Path(".")

import subprocess
import sys
python_files = list(project_folder.glob("*.py"))

total_projects = len(python_files)

today = datetime.now().strftime("%d %B %Y")

backup_folder = Path("Backups")

if backup_folder.exists():
    backup_status = "✅ READY"
else:
    backup_status = "❌ NOT FOUND"

    print("=" * 40)
print("💻 KHADIJA OS")
print("Developer Control Center")
print("=" * 40)

print()

print("👋 Welcome back, Khadija!")

print()

print(f"📁 Projects Found : {total_projects}")
print(f"📅 Date           : {today}")
print(f"💾 Backup Status  : {backup_status}")

print()

print("=" * 40)
print("1 📋 Open Developer Hub")
print("2 📦 Project Save Manager")
print("3 🚪 Exit")
print("=" * 40)

choice = input("\nChoose: ")

if choice == "1":
    print("\n💻 Opening Developer Hub...\n")
    subprocess.run([sys.executable, "developer_hub.py"])

elif choice == "2":
    print("\n📦 Opening Project Save Manager...\n")
    subprocess.run([sys.executable, "project_save_manager.py"])

elif choice == "3":
    print("\n👋 Goodbye, Khadija!")
    print("Have an awesome coding day! 🚀")

else:
    print("\n❌ Invalid choice.")

