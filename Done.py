import tkinter
import tkinter as tk
from tkinter import messagebox

from tkcalendar import DateEntry

import Finished_Tasks
import io
from tkinter import *
from tkinter.ttk import *
from datetime import date, datetime


def Done():
    windowAPP = tkinter.Tk()  # vytvořeni objektu
    windowAPP.minsize(width=800, height=800)  # Nastavení velikosti okna aplikace
    windowAPP.title("Finished Tasks")  # Pojmenování aplikace

    # Create a label for the listbox
    tasks_label = Label(windowAPP, text="Finished Tasks", font=("Helvetica", 16))
    tasks_label.pack(padx=10, pady=10)

    # Create a frame to hold the listbox and scrollbar
    tasks_frame = Frame(windowAPP)
    tasks_frame.pack()

    # Create the tasks listbox
    tasks_listbox = Listbox(tasks_frame, height=10, width=50, font=("Helvetica", 14), bd=2, bg="#ffffff",
                            selectbackground="#cccccc", highlightthickness=0, justify="center")
    tasks_listbox.pack(side="left", padx=10, pady=10, fill="both", expand=True)

    # Create the scrollbar
    scrollbar = Scrollbar(tasks_frame, orient="vertical", command=tasks_listbox.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the scrollbar to control the listbox
    tasks_listbox.config(yscrollcommand=scrollbar.set)


    tasks_listbox.delete(0, END)

    # Insert the current distinct script names from the database into the listbox
    for row in Finished_Tasks.conn.execute('SELECT name FROM finished_tasks'):
        tasks_listbox.insert(END, row[0])

    tasks_listbox.bind('<Double-1>', lambda event: open(tasks_listbox.get(ANCHOR)))
    windowAPP.mainloop()

def open(event):
    # Retrieve task information from database
    print(event)
    c = Finished_Tasks.conn.cursor()
    c.execute("SELECT * FROM finished_tasks WHERE name=?", (event,))
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
    creation_date_str = task[2]
    creation_date = datetime.strptime(creation_date_str, '%d/%m/%Y').date()
    creation_date_entry = DateEntry(window, date_pattern='dd/mm/yyyy')
    creation_date_entry.set_date(creation_date)
    creation_date_entry.configure(state="disabled")
    creation_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

    due_date_label = Label(window, text="Task Due Date:")
    due_date_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
    due_date_str = task[3]
    due_date = datetime.strptime(due_date_str, '%d/%m/%Y').date()
    due_date_entry = DateEntry(window, date_pattern='dd/mm/yyyy')
    due_date_entry.set_date(due_date)
    due_date_entry.configure(state="disabled")
    due_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

    # Create the task employee label and entry field
    employee_label = Label(window, text="Task Employee:")
    employee_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
    employee_entry = Entry(window)
    employee_entry.insert(0, task[4])
    employee_entry.configure(state="disabled")
    employee_entry.grid(row=4, column=1, padx=5, pady=5, sticky=W)

    finished_date_label = Label(window, text="Task Finished Date:")
    finished_date_label.grid(row=5, column=0, padx=5, pady=5, sticky=W)
    finished_date_str = task[5]
    finished_date = datetime.strptime(finished_date_str, '%d/%m/%Y').date()
    finished_date_entry = DateEntry(window, date_pattern='dd/mm/yyyy')
    finished_date_entry.set_date(finished_date)
    finished_date_entry.configure(state="disabled")
    finished_date_entry.grid(row=5, column=1, padx=5, pady=5, sticky=W)



    # Create the close button
    close_button = Button(window, text="Close", command=window.destroy)
    close_button.grid(row=6, column=1, padx=5, pady=5, sticky=E)

    # Make the window modal
    window.focus_set()
    window.grab_set()
    window.wait_window()


