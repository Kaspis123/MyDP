import tkinter
from tkinter import messagebox

from PIL import ImageTk
from tkinter import *
from tkinter.ttk import *
import Database
import InsideApp


def Managemet():
    window = tkinter.Tk()  # vytvořeni objektu
    window.minsize(width=800, height=800)  # Nastavení velikosti okna aplikace
    window.title("Management")  # Pojmenování aplikace
    frame_search = Frame(window)
    frame_search.grid(row=1, column=2)
    lbl_search = Label(frame_search, text='Search by Name', font=('bold', 12))
    lbl_search.grid(row=1, column=1, sticky=W)
    hostname_search = StringVar()
    hostname_search_entry = Entry(frame_search, textvariable=hostname_search)
    hostname_search_entry.grid(row=1, column=2)

    image = PhotoImage(file="arrow.jpg")
    btn = Button(window, image=image, command=lambda: [window.destroy(), Back()])
    btn.image = image
    btn.grid(row=0, column=0)
    frame_fields = Frame(window)
    frame_fields.grid(row=2, column=1)

    hostname_text = StringVar()
    hostname_label = Label(frame_fields, text='Name', font=('bold', 12))
    hostname_label.grid(row=3, column=0, sticky=E)
    hostname_entry = Entry(frame_fields, textvariable=hostname_text)
    hostname_entry.grid(row=3, column=1, sticky=W)
    Password_text = StringVar()
    Password_label = Label(frame_fields, text='Password', font=('bold', 12))
    Password_label.grid(row=4, column=0, sticky=E)
    Password_entry = Entry(frame_fields, textvariable=Password_text)
    Password_entry.grid(row=4, column=1, sticky=W)

    frame_router = Frame(window)
    frame_router.grid(row=4, column=0, columnspan=4, rowspan=6, pady=20, padx=20)

    columns = ['id', 'Name', 'Password']
    router_tree_view = Treeview(frame_router, columns=columns, show="headings")
    router_tree_view.column("id", width=30)
    for col in columns[1:]:
        router_tree_view.column(col, width=120)
        router_tree_view.heading(col, text=col)
    router_tree_view.bind('<<TreeviewSelect>>',)
    router_tree_view.pack(side="left",anchor="center", fill="y")
    scrollbar = Scrollbar(frame_router, orient='vertical')
    scrollbar.configure(command=router_tree_view.yview)
    scrollbar.pack(side="right", fill="y")
    router_tree_view.config(yscrollcommand=scrollbar.set)
    frame_btns = Frame(window)
    frame_btns.grid(row=3, column=0)
    btn1 = tkinter.Button(window, text="Add User", fg="Black", command=lambda: Add_User(hostname_entry.get(),Password_entry.get(),hostname_entry,Password_entry,router_tree_view))
    btn1.grid(row=3, column=1, pady=20)
    btn2 = tkinter.Button(window, text="Delete User", fg="Black", command=lambda: remove_User(hostname_entry.get(), hostname_entry,Password_entry,router_tree_view))
    btn2.grid(row=3, column=1, pady=20)
    search_btn = Button(frame_search, text='Search', width=12, command=lambda: search_hostname(router_tree_view,hostname_search_entry.get()))
    search_btn.grid(row=1, column=3, pady=20)
    populate_list(router_tree_view,)


def Add_User(hostname, password, hostname_entry, password_entry, router):
    if hostname == '' or password == '' :
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    Database_Add(hostname, password)
    clear_text(hostname_entry, password_entry)
    populate_list(router)


def remove_User(Name, hostname_entry, password_entry, router):
    Database.Delete_User(Name)
    clear_text(hostname_entry, password_entry)
    populate_list(router)

def Database_Add(User, Password):
    if len(User) < 3:
        messagebox.showerror("Error", "Name must contain atleast 3 characters")
    elif len(Password) < 3:
        messagebox.showerror("Error", "Password must contain atleast 3 characters")
    else:
        Database.insert_to_database(User, Password)



def Error_Handle(Name):
    messagebox.showerror("Error", "User with  name" + " " + Name +" " + "already exists")

def Database_Delete_User(Name,window):
    Database.Delete_User(Name)
    window.destroy()
def Show_All_Users():
    Database.Show_All_Database()
def Back():
    InsideApp.InsideApp()

def populate_list(router_tree_view, hostname=''):
    for i in router_tree_view.get_children():
        router_tree_view.delete(i)
    for row in Database.fetch(hostname):
        router_tree_view.insert('', 'end', values=row)
def clear_text(hostname,password):
    hostname.delete(0, END)
    password.delete(0, END)

def search_hostname(router, hostname):
    populate_list(router, hostname)

