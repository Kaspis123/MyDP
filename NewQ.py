
import shutil
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.ttk import *
from tkcalendar import DateEntry
import Database_teams
from datetime import date
global x
import tkinter as tk
from tkinter import filedialog
import os
import customtkinter
var1 = " "
var2 = " "
var3 = " "
var4 = " "


def NewQ():
    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    # Create the main window
    window = customtkinter.CTk()
    window_width = 500
    window_height = 330
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    z = int((screen_width / 2) - (window_width / 2) + 60)
    y = int((screen_height / 2) - (window_height / 2) + 60)
    window.geometry(f"{window_width}x{window_height}+{z}+{y}")
    window.title("Create Task")


    # Create the task name label and entry field
    name_label = customtkinter.CTkLabel(window, text="Task Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    name_entry = customtkinter.CTkEntry(window)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    # Create the task description label and text field
    description_label = customtkinter.CTkLabel(window, text="Task Description:")
    description_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    description_entry = customtkinter.CTkTextbox(window, height=80, width=140)
    description_entry.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    creation_date_label = customtkinter.CTkLabel(window, text="Task Creation Date:")
    creation_date_label.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
    creation_date_entry = customtkinter.CTkEntry(window)
    creation_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
    current_date = date.today()
    formatted_date = current_date.strftime("%d/%m/%Y")
    creation_date_entry.insert(0, formatted_date)  # the index of the entry is 0, not formatted_date

    # Create the task due date label and date entry field
    due_date_label = customtkinter.CTkLabel(window, text="Task Due Date:")
    due_date_label.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
    due_date_entry = DateEntry(window, date_pattern='dd/mm/yyyy')
    due_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

    # Create the task employee label and entry field
    employee_label = customtkinter.CTkLabel(window, text="Task Employee:")
    employee_label.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")
    employee_entry = customtkinter.CTkEntry(window, width=85)
    employee_entry.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

    pdf_label = customtkinter.CTkLabel(window, text="PDF:",)
    pdf_label.grid(row=5,column=0, padx=5, pady=5, sticky="nsew")
    pdf_entry = customtkinter.CTkEntry(window, width=85,)
    pdf_entry.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

    button = customtkinter.CTkButton(window, text="Open PDF File", width=60,
                                 height=30, command=lambda: open_file_dialog(pdf_entry, window))
    button.grid(row=5, column=2, sticky="nsew")

    create_employee_button = customtkinter.CTkButton(window,text="Choose",width=90,
                                 height=30,command=lambda: choose_user(employee_entry))
    create_employee_button.grid(row=4, column=2, sticky="nsew")
    global x
    x = 0
    create_task_button = customtkinter.CTkButton(window, text="Create Task", width=120,
                                 height=32, command=lambda: give_to_database(name_entry.get(), description_entry.get("1.0", END), creation_date_entry.get(), due_date_entry.get(), employee_entry.get(), window,x,pdf_entry.get()))
    create_task_button.grid(row=6, column=1, pady=5, sticky="nsew")
    # label = tk.Label(window)
    # label.grid(row=7, column=1, padx=5, pady=5, sticky=E)

    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.rowconfigure(2, weight=1)
    window.rowconfigure(3, weight=1)
    window.rowconfigure(4, weight=1)
    window.rowconfigure(5, weight=1)
    window.rowconfigure(6, weight=1)
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)

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
    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    windowforsmouvy =  customtkinter.CTkToplevel()
    windowforsmouvy.title("Smlouva")
    window_width = 310
    window_height = 310
    screen_width = windowforsmouvy.winfo_screenwidth()
    screen_height = windowforsmouvy.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2) + 60)
    y = int((screen_height / 2) - (window_height / 2) + 60)
    windowforsmouvy.geometry(f"{window_width}x{window_height}+{x}+{y}")
    import tkinter
    check_var = tkinter.StringVar()
    check_var2 = tkinter.StringVar()
    check_var3 = tkinter.StringVar()
    check_var4 = tkinter.StringVar()
    text_var = tkinter.StringVar(value="Prosím zaškrtněte všechny políčka, které vyplívají ze "
                                       "smlouvy o dílo a doplňte případné informace.")
    label = customtkinter.CTkLabel(master=windowforsmouvy,
                                   textvariable=text_var,
                                   width=120,
                                   height=25,
                                   fg_color=("#d7d6d7", "#323332"),
                                   corner_radius=8, wraplength=200, justify="center")
    label.pack(padx=20, pady=10, anchor="center")
    windowforsmouvy.lift()

    def checkbox_event():
        windowcheck=customtkinter.CTkToplevel()
        windowcheck.title("Paragraf")
        windowcheck.resizable(False, False)
        windowcheck.attributes("-topmost", True)
        window_width1 = 200
        window_height1 = 110
        screen_width = windowcheck.winfo_screenwidth()
        screen_height = windowcheck.winfo_screenheight()
        x = int((screen_width / 2) - (window_width1 / 2))
        y = int((screen_height / 2) - (window_height1 / 2))
        windowcheck.geometry(f"{window_width1}x{window_height1}+{x}+{y}")
        textbox = customtkinter.CTkTextbox(windowcheck, height=80, width=200)
        textbox.grid(row=0, column=0)

        textbox.insert("0.0", "Je možné na zaměstnancích provádět testování takovýmto způsobem?")
        button = customtkinter.CTkButton(windowcheck,text="Close", command=lambda: getdatafromcheckbox1(textbox.get("1.0", END), windowcheck)).grid(row=1,column = 0)

        windowcheck.mainloop()
    def checkbox_event2():
        windowcheck=customtkinter.CTkToplevel()
        windowcheck.title("Paragraf")
        windowcheck.resizable(False, False)
        windowcheck.attributes("-topmost", True)
        window_width1 = 200
        window_height1 = 110
        screen_width = windowcheck.winfo_screenwidth()
        screen_height = windowcheck.winfo_screenheight()
        x = int((screen_width / 2) - (window_width1 / 2))
        y = int((screen_height / 2) - (window_height1 / 2))
        windowcheck.geometry(f"{window_width1}x{window_height1}+{x}+{y}")
        textbox = customtkinter.CTkTextbox(windowcheck, height=80, width=200)
        textbox.grid(row=0, column=0)

        textbox.insert("0.0", "Vyplývá ze smlouvy, že je možné překonávat zabezpečení?")
        button = customtkinter.CTkButton(windowcheck,text="Close", command=lambda: getdatafromcheckbox2(textbox.get("1.0", END), windowcheck)).grid(row=1,column = 0)

        windowcheck.mainloop()
    def checkbox_event3():
        windowcheck=customtkinter.CTkToplevel()
        windowcheck.title("Paragraf")
        windowcheck.resizable(False, False)
        windowcheck.attributes("-topmost", True)
        window_width1 = 200
        window_height1 = 110
        screen_width = windowcheck.winfo_screenwidth()
        screen_height = windowcheck.winfo_screenheight()
        x = int((screen_width / 2) - (window_width1 / 2))
        y = int((screen_height / 2) - (window_height1 / 2))
        windowcheck.geometry(f"{window_width1}x{window_height1}+{x}+{y}")
        textbox = customtkinter.CTkTextbox(windowcheck, height=80, width=200)
        textbox.grid(row=0, column=0)

        textbox.insert("0.0", "Jak bude nakládáno s hesly??")
        button = customtkinter.CTkButton(windowcheck,text="Close", command=lambda: getdatafromcheckbox3(textbox.get("1.0", END), windowcheck)).grid(row=1,column = 0)

        windowcheck.mainloop()
    def checkbox_event4():
        windowcheck = customtkinter.CTkToplevel()
        windowcheck.title("Paragraf")
        windowcheck.resizable(False, False)
        windowcheck.attributes("-topmost", True)
        window_width1 = 200
        window_height1 = 110
        screen_width = windowcheck.winfo_screenwidth()
        screen_height = windowcheck.winfo_screenheight()
        x = int((screen_width / 2) - (window_width1 / 2))
        y = int((screen_height / 2) - (window_height1 / 2))
        windowcheck.geometry(f"{window_width1}x{window_height1}+{x}+{y}")
        textbox = customtkinter.CTkTextbox(windowcheck, height=80, width=200)
        textbox.grid(row=0, column=0)
        textbox.insert("0.0", "Jak budou zabezpečena získaná data?")
        button = customtkinter.CTkButton(windowcheck, text="Close", command=lambda: getdatafromcheckbox4(textbox.get("1.0", END), windowcheck)).grid(row=1, column = 0)

    checkbox = customtkinter.CTkCheckBox(master=windowforsmouvy, text="209 Podvod", command=checkbox_event,
                                         variable=check_var, onvalue="on", offvalue="off")
    checkbox.pack(padx=20, pady=10, anchor="w")
    checkbox2 = customtkinter.CTkCheckBox(master=windowforsmouvy, text="230 Neoprávněný přístup", command=checkbox_event2,
                                         variable=check_var2, onvalue="on", offvalue="off")
    checkbox3 = customtkinter.CTkCheckBox(master=windowforsmouvy, text="231 Opatření hesla", command=checkbox_event3,
                                         variable=check_var3, onvalue="on", offvalue="off")
    checkbox4 = customtkinter.CTkCheckBox(master=windowforsmouvy, text="182 Porušení tajemství", command=checkbox_event4,
                                         variable=check_var4, onvalue="on", offvalue="off")
    checkbox2.pack(padx=20, pady=10, anchor="w")
    checkbox3.pack(padx=20, pady=10, anchor="w")
    checkbox4.pack(padx=20, pady=10, anchor="w")

    closebutton=customtkinter.CTkButton(windowforsmouvy, text="Close",command=lambda: windowforsmouvy.destroy()).pack(padx=20, pady=10, anchor="center")
    windowforsmouvy.mainloop()
    window.lift()

