import tkinter as tk
from tkinter import messagebox

from PIL import ImageTk
from tkinter import *
from tkinter.ttk import *
import Database
import InsideApp
import DatabaseForScripts
number = 1

def Test():
    global number
    window = tk.Tk()  # vytvořeni objektu
    window_width = 800
    window_height = 800
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    # Nastavení velikosti okna aplikace
    window.title("Management")  # Pojmenování aplikace
    window.resizable(False, False)

    image = PhotoImage(file="arrow.jpg")
    btn = Button(window, image=image, command=lambda: [window.destroy(), Back()])
    btn.image = image
    btn.grid(row=0, column=0)

    lbl_search = Label(window, text='Name of the Script', font=('bold', 12))
    lbl_search.grid(row=0, column=3, padx=(100, 0), pady=(10, 0))

    hostname_search = StringVar()
    hostname_search_entry = Entry(window, textvariable=hostname_search)
    hostname_search_entry.grid(row=1, column=3, pady=(0, 10))

    bt1 = tk.Button(window, text="Chose by name", fg="red",
                    command=lambda: [initialize(window, hostname_search_entry.get())])
    bt1.grid(row=2, column=2, padx=(10, 0), pady=(0, 10))

    bt2 = tk.Button(window, text="Search by name", fg="black")
    bt2.grid(row=2, column=3, padx=(10, 100), pady=(0, 10))
    # b2 = Button(window, text="Delete Script", command=lambda: [deleteScript(hostname_search.get(),bar_tree_view)])
    # b2.grid(row=3, column=4, sticky=W)
    # frame_bar = Frame(window)
    # frame_bar.grid(row=20, column=0, columnspan=4, rowspan=6, pady=20, padx=20)
    #
    # columns = ['Name']  # Remove 'id' from the list of columns
    # bar_tree_view = Treeview(frame_bar, columns=columns, show="headings")
    # for col in columns:
    #     bar_tree_view.column(col, width=120)
    #     bar_tree_view.heading(col, text=col)
    # bar_tree_view.bind('<<TreeviewSelect>>', )
    # bar_tree_view.pack(side="left", anchor="center", fill="y")
    # scrollbar = Scrollbar(frame_bar, orient='vertical')
    # scrollbar.configure(command=bar_tree_view.yview)
    # scrollbar.pack(side="right", fill="y")
    # bar_tree_view.config(yscrollcommand=scrollbar.set)
    # frame_btns = Frame(window)
    # frame_btns.grid(row=3, column=0)
    #
    # populate_list(bar_tree_view, )
def initialize(window,name):
    T = tk.Text(window, height=10, width=40)
    T.grid(row=5, column=3)
    x = Database.databaseforscriptsread(name,number)
    T.insert(INSERT, x)
    btn3 = tk.Button(window,text='Back',fg='black', command= lambda: [backbutton(T, name)]).grid(row=6,column=6)
    btn1 = tk.Button(window, text="Pozitivni", fg="green",command=lambda: [update(T,name)]).grid(row= 7, column=4)
    btn2 = tk.Button(window, text="Negativni", fg="blue",command= lambda: [update2(T,name)]).grid(row=7, column=5)




def backbutton(T,name):
    global number
    if (number % 2) == 1:
        number -= 1
        number = number / 2
        T.delete("1.0", END)
        x = Database.databaseforscriptsread(name, number)
        T.insert(INSERT, x)
    else:
        number = number / 2
        T.delete("1.0", END)
        x = Database.databaseforscriptsread(name, number)
        T.insert(INSERT, x)

def populate_list(bar_tree_view, hostname=''):
    for i in bar_tree_view.get_children():
        bar_tree_view.delete(i)
    for row in Database.fetchscript(hostname):
        bar_tree_view.insert('', 'end', values=row)

def deleteScript(Name,router):
    Database.deleteScript(Name)
    populate_list(router)

def update(T,name):
    global number
    if number >= 3:
        number = (number * 2) + 1
    else:
        number += 2
    x = Database.databaseforscriptsread(name, number)
    T.delete("1.0", END)
    T.insert(INSERT, x)

def update2(T,name):
    global number
    if number >= 2:
        number = (number * 2)
    else:
        number +=1
    x = Database.databaseforscriptsread(name,number)
    T.delete("1.0", END)
    T.insert(INSERT, x)


def Back():
    global number
    number = 1
    InsideApp.InsideApp()

