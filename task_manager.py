import tkinter as tk
from tkinter import ttk
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
    due_date = due_entry.get()

    tasks.append({
        "task": task,
        "priority": priority,
        "due_date": due_date,
        "done": False
    })
    sort_tasks()

    entry.delete(0, tk.END)
    due_entry.delete(0, tk.END)
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

        text = f"{i+1}. {emoji} {t['task']} (Due: {t['due']}) [{status}]"
        listbox.insert(tk.END, text)
        done_tasks = sum(1 for t in tasks if t["done"])
    total_tasks = len(tasks)

    task_counter.config(text=f"Tasks Completed: {done_tasks}/{total_tasks}")
    if total_tasks > 0:
        progress["value"] = (done_tasks / total_tasks) * 100
    else:        progress["value"] = 0

# Sort tasks by priority and completion
def sort_tasks():
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks.sort(key=lambda x: (x["done"], priority_order[x["priority"]]))

# Delete task
def delete_task():
    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning("Warning", "Select a task first")
        return

    index = selected[0]
    tasks[index]["done"] = True
    sort_tasks()

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
root.configure(bg="#1e1e1e")
root.title("Student Task Manager")
root.option_add("*Font", "Arial 11")
root.geometry("400x450")
task_counter = tk.Label(root, text="", font=("Arial", 12))
task_counter.pack()
progress = ttk.Progressbar(root, length=200, mode="determinate")
progress.pack(pady=5)

tasks = load_tasks()

#here
search_entry = tk.Entry(root, width=30)
search_entry.pack(pady=5)

def search_task():
    keyword = search_entry.get().lower()

    listbox.delete(0, tk.END)

    for i, t in enumerate(tasks):
        if keyword in t["task"].lower():

            if t["priority"] == "High":
                emoji = "🔴"
            elif t["priority"] == "Medium":
                emoji = "🟡"
            else:
                emoji = "🟢"

            status = "✔" if t["done"] else "❌"

            text = f"{i+1}. {emoji} {t['task']} [{status}]"
            listbox.insert(tk.END, text)

search_btn = tk.Button(root, text="Search", command=search_task)
search_btn.pack()

# Task entry
entry = tk.Entry(root, width=30, bg="#2d2d2d", fg="white", insertbackground="white")
entry.pack(pady=10)

#entry2
due_entry = tk.Entry(root, width=30, bg="#2d2d2d", fg="white", insertbackground="white")
due_entry.insert(0, "Due Date (DD-MM)")
due_entry.pack(pady=5)

# Priority dropdown
priority_var = tk.StringVar()
priority_var.set("Medium")

priority_menu = tk.OptionMenu(root, priority_var, "High", "Medium", "Low")
priority_menu.pack()

# Buttons
add_btn = tk.Button(root, text="Add Task", command=add_task, bg="#3a3a3a", fg="white")
add_btn.pack(pady=5)

done_btn = tk.Button(root, text="Mark Done", command=mark_done)
done_btn.pack(pady=5)

delete_btn = tk.Button(root, text="Delete Task", command=delete_task)
delete_btn.pack(pady=5)

# Task list
listbox = tk.Listbox(root, width=45,height =12, bg="#2d2d2d", fg="white")
listbox.pack(pady=10)
listbox.bind("<Double-Button-1>", lambda event: mark_done())
listbox.bind("<Button-3>", lambda event: delete_task())

show_tasks()

root.mainloop()