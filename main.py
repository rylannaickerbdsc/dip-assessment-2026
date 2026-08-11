import tkinter as tk

# window
window = tk.Tk()
window.title("Study System - Version 1")
window.geometry("320x350")

# Title at the top
title_label = tk.Label(
    window, text="My Study System", font=("Arial", 14, "bold")
)
title_label.pack(pady=10)

# Text box to type task names
task_box = tk.Entry(window, width=28)
task_box.pack(pady=5)

# Add Task Button
add_button = tk.Button(window, text="Add Task")
add_button.pack(pady=5)

# List box to show added tasks
task_list = tk.Listbox(window, width=32, height=10)
task_list.pack(pady=10)

# Keep the window open
window.mainloop()