def error_task_name():
    messagebox.showerror('Error', 'Error: Name of the task is already in database!')

def error_user_name():
    messagebox.showerror('Error', 'Error: User does not exists!')

def give_to_database(name_entry, description_entry, creation_date_entry, due_date_entry, employee_entry, window, x, pdf):
    if x == 0:
        p = Database_teams.insert_task(name_entry, description_entry, creation_date_entry, due_date_entry, employee_entry, pdf)
        printa(name_entry)
        window.lift()
        if p != 0 and p != 1:

            window.destroy()

    else:
        Database_teams.add_task_for_team(employee_entry, name_entry, creation_date_entry, description_entry, due_date_entry, pdf)
        printa(name_entry)

        window.destroy()
def getdatafromcheckbox1(text,window1):
    global var1
    var1 = text
    window1.destroy()


def getdatafromcheckbox2(text, window2):
    global var2
    var2 = text
    window2.destroy()

def getdatafromcheckbox3(text,window3):
    global var3
    var3 = text
    window3.destroy()

def getdatafromcheckbox4(text,window4):
    global var4
    var4 = text
    window4.destroy()

def printa(name):
    global var1, var2, var3, var4
    Database_teams.smlouvainsert(name,var1,var2,var3,var4)
    var1 = var2 = var3 = var4 = ' '





