import Database_tasks
from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry
from datetime import date

import Database_teams
from Quests import show, show_pdf_file
import customtkinter


def Running():
    # Create the tasks window
    customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    RED = "#FF3333"
    ORANGE = "#FFA500"
    GREEN = "#33FF33"
    running_tasks_window= customtkinter.CTk()
    running_tasks_window.title("Currently Running Tasks")

    # Create the tasks label
    # tasks_label = customtkinter.CTkLabel(running_tasks_window, text="Currently Running Tasks", width=300,
    #                            height=50,
    #                            fg_color=("white", "gray75"),
    #                            corner_radius=8, padx=20,
    #                     pady=20)
    # tasks_label.pack(padx=10, pady=10)
    scrollbar = Scrollbar(running_tasks_window, orient="vertical")
    scrollbar.pack(side="right", fill="y")
    # Create the tasks listbox
    tasks_listbox = Listbox(running_tasks_window, height=10, width=50, font=("Helvetica", 14), bd=2, bg="#ffffff",
                            selectbackground="#cccccc", highlightthickness=0,yscrollcommand=scrollbar.set)
    tasks_listbox.pack(padx=10, pady=10)
    scrollbar.config(command=tasks_listbox.yview)


    close_button = customtkinter.CTkButton(running_tasks_window, text="Close", command=running_tasks_window.destroy)
    close_button.pack(padx=10, pady=10)

    tasks_listbox.delete(0, END)

    # Insert default value
    tasks_listbox.insert(END, "{:<30} {:^30}".format("Name of the task", "Name of the employee"))


    for row in Database_teams.conn.execute('SELECT name, employee, due_date FROM tasks ORDER BY due_date ' ):
        # Parse the due date from the database row
        due_date_str = row[2]
        due_date = datetime.strptime(due_date_str, '%d/%m/%Y').date()

        # Calculate the number of days until the due date
        days_remaining = (due_date - date.today()).days

        # Set the color based on the number of days remaining
        if days_remaining < 0:
            color = RED
        elif days_remaining < 4:
            color = RED
        elif days_remaining < 7:
            color = ORANGE
        else:
            color = GREEN
        base = 70
        h = len(row[0])
        dd = base - h
        # Add the item to the listbox with the appropriate background color
        tasks_listbox.insert(END, "{:<{}} {:^0}".format(row[0],dd, row[1] ))
        tasks_listbox.itemconfig(END, bg=color)


    def double_click(event):
        selected_text = tasks_listbox.get(ANCHOR)
        if tasks_listbox.index(ANCHOR) == 0:
            return 0
        task_name, employee_name = selected_text.split()
        bbox = tasks_listbox.bbox(ANCHOR)
        if event.x < (bbox[0] + bbox[2]) / 2:
            open_task_window(task_name,employee_name)
        else:
            show(employee_name)

    tasks_listbox.bind('<Double-1>', double_click)
    running_tasks_window.focus_set()
    running_tasks_window.mainloop()


def open_task_window(task_name,employee_name):
    if task_name == "Name of the task              Name of the employee":
        return
    c = Database_teams.conn.cursor()
    c.execute("SELECT * FROM tasks WHERE name=? AND employee=? ", (task_name, employee_name))
    task = c.fetchone()
    c.close()

    # Create the main window
    window = customtkinter.CTk()
    window.title("View Task")

    # Create the task name label and entry field
    name_label = customtkinter.CTkLabel(window, text="Task Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
    name_entry = customtkinter.CTkEntry(window)
    name_entry.insert(0, task[0])
    name_entry.configure(state="readonly")
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

    # Create the task description label and text field
    description_label = customtkinter.CTkLabel(window, text="Task Description:")
    description_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
    description_entry = customtkinter.CTkTextbox(window, height=20, width=140)
    description_entry.insert(END, task[1])
    description_entry.configure(state="disabled")
    description_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

    # Create the task creation date label and date entry field
    creation_date_label = customtkinter.CTkLabel(window, text="Task Creation Date:")
    creation_date_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
    creation_date_str = task[2]
    creation_date = datetime.strptime(creation_date_str, '%d/%m/%Y').date()
    creation_date_entry = DateEntry(window, date_pattern='dd/mm/yyyy')
    creation_date_entry.set_date(creation_date)
    creation_date_entry.configure(state="disabled")
    creation_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

    # Create the task due date label and date entry field
    due_date_label = customtkinter.CTkLabel(window, text="Task Due Date:")
    due_date_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)

    due_date_str = task[3]
    due_date = datetime.strptime(due_date_str, '%d/%m/%Y').date()

    due_date_entry = DateEntry(window, date_pattern='dd/mm/yyyy')
    due_date_entry.set_date(due_date)
    due_date_entry.configure(state="disabled")
    due_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)


    # Create the task employee label and entry field
    employee_label = customtkinter.CTkLabel(window, text="Task Employee:")
    employee_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
    employee_entry = customtkinter.CTkEntry(window)
    employee_entry.insert(0, task[4])
    employee_entry.configure(state="disabled")
    employee_entry.grid(row=4, column=1, padx=5, pady=5, sticky=W)

    days_remaining = (due_date - date.today()).days
    day_label = customtkinter.CTkLabel(window, text="Days to finish: " + str(days_remaining))
    day_label.grid(row=5, column=1, padx=5, pady=5, sticky=W)
    if task[6] != '':
        pdf_label = customtkinter.CTkLabel(window, text="PDF:")
        pdf_label.grid(row=6, column=0, padx=5, pady=5, sticky=W)
        pdf_entry = customtkinter.CTkEntry(window,height=30, width=80)
        pdf_entry.insert(END, task[6])
        pdf_entry.configure(state="readonly")
        pdf_entry.grid(row=6, column=1, padx=5, pady=5, sticky=W)

        # Create the close button
        open_button = customtkinter.CTkButton(window, text="Open",height=30, width=80, command=lambda: show_pdf_file(pdf_entry.get()))
        open_button.grid(row=6, column=1, padx=(88, 0))

    # Create the close button
    close_button = customtkinter.CTkButton(window, text="Close",command= lambda: window.destroy())
    close_button.grid(row=7, column=1, padx=(0, 95), pady=5)


    window.mainloop()

