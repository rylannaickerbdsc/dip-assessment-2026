import tkinter as tk

tasks = []


def add_task():
    task_name = task_box.get()
    if task_name != "":
        tasks.append(task_name)
        task_list.insert(tk.END, task_name)
        task_box.delete(0, tk.END)


#window
window = tk.Tk()
window.title("Study System - Version 2")
window.geometry("350x460")

# Heading
tk.Label(window, text="My Study System", font=("Arial", 14, "bold")).pack(pady=10)

# Input 1: Task Name
tk.Label(window, text="Task Name:").pack(anchor="w", padx=30)
name_box = tk.Entry(window, width=34)
name_box.pack(pady=3)

# Input  2: Duration (Minutes)
tk.Label(window, text="Time Needed (mins):").pack(anchor="w", padx=30)
mins_box = tk.Entry(window, width=34)
mins_box.pack(pady=3)

# Input  3: Priority
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

window.mainloop()