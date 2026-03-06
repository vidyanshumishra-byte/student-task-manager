import tkinter as tk
from tkinter import messagebox
import json

FILE_NAME = "tasks.json"

# Load tasks
def load_tasks():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except:
        return []

# Save tasks
def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file)

# Add task
def add_task():
    task = entry.get()

    if task == "":
        messagebox.showwarning("Warning", "Task cannot be empty")
        return

    priority = priority_var.get()

    tasks.append({
        "task": task,
        "priority": priority,
        "done": False
    })

    entry.delete(0, tk.END)
    save_tasks()
    show_tasks()

# Show tasks
def show_tasks():
    listbox.delete(0, tk.END)

    for i, t in enumerate(tasks):

        if t["priority"] == "High":
            emoji = "🔴"
        elif t["priority"] == "Medium":
            emoji = "🟡"
        else:
            emoji = "🟢"

        status = "✔" if t["done"] else "❌"

        text = f"{i+1}. {emoji} {t['task']} [{status}]"
        listbox.insert(tk.END, text)

# Delete task
def delete_task():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select a task first")
        return

    index = selected[0]
    tasks.pop(index)

    save_tasks()
    show_tasks()

# Mark complete
def mark_done():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select a task")
        return

    index = selected[0]

    tasks[index]["done"] = True

    save_tasks()
    show_tasks()

# GUI
root = tk.Tk()
root.title("Student Task Manager")
root.geometry("400x450")

tasks = load_tasks()

# Task entry
entry = tk.Entry(root, width=30)
entry.pack(pady=10)

# Priority dropdown
priority_var = tk.StringVar()
priority_var.set("Medium")

priority_menu = tk.OptionMenu(root, priority_var, "High", "Medium", "Low")
priority_menu.pack()

# Buttons
add_btn = tk.Button(root, text="Add Task", command=add_task)
add_btn.pack(pady=5)

done_btn = tk.Button(root, text="Mark Done", command=mark_done)
done_btn.pack(pady=5)

delete_btn = tk.Button(root, text="Delete Task", command=delete_task)
delete_btn.pack(pady=5)

# Task list
listbox = tk.Listbox(root, width=45)
listbox.pack(pady=10)

show_tasks()

root.mainloop()