def switch_to_teams(tree,window):
    window.title("Teams Database")
    global x
    x = + 1
    if x > 1:
        x = 1
    for i in tree.get_children():
        tree.delete(i)

    cur = Database_teams.conn.cursor()
    cur.execute("Select team_name, team_id from TEAMS")
    rows = cur.fetchall()
    for row in rows:
        task_name = row[0]
        item = tree.insert("", "end", text="", values=(task_name))
def switch_to_users(tree,window):
    window.title("Users Database")
    global x
    if x != 0:
        x = 0
    for i in tree.get_children():
        tree.delete(i)

    for row in Database_teams.conn.execute('SELECT id, name FROM members'):
        task_name = row[1]
        item = tree.insert("", "end", text="", values=(task_name))


def choose_user(employee_entry):
    new_window = customtkinter.CTkToplevel()
    new_window.resizable(False, False)
    new_window.title("User Database")
    window_width = 500
    window_height = 275
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    columns = ('last_name')
    style = ttk.Style(new_window)
    # set ttk theme to "clam" which support the fieldbackground option
    style.theme_use("clam")
    style.configure("Treeview", background="#323332",
                    fieldbackground="#323332", foreground="#d7d6d7")

    tree = ttk.Treeview(new_window, style="Treeview", columns=columns, show='headings')


    # define headings
    tree.heading('last_name', text='Name')


    # pack the treeview widget
    tree.grid(row = 1,column=1)
    tree.column("# 1", anchor=CENTER, stretch=YES, width=500)
    tree.grid_columnconfigure(0, weight=5)


    close_button = customtkinter.CTkButton(new_window, text="Close", command=new_window.destroy)
    close_button.grid(row=5,column = 1,sticky = "w")
    switch_button = customtkinter.CTkButton(new_window, text="Teams", command=lambda: switch_to_teams(tree, new_window))
    switch_button.grid(row=5,column = 1)
    switch_button_users = customtkinter.CTkButton(new_window, text="Users", command=lambda: switch_to_users(tree, new_window))
    switch_button_users.grid(row=5,column = 1,sticky = "e")
    for row in Database_teams.conn.execute('SELECT id, name FROM members'):
        task_name = row[1]
        item = tree.insert("", "end", text="", values=(task_name))

    tree.column("last_name", anchor="center")

    def double_click(event):
        employee_entry.delete(0, END)
        try:
            item = tree.item(tree.selection())
            task_name = item['values'][0]
            employee_entry.insert(0, task_name)
            new_window.destroy()
        except:
            print()


    tree.bind('<Double-1>', lambda event: [double_click(event)])

