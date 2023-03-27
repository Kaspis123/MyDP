
import Database_tasks
from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry
from datetime import date

import Finished_Tasks


def show(name1):
    # Create the tasks window
    RED = "#FF3333"
    ORANGE = "#FFA500"
    GREEN = "#33FF33"
    tasks_window = Tk()
    tasks_window.title("My Tasks")

    # Create the tasks label
    tasks_label = Label(tasks_window, text="My Tasks", font=("Arial", 24, "bold"), fg="#333333", bg="#f2f2f2", padx=20, pady=20)
    tasks_label.pack(padx=10, pady=10)

    # Create the tasks listbox
    tasks_listbox = Listbox(tasks_window, height=10, width=50, font=("Helvetica", 14), bd=2, bg="#ffffff", selectbackground="#cccccc", highlightthickness=0,justify="center")
    tasks_listbox.pack(padx=10, pady=10)

    close_button = Button(tasks_window, text="Close", command=tasks_window.destroy)
    close_button.pack(padx=10, pady=10)

    def getlistbox():
        tasks_listbox.delete(0, END)

        # Insert default value
        tasks_listbox.insert(END, "Name")
        for row in Database_tasks.conn.execute(
                'SELECT name, due_date FROM tasks WHERE employee=? ORDER BY due_date ',
                (name1,)):
            # Parse the due date from the database row
            due_date_str = row[1]
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

            # Add the item to the listbox with the appropriate background color
            tasks_listbox.insert(END, row[0])
            tasks_listbox.itemconfig(END, bg=color)
    getlistbox()



    def pop(event):
        # Get the selected item from the listbox

        selection = event.widget.curselection()

        if selection:
            selected_item = event.widget.get(selection[0])
            if selected_item == "Name":
                return

            # Create a popup menu with the option to delete the selected image
            popup_menu = Menu(tasks_window, tearoff=0)
            popup_menu.add_command(label="Mark as Finished", command= lambda: [mark_as_finished(selected_item),getlistbox()])
            popup_menu.add_command(label="Show", command=lambda event=event: open_task_window(tasks_listbox.get(ANCHOR)))

            # Display the popup menu at the mouse position
            try:
                popup_menu.tk_popup(event.x_root, event.y_root, 0)
            finally:
                popup_menu.grab_release()

    tasks_listbox.bind("<Button-3>", pop)
    tasks_listbox.bind('<Double-1>', lambda event: open_task_window(tasks_listbox.get(ANCHOR)))
    tasks_window.mainloop()

def open_task_window(task_name):
    if task_name == "Name":
        return
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

    # # Create the task creation date label and date entry field
    # creation_date_label = Label(window, text="Task Creation Date:")
    # creation_date_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
    # creation_date_entry = DateEntry(window)
    # creation_date_entry.insert(0, task[2])
    # creation_date_entry.configure(state="disabled")
    # creation_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

    # Create the task due date label and date entry field
    due_date_label = Label(window, text="Task Due Date:")
    due_date_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)

    due_date_str = task[3]
    due_date = datetime.strptime(due_date_str, '%d/%m/%Y').date()

    due_date_entry = DateEntry(window, date_pattern='dd/mm/yyyy')
    due_date_entry.set_date(due_date)
    due_date_entry.configure(state="disabled")
    due_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

    days_remaining = (due_date - date.today()).days
    day_label = Label(window, text="Days to finish: " + str(days_remaining))
    day_label.grid(row=3, column=1, padx=5, pady=5, sticky=W)



    # Create the task employee label and entry field
    # employee_label = Label(window, text="Task Employee:")
    # employee_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
    # employee_entry = Entry(window)
    # employee_entry.insert(0, task[4])
    # employee_entry.configure(state="disabled")
    # employee_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

    # Create the close button
    close_button = Button(window, text="Close", command=window.destroy)
    close_button.grid(row=3, column=1, padx=5, pady=5, sticky=E)

    # Make the window modal
    window.focus_set()
    window.grab_set()
    window.wait_window()

def mark_as_finished(event):
    current_date = date.today()
    formatted_date = current_date.strftime("%d/%m/%Y")
    c = Database_tasks.conn.cursor()
    c.execute("SELECT * FROM tasks WHERE name=?", (event,))
    task = c.fetchone()
    Finished_Tasks.insert_task(task[0],task[1],task[2],task[3],task[4],formatted_date)
    c.close()
    Database_tasks.delete_task(event)








