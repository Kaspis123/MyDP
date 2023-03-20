from tkinter import *
from tkinter.ttk import *
from tkcalendar import DateEntry
import Database_tasks
import InsideApp


def NewQ():

    # Create the main window
    window = Tk()
    window.title("Create Task")
    # Create the task name label and entry field
    name_label = Label(window, text="Task Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky=W)
    name_entry = Entry(window)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

    # Create the task description label and text field
    description_label = Label(window, text="Task Description:")
    description_label.grid(row=1, column=0, padx=5, pady=5, sticky=W)
    description_entry = Text(window, height=5, width=30)
    description_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

    creation_date_label = Label(window, text="Task Creation Date:")
    creation_date_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
    creation_date_entry = DateEntry(window)
    creation_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

    # Create the task due date label and date entry field
    due_date_label = Label(window, text="Task Due Date:")
    due_date_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
    due_date_entry = DateEntry(window)
    due_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

    # Create the task employee label and entry field
    employee_label = Label(window, text="Task Employee:")
    employee_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
    employee_entry = Entry(window)
    employee_entry.grid(row=4, column=1, padx=5, pady=5, sticky=W)

    task_name = name_entry.get()
    task_description = description_entry.get("1.0", END)
    task_creation_date = creation_date_entry.get()
    task_due_date = due_date_entry.get()
    task_employee = employee_entry.get()


    create_task_button = Button(window, text="Create Task", command=lambda: [Database_tasks.insert_task(name_entry.get(), description_entry.get("1.0", END), creation_date_entry.get(), due_date_entry.get(), employee_entry.get()), window.destroy(),InsideApp.InsideApp()])
    create_task_button.grid(row=5, column=1, padx=5, pady=5, sticky=E)




    # Start the main event loop
    window.mainloop()