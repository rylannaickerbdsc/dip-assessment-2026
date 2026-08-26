import os
import tkinter as tk
from tkinter import messagebox
from task import Task

# Path to persistent data file
FILE_NAME = "tasks.txt"

# Main in-memory list to store Task objects
tasks = []


def load_tasks_from_file():
    """Reads tasks.txt on startup and rebuilds the tasks list."""
    if not os.path.exists(FILE_NAME):
        return

    with open(FILE_NAME, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 4:
                name, subject, duration, priority = parts
                if duration.isdigit():
                    task = Task(name, subject, int(duration), priority)
                    tasks.append(task)
                    task_list.insert(tk.END, task.get_details())


def save_tasks_to_file():
    """Overwrites tasks.txt with the current list of tasks."""
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write(task.to_file_line())


def add_task():
    """Validates input fields, instantiates Task object, and updates GUI list."""
    name = name_box.get().strip()
    subject = subject_box.get().strip().title()
    mins = mins_box.get().strip()
    priority = priority_var.get()

    # Validation 1: Blank entries
    if not name or not subject:
        messagebox.showerror(
            "Input Error", "Please fill in both Task Name and Subject!"
        )
        return

    # Validation 2: Numeric duration check
    if not mins.isdigit() or int(mins) <= 0:
        messagebox.showerror(
            "Input Error", "Minutes must be a positive whole number!"
        )
        return

    # Instantiate task and save
    new_task = Task(name, subject, int(mins), priority)
    tasks.append(new_task)
    save_tasks_to_file()

    # Display formatted string in Listbox
    task_list.insert(tk.END, new_task.get_details())

    # Clear text fields
    name_box.delete(0, tk.END)
    subject_box.delete(0, tk.END)
    mins_box.delete(0, tk.END)


# window setup
window = tk.Tk()
window.title("Study System - Version 2.2")
window.geometry("380x500")

# Heading
tk.Label(window, text="My Study Planner", font=("Arial", 14, "bold")).pack(pady=10)

# Input Field 1: Task Name
tk.Label(window, text="Task Name:").pack(anchor="w", padx=30)
name_box = tk.Entry(window, width=38)
name_box.pack(pady=2)

# Input Field 2: Subject
tk.Label(window, text="Subject (e.g., Math, Science):").pack(anchor="w", padx=30)
subject_box = tk.Entry(window, width=38)
subject_box.pack(pady=2)

# Input Field 3: Duration (Minutes)
tk.Label(window, text="Time Needed (mins):").pack(anchor="w", padx=30)
mins_box = tk.Entry(window, width=38)
mins_box.pack(pady=2)

# Input Field 4: Priority (Radio Buttons)
tk.Label(window, text="Priority:").pack(anchor="w", padx=30)
radio_frame = tk.Frame(window)
radio_frame.pack(pady=2)

priority_var = tk.StringVar(value="Med")
tk.Radiobutton(
    radio_frame, text="High", variable=priority_var, value="High"
).pack(side="left", padx=10)
tk.Radiobutton(
    radio_frame, text="Med", variable=priority_var, value="Med"
).pack(side="left", padx=10)
tk.Radiobutton(
    radio_frame, text="Low", variable=priority_var, value="Low"
).pack(side="left", padx=10)

# Action Button
add_button = tk.Button(
    window,
    text="Add Task",
    command=add_task,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 9, "bold"),
    width=15,
)
add_button.pack(pady=10)

# Display Area
tk.Label(window, text="Your Tasks:").pack(anchor="w", padx=30)
task_list = tk.Listbox(window, width=42, height=8)
task_list.pack(pady=5)

# Load existing tasks when launching app
load_tasks_from_file()

window.mainloop()