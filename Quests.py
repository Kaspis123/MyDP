
import Database_tasks
from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry

def show(name1):
    # Create the tasks window
    tasks_window = Tk()
    tasks_window.title("My Tasks")

    # Create the tasks label
    tasks_label = Label(tasks_window, text="My Tasks", font=("Arial", 16))
    tasks_label.pack(padx=10, pady=10)

    # Create the tasks listbox
    tasks_listbox = Listbox(tasks_window, height=10, width=50)
    tasks_listbox.pack(padx=10, pady=10)

    # Get the tasks from the database
    tasks_listbox.delete(0, END)

    # Insert default value
    tasks_listbox.insert(END, "Name")

    # Insert the current script names from the database into the listbox
    for row in Database_tasks.conn.execute('SELECT name FROM tasks WHERE employee=?', (name1,)):
        tasks_listbox.insert(END, row[0])

    # Create the close button
    close_button = Button(tasks_window, text="Close", command=tasks_window.destroy)
    close_button.pack(padx=10, pady=10)

    tasks_listbox.bind('<Double-1>', lambda event: open_task_window(tasks_listbox.get(ANCHOR)))
    tasks_window.mainloop()


def open_task_window(task_name):
    print(task_name)
    # Retrieve task information from database
    c = Database_tasks.conn.cursor()
    c.execute("SELECT * FROM tasks WHERE name=?", (task_name,))
    task = c.fetchone()
    c.close()

    # Create the main window
    window = Tk()
    window.title("View Task")

    # Create the task name label and entry field
    name_label = Label(window, text="Task Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
    name_entry = Entry(window)
    name_entry.insert(0, task[0])
    name_entry.configure(state="readonly")
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

    # Create the task description label and text field
    description_label = Label(window, text="Task Description:")
    description_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
    description_entry = Text(window, height=5, width=30)
    description_entry.insert(END, task[1])
    description_entry.configure(state="disabled")
    description_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

    # Create the task creation date label and date entry field
    creation_date_label = Label(window, text="Task Creation Date:")
    creation_date_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
    creation_date_entry = DateEntry(window)
    creation_date_entry.insert(0, task[2])
    creation_date_entry.configure(state="disabled")
    creation_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

    # Create the task due date label and date entry field
    due_date_label = Label(window, text="Task Due Date:")
    due_date_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
    due_date_entry = DateEntry(window)
    due_date_entry.insert(0, task[3])
    due_date_entry.configure(state="disabled")
    due_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

    # Create the task employee label and entry field
    employee_label = Label(window, text="Task Employee:")
    employee_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
    employee_entry = Entry(window)
    employee_entry.insert(0, task[4])
    employee_entry.configure(state="disabled")
    employee_entry.grid(row=4, column=1, padx=5, pady=5, sticky=W)

    # Create the close button
    close_button = Button(window, text="Close", command=window.destroy)
    close_button.grid(row=5, column=1, padx=5, pady=5, sticky=E)

    # Make the window modal
    window.focus_set()
    window.grab_set()
    window.wait_window()

