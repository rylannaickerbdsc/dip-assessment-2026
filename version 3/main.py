import os
import tkinter as tk
from tkinter import messagebox
from task import Task

# Path to persistent data file
FILE_NAME = "tasks.txt"

# Memory list for Task objects
tasks = []


# --- FILE STORAGE FUNCTIONS ---
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
    refresh_listbox()


def save_tasks_to_file():
    """Overwrites tasks.txt with the current list of tasks."""
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write(task.to_file_line())


# --- DISPLAY & SORTING FUNCTIONS ---
def refresh_listbox():
    """Clears and updates the display listbox with the sorted tasks list."""
    task_list.delete(0, tk.END)
    for task in tasks:
        task_list.insert(tk.END, task.get_details())


def sort_by_priority():
    """Sorts tasks by priority (High -> Med -> Low)."""
    tasks.sort(key=lambda t: t.get_priority_rank())
    save_tasks_to_file()
    refresh_listbox()


def sort_by_subject():
    """Sorts tasks alphabetically by subject name."""
    tasks.sort(key=lambda t: t.subject.lower())
    save_tasks_to_file()
    refresh_listbox()


# --- ACTION FUNCTIONS ---
def add_task():
    """Validates input, creates a Task object, saves it, and updates display."""
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

    # Sort by priority by default on add
    sort_by_priority()

    # Clear text fields
    name_box.delete(0, tk.END)
    subject_box.delete(0, tk.END)
    mins_box.delete(0, tk.END)


def mark_done():
    """Deletes the selected task from memory and updates tasks.txt."""
    try:
        selected_index = task_list.curselection()[0]
        # Remove task from memory list
        removed_task = tasks.pop(selected_index)
        # Update file and screen
        save_tasks_to_file()
        refresh_listbox()
        messagebox.showinfo(
            "Task Completed", f"Finished: '{removed_task.name}'!"
        )
    except IndexError:
        messagebox.showwarning(
            "Selection Error", "Please select a task from the list first!"
        )


# --- WINDOW SETUP ---
window = tk.Tk()
window.title("Study System - Version 3 Final")
window.geometry("380x570")

# Heading
tk.Label(window, text="My Study Planner", font=("Arial", 14, "bold")).pack(
    pady=10
)

# Input Field 1: Task Name
tk.Label(window, text="Task Name:").pack(anchor="w", padx=30)
name_box = tk.Entry(window, width=38)
name_box.pack(pady=2)

# Input Field 2: Subject
tk.Label(window, text="Subject (e.g., Math, Science):").pack(
    anchor="w", padx=30
)
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

# Action Buttons
add_button = tk.Button(
    window,
    text="Add Task",
    command=add_task,
    bg="#4CAF50",
    fg="white",
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

# Display Area (Listbox & Scrollbar)
tk.Label(window, text="Your Tasks:").pack(anchor="w", padx=30, pady=(10, 0))
task_list = tk.Listbox(window, width=42, height=9)
task_list.pack(pady=5)

# Delete / Complete Task Button
done_button = tk.Button(
    window,
    text="✓ Mark Done / Delete",
    command=mark_done,
    bg="#f44336",
    fg="white",
    font=("Arial", 9, "bold"),
)
done_button.pack(pady=5)

# Load existing tasks when launching app
load_tasks_from_file()

window.mainloop()