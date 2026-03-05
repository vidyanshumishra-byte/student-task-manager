import json

try:
    with open("tasks.json", "r") as file:
        tasks = json.load(file)
except:
    tasks = []

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)
def show_menu():
    print("\n--- Student Task Manager ---")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Delete Task")
    print("4. Mark Complete")
    print("5. Exit")

while True:
    show_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        task = input("Enter task: ")
        tasks.append({"task": task, "completed": False})
        save_tasks()
        print("Task added successfully!")

    elif choice == "2":
        if len(tasks) == 0:
            print("No tasks available.")
        else:
            for i in range(len(tasks)):
                status = "✓" if tasks[i]["completed"] else "✗"
                print(i + 1, ".", tasks[i]["task"], "-", status)

    elif choice == "3":
        if len(tasks) == 0:
            print("No tasks available.")
        else:
            for i in range(len(tasks)):
                print(i + 1, ".", tasks[i]["task"])

            num = int(input("Enter task number to delete: "))
            if 1 <= num <= len(tasks):
                tasks.pop(num - 1)
                save_tasks()
                print("Task deleted successfully!")
            else:
                print("Invalid task number.")

    elif choice == "4":
        if len(tasks) == 0:
            print("No tasks available.")
        else:
            for i in range(len(tasks)):
                print(i + 1, ".", tasks[i]["task"])

            num = int(input("Enter task number to mark complete: "))
            if 1 <= num <= len(tasks):
                tasks[num - 1]["completed"] = True
                save_tasks()
                print("Task marked as complete!")
            else:
                print("Invalid task number.")

    elif choice == "5":
        print("Exiting program...")
        break

    else:
        print("Invalid choice. Try again.")