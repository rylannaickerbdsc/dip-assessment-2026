import tkinter as tk

# A list to keep track of tasks in memory
tasks = []


def add_task():
    # Get whatever text was typed into the box
    task_name = task_box.get()

    # Make sure the box isn't empty
    if task_name != "":
        tasks.append(task_name)  # Save it to our list
        task_list.insert(tk.END, task_name)  # Display it on the screen
        task_box.delete(0, tk.END)  # Clear the text box for the next task


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
add_button = tk.Button(window, text="Add Task", command=add_task)
add_button.pack(pady=5)

# List box to show added tasks
task_list = tk.Listbox(window, width=32, height=10)
task_list.pack(pady=10)

# Keep the window open
window.mainloop()