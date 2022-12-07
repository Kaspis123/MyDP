import tkinter as tk
import tkinter.scrolledtext
from tkinter import Canvas, messagebox
from tkinter import *
from tkinter.ttk import *
from Tools.scripts.pindent import start

import Database
import DatabaseForScripts
import InsideApp

x = 0
number = 1
def retrieve_input(T,name,option,window):
    input = T.get("1.0", END)
    T.delete("1.0", END)
    global x
    global number
    x += 1
    if name == '' or option == None:
        x = 0
        number = 1
        window.destroy()
        NewS()
        messagebox.showerror("Error", "No data provided")
    else:
        if (x % 2) == 1:
            T.insert(INSERT, "Zadejte text při negativní odpovědi na " + Database.databaseforscriptsread(name, number))
            return input
        else:
            T.insert(INSERT, "Zadejte text při pozitivní odpovědi na " + Database.databaseforscriptsread(name, number))
            number += 1
            return input

def NewS():
    window = tkinter.Tk()  # vytvořeni objektu
    window.minsize(width=800, height=800)  # Nastavení velikosti okna aplikace
    window.title("New Script")  # Pojmenování aplikace
    frame_search = Frame(window)
    frame_search.grid(row=1, column=2)
    lbl_search = Label(frame_search, text='Name of the new Script', font=('bold', 12))
    lbl_search.grid(row=1, column=1, sticky=W)
    hostname_search = StringVar()
    hostname_search_entry = Entry(frame_search, textvariable=hostname_search)
    hostname_search_entry.grid(row=1, column=2)
    var1 = IntVar()
    var2 = IntVar()
    c1 = tk.Checkbutton(window, variable=var1, text='Phishing', onvalue=1, offvalue=0).grid(row=3, column=3)
    c2 = tk.Checkbutton(window ,variable=var2, text='Vishing',  onvalue=1, offvalue=0).grid(row=4, column=3)
    image = PhotoImage(file="arrow.jpg")
    btn = Button(window, image=image, command=lambda: [window.destroy(), Back()])
    btn.image = image
    btn.grid(row=0, column=0)

    def print_selection():
        if (var1.get() == 1) & (var2.get() == 0):
            return 1
        elif (var1.get() == 0) & (var2.get() == 1):
            return 0
        elif (var1.get() == 0) & (var2.get() == 0):
            messagebox.showerror("Error", "Atleast one must be chosen")
        else:
            messagebox.showerror("Error", "Cant use both")



    T = tk.Text(window, height=10, width=40)
    T.grid(row=10, column=3)
    T.insert(INSERT, "Úvodní věta")
    # Create button for next text.
    b1 = Button(window, text="Next and Save", command= lambda: [Database.databaseforscriptsinsert(print_selection(), hostname_search.get(), T.get("1.0", END)), retrieve_input(T,hostname_search_entry.get(),print_selection(), window)])
    # b1 = Button(window, text="Next", command=lambda: [DatabaseForScripts.Datafromscripts(hostname_search.get(), print_selection(), T.get("1.0", END)),retrieve_input(T,hostname_search_entry.get())])
    b1.grid(row=50, column=3, sticky=E)
    b2 = Button(window, text="Delete", command=lambda: [deleteScript(hostname_search.get(),bar_tree_view)])
    b2.grid(row=50, column=3, sticky=W)
    frame_bar = Frame(window)
    frame_bar.grid(row=20, column=0, columnspan=4, rowspan=6, pady=20, padx=20)

    columns = ['id', 'Name']
    bar_tree_view = Treeview(frame_bar, columns=columns, show="headings")
    bar_tree_view.column("id", width=30)
    for col in columns[1:]:
        bar_tree_view.column(col, width=120)
        bar_tree_view.heading(col, text=col)
    bar_tree_view.bind('<<TreeviewSelect>>', )
    bar_tree_view.pack(side="left", anchor="center", fill="y")
    scrollbar = Scrollbar(frame_bar, orient='vertical')
    scrollbar.configure(command=bar_tree_view.yview)
    scrollbar.pack(side="right", fill="y")
    bar_tree_view.config(yscrollcommand=scrollbar.set)
    frame_btns = Frame(window)
    frame_btns.grid(row=3, column=0)

    populate_list(bar_tree_view, )



    window.mainloop()


def deleteScript(Name,router):
    Database.deleteScript(Name)
    populate_list(router)



def Back():
    global x
    x = 0
    global number
    number = 1
    InsideApp.InsideApp()

def populate_list(bar_tree_view, hostname=''):
    for i in bar_tree_view.get_children():
        bar_tree_view.delete(i)
    for row in Database.fetchscript(hostname):
        bar_tree_view.insert('', 'end', values=row)



