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
    subject = "General"  # Temporary default until UI field is added
    mins = mins_box.get().strip()
    priority = priority_box.get().strip().title() or "Med"

    # Valid input Check 1: Empty Task Name
    if not name:
        messagebox.showerror("Input Error", "Please enter a task name!")
        return

    # Valid input Check 2: Invalid or non-positive minutes
    if not mins.isdigit() or int(mins) <= 0:
        messagebox.showerror("Input Error", "Minutes must be a positive whole number!")
        return

    # Create Task object and store in Python list
    new_task = Task(name, subject, int(mins), priority)
    tasks.append(new_task)
    save_tasks_to_file()

    # Display formatted string in Listbox
    task_list.insert(tk.END, new_task.get_details())

    # Clear input boxes
    name_box.delete(0, tk.END)
    mins_box.delete(0, tk.END)
    priority_box.delete(0, tk.END)


# window
window = tk.Tk()
window.title("Study System - Version 2.1")
window.geometry("350x460")

# Heading
tk.Label(window, text="My Study System", font=("Arial", 14, "bold")).pack(pady=10)

# Input 1: Task Name
tk.Label(window, text="Task Name:").pack(anchor="w", padx=30)
name_box = tk.Entry(window, width=34)
name_box.pack(pady=3)

# Input 2: Duration (Minutes)
tk.Label(window, text="Time Needed (mins):").pack(anchor="w", padx=30)
mins_box = tk.Entry(window, width=34)
mins_box.pack(pady=3)

# Input 3: Priority
tk.Label(window, text="Priority (Low / Med / High):").pack(anchor="w", padx=30)
priority_box = tk.Entry(window, width=34)
priority_box.pack(pady=3)

# Action Button
add_button = tk.Button(
    window,
    text="Add Task",
    command=add_task,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold"),
)
add_button.pack(pady=12)

# Display Area
tk.Label(window, text="Your Tasks:").pack(anchor="w", padx=30)
task_list = tk.Listbox(window, width=38, height=8)
task_list.pack(pady=5)

# Load file data at startup
load_tasks_from_file()

window.mainloop()