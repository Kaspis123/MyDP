
import shutil
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkcalendar import DateEntry
import Database_tasks
import Database_teams
import Database_users
from datetime import date
global x
import tkinter as tk
from tkinter import filedialog
import os


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
    creation_date_entry = Entry(window)
    creation_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky=W)
    current_date = date.today()
    formatted_date = current_date.strftime("%d/%m/%Y")
    creation_date_entry.insert(0, formatted_date)  # the index of the entry is 0, not formatted_date

    # Create the task due date label and date entry field
    due_date_label = Label(window, text="Task Due Date:")
    due_date_label.grid(row=3, column=0, padx=5, pady=5, sticky=W)
    due_date_entry = DateEntry(window, date_pattern='dd/mm/yyyy')
    due_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)

    # Create the task employee label and entry field
    employee_label = Label(window, text="Task Employee:")
    employee_label.grid(row=4, column=0, padx=5, pady=5, sticky=W)
    employee_entry = Entry(window)
    employee_entry.grid(row=4, column=1, padx=5, pady=5, sticky=W)

    pdf_label = Label(window, text="PDF:")
    pdf_label.grid(row=5,column=0, padx=5, pady=5, sticky=W)
    pdf_entry = Entry(window)
    pdf_entry.grid(row=5, column=1, padx=5, pady=5, sticky=W)

    button = Button(window, text="Open PDF File", command=lambda :[open_file_dialog(pdf_entry, window)])
    button.grid(row=5, column=1, padx=(92, 0))

    create_employee_button = Button(window,text="Choose",command=lambda: [choose_user(employee_entry)] )
    create_employee_button.grid(row=4, column=1, padx=(88, 0))
    global x
    x = 0
    create_task_button = Button(window, text="Create Task", command=lambda: [give_to_database(name_entry.get(), description_entry.get("1.0", END), creation_date_entry.get(), due_date_entry.get(), employee_entry.get(), window,x,pdf_entry.get())])
    create_task_button.grid(row=6, column=1, padx=(0, 88), pady=5)
    label = tk.Label(window)
    label.grid(row=7, column=1, padx=5, pady=5, sticky=E)
    window.mainloop()

def open_file_dialog(pdf_entry,window):
    file_path = tk.filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])
    pdf_name = os.path.basename(file_path)
    pdf_entry.insert(0, pdf_name)
    dest_dir = "pdf_files/"

    # create the destination directory if it does not exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # copy the file to the destination directory
    shutil.copy2(file_path, os.path.join(dest_dir, pdf_name))
    window.lift()

    # new_window = Toplevel()
    # new_window.resizable(False, False)
    # new_window.title("User Database")
    # window_width = 500
    # window_height = 500
    # screen_width = new_window.winfo_screenwidth()
    # screen_height = new_window.winfo_screenheight()
    # x = int((screen_width / 2) - (window_width / 2))
    # y = int((screen_height / 2) - (window_height / 2))
    # new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    # file_path = tk.filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])
    # print(file_path)
    # if file_path:
    #     v1 = pdf.ShowPdf()
    #     v2= v1.pdf_view(new_window,pdf_location=open(file_path,"r"))
    #     v2.pack()






def error_task_name():
    messagebox.showerror('Error', 'Error: Name of the task is already in database!')

def error_user_name():
    messagebox.showerror('Error', 'Error: User does not exists!')

def give_to_database(name_entry, description_entry, creation_date_entry, due_date_entry, employee_entry, window, x, pdf):
    if x == 0:
        p = Database_tasks.insert_task(name_entry, description_entry, creation_date_entry, due_date_entry, employee_entry, pdf)
        window.lift()
        if p != 0 and p != 1:
            window.destroy()
    else:
        Database_tasks.add_task_for_team(employee_entry, name_entry, creation_date_entry, description_entry, due_date_entry, pdf)
        window.destroy()

def switch_to_teams(listbox):
    global x
    x = + 1
    if x > 1:
        x = 1
    listbox.delete(0, END)
    listbox.insert(END, "{:<30} {:^30}".format("ID", "Teams"))
    cur = Database_teams.conn.cursor()
    cur.execute("Select team_name, team_id from TEAMS")
    rows = cur.fetchall()
    for row in rows:
        listbox.insert(END, "{:<30} {:^30}".format(row[1], row[0]))
def switch_to_users(listbox):
    global x
    if x != 0:
        x = 0
    listbox.delete(0, END)
    listbox.insert(END, "{:<30} {:^30}".format("ID", "Name"))
    for row in Database_users.conn.execute('SELECT id, name FROM users'):
        listbox.insert(END, "{:<30} {:^30}".format(row[0], row[1]))


def choose_user(employee_entry):
    new_window = Toplevel()
    new_window.resizable(False, False)
    new_window.title("User Database")
    window_width = 500
    window_height = 500
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    listbox = Listbox(new_window, height=10, width=50, font=("Helvetica", 14), bd=2, bg="#ffffff",
                            selectbackground="#cccccc", highlightthickness=0)
    listbox.pack(padx=10, pady=10)


    listbox.delete(0, END)
    listbox.insert(END, "{:<30} {:^30}".format("ID", "Name"))
    close_button = Button(new_window, text="Close", command=new_window.destroy)
    close_button.pack()
    switch_button = Button(new_window, text="Teams", command=lambda: [switch_to_teams(listbox)])
    switch_button.pack()
    switch_button_users = Button(new_window, text="Users", command=lambda: [switch_to_users(listbox)])
    switch_button_users.pack()
    for row in Database_users.conn.execute('SELECT id, name FROM users'):
        listbox.insert(END, "{:<30} {:^30}".format(row[0], row[1]))

    def double_click(event):
        employee_entry.delete(0, END)
        selected_text = listbox.get(ANCHOR)
        if listbox.index(ANCHOR) == 0:
            return 0
        ID, name = selected_text.split()
        bbox = listbox.bbox(ANCHOR)
        if event.x < (bbox[0] + bbox[2]) / 2:
            employee_entry.insert(0, name)
            new_window.destroy()
        else:
            employee_entry.insert(0, name)
            new_window.destroy()


    listbox.bind('<Double-1>', lambda event: [double_click(event)])

