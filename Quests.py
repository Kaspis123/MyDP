

from tkinter import *

from datetime import datetime
from tkcalendar import DateEntry
from datetime import date
from tkPDFViewer import tkPDFViewer as pdf

import Database_teams
import Finished_Tasks
import customtkinter

def show(name1):
    # Create the tasks window
    RED = "#FF3333"
    ORANGE = "#FFA500"
    GREEN = "#33FF33"
    customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    tasks_window = customtkinter.CTk()
    tasks_window.title("My Tasks")



    # Create the tasks listbox
    tasks_listbox = Listbox(tasks_window, height=10, width=50, font=("Helvetica", 14), bd=2, bg="#ffffff", selectbackground="#cccccc", highlightthickness=0,justify="center")
    tasks_listbox.pack(padx=10, pady=10)

    close_button = customtkinter.CTkButton(tasks_window, text="Close", command=lambda: tasks_window.destroy())
    close_button.pack(padx=10, pady=10)

    def getlistbox():
        tasks_listbox.delete(0, END)

        # Insert default value
        tasks_listbox.insert(END, "Name")
        for row in Database_teams.conn.execute(
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
            popup_menu.add_command(label="Mark as Finished", command= lambda: [mark_as_finished(selected_item,name1),getlistbox()])
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
    c = Database_teams.conn.cursor()
    c.execute("SELECT * FROM tasks WHERE name=?", (task_name,))
    task = c.fetchone()
    c.close()
    customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
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

    # # Create the task creation date label and date entry field
    # creation_date_label = Label(window, text="Task Creation Date:")
    # creation_date_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)
    # creation_date_entry = DateEntry(window)
    # creation_date_entry.insert(0, task[2])
    # creation_date_entry.configure(state="disabled")
    # creation_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

    # Create the task due date label and date entry field
    due_date_label = customtkinter.CTkLabel(window, text="Task Due Date:")
    due_date_label.grid(row=2, column=0, padx=5, pady=5, sticky=W)

    due_date_str = task[3]
    due_date = datetime.strptime(due_date_str, '%d/%m/%Y').date()

    due_date_entry = DateEntry(window, date_pattern='dd/mm/yyyy')
    due_date_entry.set_date(due_date)
    due_date_entry.configure(state="disabled")
    due_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)

    days_remaining = (due_date - date.today()).days
    day_label = customtkinter.CTkLabel(window, text="Days to finish: " + str(days_remaining))
    day_label.grid(row=3, column=1, padx=5, pady=5, sticky=W)

    # Create the task employee label and entry field
    # employee_label = Label(window, text="Task Employee:")
    # employee_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
    # employee_entry = Entry(window)
    # employee_entry.insert(0, task[4])
    # employee_entry.configure(state="disabled")
    # employee_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)
    if task[6] != '':

        pdf_label = customtkinter.CTkLabel(window, text="PDF:")
        pdf_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
        pdf_entry = customtkinter.CTkEntry(window,height=30, width=80)

        pdf_entry.insert(END, task[6])
        pdf_entry.configure(state="readonly")
        pdf_entry.grid(row=4, column=1, padx=5, pady=5, sticky=W)

        # Create the close button
        open_button = customtkinter.CTkButton(window,text="Open",height=30, width=80, command=lambda: show_pdf_file(pdf_entry.get()))
        open_button.grid(row=4, column=1, padx=(88, 0))
    close_button = customtkinter.CTkButton(window, text="Close", command=lambda: window.destroy())
    close_button.grid(row=5, column=1, padx=(5, 88), pady=5, )

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






def show_pdf_file(entry):
    new_window = Toplevel()
    new_window.resizable(True, True)
    new_window.title("PDF File")
    window_width = 600
    window_height = 600
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    file_path = "pdf_files/" + entry
    if file_path:
        v1 = pdf.ShowPdf()
        v2 = v1.pdf_view(new_window, pdf_location=open(file_path, "r"))
        v2.pack()
def mark_as_finished(event,name1):
    current_date = date.today()
    formatted_date = current_date.strftime("%d/%m/%Y")
    c = Database_teams.conn.cursor()
    c.execute("SELECT * FROM tasks WHERE name=? AND employee=?", (event, name1))
    task = c.fetchone()
    Finished_Tasks.insert_task(task[0], task[1], task[2], task[3], task[4], formatted_date, task[6])
    c.close()
    Database_teams.delete_task(event)









