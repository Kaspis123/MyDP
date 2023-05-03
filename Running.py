
from tkinter import *

from datetime import datetime
from tkcalendar import DateEntry
from datetime import date

import Database_teams
from Quests import show, show_pdf_file
import customtkinter
from tkinter import ttk


def Running():
    # Create the tasks window
    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

    running_tasks_window= customtkinter.CTk()
    running_tasks_window.title("Currently Running Tasks")
    window_width = 400
    window_height = 280
    screen_width = running_tasks_window.winfo_screenwidth()
    screen_height = running_tasks_window.winfo_screenheight()
    z = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    running_tasks_window.geometry(f"{window_width}x{window_height}+{z}+{y}")


    # scrollbar = Scrollbar(running_tasks_window, orient="vertical")
    # scrollbar.pack(side="right", fill="y")
    # # Create the tasks listbox
    # tasks_listbox = Listbox(running_tasks_window, height=10, width=50, font=("Helvetica", 14), bd=2, bg="#ffffff",
    #                         selectbackground="#cccccc", highlightthickness=0,yscrollcommand=scrollbar.set)
    # tasks_listbox.pack(padx=10, pady=10)
    # scrollbar.config(command=tasks_listbox.yview)




    columns = ('last_name', 'email')

    tree = ttk.Treeview(running_tasks_window, columns=columns, show='headings')

    # define headings

    tree.heading('last_name', text='Name of the task')
    tree.heading('email', text='Name of the employee')

    # pack the treeview widget
    tree.pack()

    close_button = customtkinter.CTkButton(running_tasks_window, text="Close", command=running_tasks_window.destroy)
    close_button.pack(padx=10, pady=10)
    for row in Database_teams.conn.execute('SELECT name, employee, due_date FROM tasks ORDER BY due_date '):
        task_name = row[0]
        employee_name = row[1]
        due_date_str = row[2]

        # Convert the due date string to a datetime object
        due_date = datetime.strptime(due_date_str, '%d/%m/%Y').date()
        days_remaining = (due_date - date.today()).days

        # Insert the record into the treeview
        item = tree.insert("", "end", text="", values=(task_name, employee_name, due_date_str))


        # Change the background color of the row if the due date is within 3 days
        if days_remaining < 0:
            tree.item(item, tags=("overdue","myfont"))
        elif days_remaining < 4:
                tree.item(item, tags=("overdue","myfont"))
        elif days_remaining < 7:
                tree.item(item, tags=("slightly","myfont"))
        else:
            tree.item(item, tags=("normal","myfont"))


# Define the tags for the row colors
    tree.column("email", anchor="center")

    tree.tag_configure("overdue", background="red")
    tree.tag_configure("slightly", background="orange")
    tree.tag_configure("normal", background="green")
    tree.tag_configure("myfont", font=("Helvetica", 12))

    def treeview_double_click(event):
        item = tree.item(tree.selection())
        column = tree.identify_column(event.x)

        if column == '#1':  # First column (Name of the Task) was clicked
            task_name = item['values'][0]
            open_task_window(task_name, item['values'][1])
        elif column == '#2':  # Second column (Name of the Employee) was clicked
            employee_name = item['values'][1]
            show(employee_name)
            # Do something with the employee name
    tree.bind('<Double-1>', treeview_double_click)

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
    window.resizable(False,False)

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
    description_entry = customtkinter.CTkTextbox(window, height=80, width=140)
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
    def displayrows():
        rows = Database_teams.smlouvaread(task[0])
        print(rows)

        for row in rows:
            if row[2] !=" ":
                t.insert('end', str(row[2]) + '\n\n')
            if row[3] !=" ":
                t.insert('end', str(row[3]) + '\n\n')
            if row[4] !=" ":
                t.insert('end', str(row[4]) + '\n\n')
            if row[5] !=" ":
                t.insert('end', str(row[5]) + '\n\n')

    windowsmlouva = customtkinter.CTkToplevel(window)
    windowsmlouva.title("Smlouva")
    window_width = 420
    window_height = 350
    screen_width = windowsmlouva.winfo_screenwidth()
    screen_height = windowsmlouva.winfo_screenheight()
    z = int((screen_width / 2) - (window_width / 2) + 60)
    y = int((screen_height / 2) - (window_height / 2) + 60)
    windowsmlouva.geometry(f"{window_width}x{window_height}+{z}+{y}")

    t = customtkinter.CTkTextbox(windowsmlouva,width=420,height=350)
    t.pack()

    displayrows()


    window.mainloop()

