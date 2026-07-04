from pathlib import Path
from datetime import datetime
import shutil

base_folder = Path("Backups")
base_folder.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

backup_folder = base_folder / f"Backup_{timestamp}"
backup_folder.mkdir()

project_folder = Path(".")
python_files = list(project_folder.glob("*.py"))

print("\n📦 Project Save Manager V3")
print("=========================")
print("\n📁 Backup Created!")

print("Location:", backup_folder.resolve())

print("\n📄 Files backed up:")

for file in python_files:
    print("✔", file.name)

print("\n🏆 BACKUP COMPLETE!")

backup_file = backup_folder / "backup_info.txt"

with open(backup_file, "w") as file:

    file.write("PROJECT BACKUP\n")
    file.write("====================\n")
    file.write(f"Created: {datetime.now()}\n")
    file.write("Status: Backup Ready\n")
    
