tasks = []

try:
    with open("tasks.txt", "r") as file:
        tasks = file.read().splitlines()
except FileNotFoundError:
    pass

while True:
    print("\nTO-DO APP")
    print("1 - Add Task")
    print("2 - View Tasks")
    print("3 - Exit")
    print("4 - Delete Task")
    choice = input("Choose: ")

    if choice == "1":
        task = input("Enter task: ")
        tasks.append(task)
        with open("tasks.txt", "w") as file:
            for t in tasks:
                file.write(t + "\n")
        print("Task added!")

    elif choice == "2":
        print("\nYour Tasks:")
        if len(tasks) == 0:
            print("No tasks yet")
        else:
            for i, task in enumerate(tasks):
                print(i + 1, "-", task)

    elif choice == "4":
        print("\nTasks:")
        for i, task in enumerate(tasks):
            print(i + 1, "-", task)

        try:
            remove = int(input("Task number to delete: "))
        except ValueError:
            print("Invalid number")
            continue

        if 1 <= remove <= len(tasks):
            tasks.pop(remove - 1)
            with open("tasks.txt", "w") as file:
                for t in tasks:
                    file.write(t + "\n")
            print("Task removed!")
        else:
            print("Invalid task number")

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice")