from tkinter import ttk

from tkcalendar import DateEntry

import Database_teams
import Finished_Tasks

from tkinter import *
from tkinter.ttk import *
from datetime import  datetime

from Quests import show_pdf_file
import customtkinter


def Done():
    windowAPP = customtkinter.CTk()  # vytvořeni objektu
    windowAPP.title("Dokončené úkoly")  # Pojmenování aplikace

    window_width = 400
    window_height = 280
    screen_width = windowAPP.winfo_screenwidth()
    screen_height = windowAPP.winfo_screenheight()
    z = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    windowAPP.geometry(f"{window_width}x{window_height}+{z}+{y}")



    # Create a frame to hold the listbox and scrollbar
    # tasks_frame = customtkinter.CTkFrame(windowAPP)
    # tasks_frame.pack()

    # # Create the tasks listbox
    # tasks_listbox = Listbox(tasks_frame, height=10, width=50, font=("Helvetica", 14), bd=2, bg="#ffffff",
    #                         selectbackground="#cccccc", highlightthickness=0, justify="center")
    # tasks_listbox.pack(side="left", padx=10, pady=10, fill="both", expand=True)
    #
    # # Create the scrollbar
    # scrollbar = Scrollbar(tasks_frame, orient="vertical", command=tasks_listbox.yview)
    # scrollbar.pack(side="right", fill="y")
    #
    # # Configure the scrollbar to control the listbox
    # tasks_listbox.config(yscrollcommand=scrollbar.set)
    #
    #
    # tasks_listbox.delete(0, END)

    columns = ('last_name', 'email')

    tree = ttk.Treeview(windowAPP, columns=columns, show='headings')

    # define headings
    tree.heading('last_name', text='Name of the task')
    tree.heading('email', text='Finished by')

    # pack the treeview widget
    tree.pack()

    # Insert the current distinct script names from the database into the listbox
    for row in Finished_Tasks.conn.execute('SELECT name, employee FROM finished_tasks'):
        task_name = row[0]
        employee_name = row[1]
        item = tree.insert("", "end", text="", values=(task_name, employee_name))
        tree.item(item, tags=("myfont",))
    #     tasks_listbox.insert(END, row[0])
    #
    def treeview_double_click(event):
        item = tree.item(tree.selection())
        column = tree.identify_column(event.x)

        if column == '#1':  # First column (Name of the Task) was clicked
            task_name = item['values'][0]
            open(task_name)

            # Do something with the employee name
    tree.bind('<Double-1>', treeview_double_click)
    tree.column("email", anchor="center")
    tree.tag_configure("myfont", font=("Helvetica", 12))
    close_button = customtkinter.CTkButton(windowAPP, text="Close", command=windowAPP.destroy)
    close_button.pack(padx=10, pady=10)
    windowAPP.mainloop()

def open(event):
    # Retrieve task information from database)
    c = Finished_Tasks.conn.cursor()
    c.execute("SELECT * FROM finished_tasks WHERE name=?", (event,))
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
    description_entry = customtkinter.CTkTextbox(window, height=5, width=140)
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

    finished_date_label = customtkinter.CTkLabel(window, text="Task Finished Date:")
    finished_date_label.grid(row=5, column=0, padx=5, pady=5, sticky=W)
    finished_date_str = task[5]
    finished_date = datetime.strptime(finished_date_str, '%d/%m/%Y').date()
    finished_date_entry = DateEntry(window, date_pattern='dd/mm/yyyy')
    finished_date_entry.set_date(finished_date)
    finished_date_entry.configure(state="disabled")
    finished_date_entry.grid(row=5, column=1, padx=5, pady=5, sticky=W)
    if task[6] != '':
        pdf_label = customtkinter.CTkLabel(window, text="PDF:")
        pdf_label.grid(row=6, column=0, padx=5, pady=5, sticky=W)
        pdf_entry = customtkinter.CTkEntry(window,width=85)
        pdf_entry.insert(END, task[6])
        pdf_entry.configure(state="readonly")
        pdf_entry.grid(row=6, column=1, padx=5, pady=5, sticky=W)

        # Create the close button
        open_button = customtkinter.CTkButton(window, text="Open",width=60, command=lambda: show_pdf_file(pdf_entry.get()))
        open_button.grid(row=6, column=1, padx=(88, 0))

    # Create the close button
    close_button = customtkinter.CTkButton(window, text="Close", command=window.destroy)
    close_button.grid(row=7, column=1, padx=(0, 88), pady=5, sticky=E)
    x = Database_teams.getinfoabouattack(event)
    if x !=0:
        windowdata = customtkinter.CTkToplevel(window)
        windowdata.title("Informace o útoku")
        text = customtkinter.CTkTextbox(windowdata, width=500, height=300)
        text.pack()
        text.insert(INSERT, x)



    # Make the window modal
    window.mainloop()


