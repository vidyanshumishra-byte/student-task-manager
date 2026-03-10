import customtkinter as ctk
import json
import os
from tkinter import messagebox

FILE_NAME = "tasks.json"

# --- Data Management ---
def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks_list):
    with open(FILE_NAME, "w") as file:
        json.dump(tasks_list, file, indent=4)

tasks = load_tasks()

# --- App Setup ---
ctk.set_appearance_mode("Dark")  # Ekdum modern dark theme
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("500x700")
app.title("Student Task Manager v4 (Stable Pro)")

# --- Core Logic & UI Update ---
def refresh_ui():
    # Pehle purane list items clear karo
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
        
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks.sort(key=lambda x: (x.get("done", False), priority_order.get(x.get("priority", "Low"), 3)))

    done_count = 0
    total = len(tasks)

    for index, t in enumerate(tasks):
        is_done = t.get("done", False)
        if is_done: done_count += 1
        
        # Priority Colors
        p_color = {"High": "#FF4B4B", "Medium": "#FACA2B", "Low": "#00CC96"}.get(t.get("priority", "Low"))
        
        # Task Card
        card = ctk.CTkFrame(scrollable_frame, corner_radius=10, fg_color="#2b2b2b" if not is_done else "#1f1f1f")
        card.pack(fill="x", pady=5, padx=5)

        # Priority Indicator Line
        indicator = ctk.CTkFrame(card, width=5, corner_radius=5, fg_color=p_color)
        indicator.pack(side="left", fill="y", padx=(5, 10), pady=5)

        # Checkbox & Task Name
        task_text = t.get("task", "")
        if is_done:
            task_text = f"~~ {task_text} ~~" # Done hone pe strikethrough effect

        checkbox = ctk.CTkCheckBox(
            card, text=task_text, 
            text_color="white" if not is_done else "gray",
            font=("Segoe UI", 14),
            command=lambda i=index: toggle_done(i)
        )
        if is_done:
            checkbox.select()
            
        checkbox.pack(side="left", padx=10, pady=15)

        # Delete Button
        delete_btn = ctk.CTkButton(
            card, text="🗑", width=40, height=30, 
            fg_color="#FF4B4B", hover_color="#cc3c3c",
            command=lambda i=index: delete_task(i)
        )
        delete_btn.pack(side="right", padx=10)

        # Due Date Text
        date_text = t.get("due_date", "")
        if date_text:
            date_label = ctk.CTkLabel(card, text=f"📅 {date_text}", text_color="#00CC96" if not is_done else "gray", font=("Segoe UI", 11))
            date_label.pack(side="right", padx=10)

    # Update Progress
    progress_label.configure(text=f"Progress: {done_count}/{total} Tasks Completed")
    if total > 0:
        progress_bar.set(done_count / total)
    else:
        progress_bar.set(0)

    save_tasks(tasks)

def add_task():
    task_text = entry_task.get().strip()
    date_text = entry_date.get().strip()
    priority = combo_priority.get()

    if not task_text:
        messagebox.showerror("Error", "Task cannot be empty!")
        return

    tasks.append({
        "task": task_text,
        "priority": priority,
        "due_date": date_text if date_text else "No Date",
        "done": False
    })
    
    # Text box clear karo
    entry_task.delete(0, ctk.END)
    entry_date.delete(0, ctk.END)
    refresh_ui()

def delete_task(index):
    del tasks[index]
    refresh_ui()

def toggle_done(index):
    tasks[index]["done"] = not tasks[index]["done"]
    refresh_ui()

# --- UI Components ---
# Header
header = ctk.CTkLabel(app, text="My Tasks", font=("Segoe UI", 28, "bold"))
header.pack(pady=(20, 5), padx=20, anchor="w")

progress_label = ctk.CTkLabel(app, text="Progress: 0/0 Tasks Completed", font=("Segoe UI", 12), text_color="gray")
progress_label.pack(padx=20, anchor="w")

progress_bar = ctk.CTkProgressBar(app, width=460, height=8, progress_color="#1f6aa5")
progress_bar.set(0)
progress_bar.pack(pady=(5, 15), padx=20)

# Input Frame
input_frame = ctk.CTkFrame(app, corner_radius=10)
input_frame.pack(fill="x", padx=20, pady=10)

entry_task = ctk.CTkEntry(input_frame, placeholder_text="What do you need to do?", font=("Segoe UI", 14), width=300)
entry_task.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="ew")

combo_priority = ctk.CTkComboBox(input_frame, values=["High", "Medium", "Low"], width=130)
combo_priority.set("Medium")
combo_priority.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="w")

entry_date = ctk.CTkEntry(input_frame, placeholder_text="Due Date (e.g. 15-Aug)", width=155)
entry_date.grid(row=1, column=1, padx=(0, 15), pady=(0, 15), sticky="e")

add_btn = ctk.CTkButton(input_frame, text="Add Task", font=("Segoe UI", 14, "bold"), command=add_task)
add_btn.grid(row=2, column=0, columnspan=2, padx=15, pady=(0, 15), sticky="ew")

# Scrollable Task List
scrollable_frame = ctk.CTkScrollableFrame(app, corner_radius=10, fg_color="transparent")
scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Boot App
refresh_ui()
app.mainloop()