import os
import tkinter as tk
from tkinter import messagebox
from task import Task

# File name for saving tasks
FILE_NAME = "tasks.txt"

# Task object list stored in memory
tasks = []


# --- FILE STORAGE LOGIC ---
def load_tasks_from_file():
    """Reads saved tasks from tasks.txt when launching."""
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
    refresh_listbox()


def save_tasks_to_file():
    """Saves current task list to tasks.txt."""
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write(task.to_file_line())


# --- GUI UPDATE & SORTING ---
def refresh_listbox():
    """Refreshes the on-screen listbox."""
    task_list.delete(0, tk.END)
    for task in tasks:
        task_list.insert(tk.END, task.get_details())


def sort_by_priority():
    """Sorts list by Priority (High -> Med -> Low)."""
    tasks.sort(key=lambda t: t.get_priority_rank())
    save_tasks_to_file()
    refresh_listbox()


def sort_by_subject():
    """Sorts list alphabetically by Subject."""
    tasks.sort(key=lambda t: t.subject.lower())
    save_tasks_to_file()
    refresh_listbox()


# --- ACTION FUNCTIONS ---
def add_task():
    """Validates input, creates a task, saves it, and refreshes screen."""
    name = name_box.get().strip()
    subject = subject_box.get().strip().title()
    mins = mins_box.get().strip()
    priority = priority_var.get()

    # Validation: Check empty inputs
    if not name or not subject:
        messagebox.showerror(
            "Input Error", "Please fill in both Task Name and Subject!"
        )
        return

    # Validation: Check numeric time
    if not mins.isdigit() or int(mins) <= 0:
        messagebox.showerror(
            "Input Error", "Minutes must be a positive whole number!"
        )
        return

    # Create task object and append to list
    new_task = Task(name, subject, int(mins), priority)
    tasks.append(new_task)

    # Sort high priority tasks to top automatically
    sort_by_priority()

    # Clear input fields
    name_box.delete(0, tk.END)
    subject_box.delete(0, tk.END)
    mins_box.delete(0, tk.END)


def mark_done():
    """Deletes selected task from memory list and updates text file."""
    try:
        selected_index = task_list.curselection()[0]
        removed_task = tasks.pop(selected_index)
        save_tasks_to_file()
        refresh_listbox()
        messagebox.showinfo(
            "Task Completed", f"Finished: '{removed_task.name}'!"
        )
    except IndexError:
        messagebox.showwarning(
            "Selection Error", "Please click on a task from the list first!"
        )


# --- APPLICATION INTERFACE ---
window = tk.Tk()
window.title("Study System - Version 3 Final")
window.geometry("380x570")

# Header
tk.Label(window, text="My Study Planner", font=("Arial", 14, "bold")).pack(
    pady=10
)

# Task Name Input
tk.Label(window, text="Task Name:").pack(anchor="w", padx=30)
name_box = tk.Entry(window, width=38)
name_box.pack(pady=2)

# Subject Input
tk.Label(window, text="Subject (e.g., Math, Science):").pack(
    anchor="w", padx=30
)
subject_box = tk.Entry(window, width=38)
subject_box.pack(pady=2)

# Duration Input
tk.Label(window, text="Time Needed (mins):").pack(anchor="w", padx=30)
mins_box = tk.Entry(window, width=38)
mins_box.pack(pady=2)

# Priority Options (Radio Buttons)
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

# Add Task Button (Clear text styling)
add_button = tk.Button(
    window,
    text="Add Task",
    command=add_task,
    font=("Arial", 9, "bold"),
    width=15,
)
add_button.pack(pady=8)

# Sorting Control Buttons
sort_frame = tk.Frame(window)
sort_frame.pack(pady=2)
tk.Button(
    sort_frame,
    text="Sort by Priority",
    command=sort_by_priority,
    font=("Arial", 8),
).pack(side="left", padx=4)
tk.Button(
    sort_frame,
    text="Sort by Subject",
    command=sort_by_subject,
    font=("Arial", 8),
).pack(side="left", padx=4)

# Display Listbox
tk.Label(window, text="Your Tasks:").pack(anchor="w", padx=30, pady=(10, 0))
task_list = tk.Listbox(window, width=42, height=9)
task_list.pack(pady=5)

# Mark Done Button (Clear text styling)
done_button = tk.Button(
    window,
    text="✓ Mark Done / Delete",
    command=mark_done,
    font=("Arial", 9, "bold"),
)
done_button.pack(pady=5)

# Load saved items when app launches
load_tasks_from_file()

window.mainloop()