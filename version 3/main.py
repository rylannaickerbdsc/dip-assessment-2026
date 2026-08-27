import os
import tkinter as tk
from tkinter import messagebox
from task import Task

FILE_NAME = "tasks.txt"
tasks = []

# COLOR PALETTE
BG_MAIN = "#FDEED0"  
BG_CARD = "#FFFFFF"  
TEXT_MAIN = "#4D250E"     
TEXT_MUTED = "#4D250E"   
ACCENT_HEADER = "#4D250E"  
SELECT_BG = "#E0E7FF"  
SELECT_FG = "#3730A3"  
BORDER_COLOR = "#4D250E"   


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

    if not name or not subject:
        messagebox.showerror(
            "Input Error", "Please fill in both Task Name and Subject!"
        )
        return

    if not mins.isdigit() or int(mins) <= 0:
        messagebox.showerror(
            "Input Error", "Minutes must be a positive whole number!"
        )
        return

    new_task = Task(name, subject, int(mins), priority)
    tasks.append(new_task)

    sort_by_priority()

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
window.geometry("410x600")
window.configure(bg=BG_MAIN)

# Main Title Header
tk.Label(
    window,
    text="My Study Planner",
    font=("Segoe UI", 16, "bold"),
    fg=ACCENT_HEADER,
    bg=BG_MAIN,
).pack(pady=(16, 12))

# Task Name Field
tk.Label(
    window,
    text="TASK NAME",
    font=("Segoe UI", 8, "bold"),
    fg=TEXT_MUTED,
    bg=BG_MAIN,
).pack(anchor="w", padx=36)
name_box = tk.Entry(
    window,
    width=38,
    bg=BG_CARD,
    fg=TEXT_MAIN,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER_COLOR,
    highlightcolor=ACCENT_HEADER,
    font=("Segoe UI", 9),
)
name_box.pack(pady=(2, 8), ipady=3)

# Subject Field
tk.Label(
    window,
    text="SUBJECT (E.G. MATH, SCIENCE)",
    font=("Segoe UI", 8, "bold"),
    fg=TEXT_MUTED,
    bg=BG_MAIN,
).pack(anchor="w", padx=36)
subject_box = tk.Entry(
    window,
    width=38,
    bg=BG_CARD,
    fg=TEXT_MAIN,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER_COLOR,
    highlightcolor=ACCENT_HEADER,
    font=("Segoe UI", 9),
)
subject_box.pack(pady=(2, 8), ipady=3)

# Duration Field
tk.Label(
    window,
    text="TIME NEEDED (MINUTES)",
    font=("Segoe UI", 8, "bold"),
    fg=TEXT_MUTED,
    bg=BG_MAIN,
).pack(anchor="w", padx=36)
mins_box = tk.Entry(
    window,
    width=38,
    bg=BG_CARD,
    fg=TEXT_MAIN,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER_COLOR,
    highlightcolor=ACCENT_HEADER,
    font=("Segoe UI", 9),
)
mins_box.pack(pady=(2, 8), ipady=3)

# Priority Radio Buttons
tk.Label(
    window,
    text="PRIORITY LEVEL",
    font=("Segoe UI", 8, "bold"),
    fg=TEXT_MUTED,
    bg=BG_MAIN,
).pack(anchor="w", padx=36)
radio_frame = tk.Frame(window, bg=BG_MAIN)
radio_frame.pack(pady=(2, 8))

priority_var = tk.StringVar(value="Med")
for prio in ["High", "Med", "Low"]:
    tk.Radiobutton(
        radio_frame,
        text=prio,
        variable=priority_var,
        value=prio,
        bg=BG_MAIN,
        fg=TEXT_MAIN,
        activebackground=BG_MAIN,
        highlightbackground=BG_MAIN,
        font=("Segoe UI", 9),
    ).pack(side="left", padx=12)

# Add Task Button (highlightbackground removes outer dark box on macOS)
add_button = tk.Button(
    window,
    text="Add Task",
    command=add_task,
    font=("Segoe UI", 9, "bold"),
    width=16,
    highlightbackground=BG_MAIN,
    cursor="hand2",
)
add_button.pack(pady=6)

# Sorting Control Buttons (highlightbackground removes outer dark box on macOS)
sort_frame = tk.Frame(window, bg=BG_MAIN)
sort_frame.pack(pady=4)
tk.Button(
    sort_frame,
    text="Sort by Priority",
    command=sort_by_priority,
    font=("Segoe UI", 8),
    highlightbackground=BG_MAIN,
    cursor="hand2",
).pack(side="left", padx=5)
tk.Button(
    sort_frame,
    text="Sort by Subject",
    command=sort_by_subject,
    font=("Segoe UI", 8),
    highlightbackground=BG_MAIN,
    cursor="hand2",
).pack(side="left", padx=5)

# Display Listbox Section
tk.Label(
    window,
    text="CURRENT TASKS",
    font=("Segoe UI", 8, "bold"),
    fg=TEXT_MUTED,
    bg=BG_MAIN,
).pack(anchor="w", padx=36, pady=(10, 2))

task_list = tk.Listbox(
    window,
    width=42,
    height=7,
    bg=BG_CARD,
    fg=TEXT_MAIN,
    selectbackground=SELECT_BG,
    selectforeground=SELECT_FG,
    relief="flat",
    highlightthickness=1,
    highlightbackground=BORDER_COLOR,
    font=("Consolas", 9),
)
task_list.pack(pady=4)

# Mark Done Button (highlightbackground removes outer dark box on macOS)
done_button = tk.Button(
    window,
    text="✓ Mark Done / Delete",
    command=mark_done,
    font=("Segoe UI", 9, "bold"),
    highlightbackground=BG_MAIN,
    cursor="hand2",
)
done_button.pack(pady=(4, 15))

# Load saved items on launch
load_tasks_from_file()

window.mainloop()