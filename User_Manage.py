import tkinter
from tkinter import messagebox

import Database

def Managemet():
    window = tkinter.Tk()  # vytvořeni objektu
    window.minsize(width=800, height=800)  # Nastavení velikosti okna aplikace
    window.title("Management")  # Pojmenování aplikace
    btn1 = tkinter.Button(window, text="Add User", fg="Black", command=Add_User).pack(side="left", anchor="nw")
    btn2 = tkinter.Button(window, text="Delete User", fg="Black", command=Delete_User).pack(side="left", anchor="nw")


def Add_User():
    x = 800
    y = 800
    windowAdd = tkinter.Tk()  # vytvořeni objektu
    windowAdd.minsize(width=x, height=y)  # Nastavení velikosti okna aplikace
    windowAdd.title("Add User")  # Pojmenování aplikace
    # cavas = tkinter.Canvas(windowAdd, width=x, height=y)
    # cavas.pack(expand=True, fill='both')
    # cavas.create_window(x / 2, y / 2 - 20, window=Add_button, anchor="center")
    Username = tkinter.Label(windowAdd, text="Username").pack(side="top", anchor="center")
    # cavas.create_window(x/2, y/2, window=Username, anchor="center")
    EntryUser = tkinter.Entry(windowAdd)
    EntryUser.pack(side="top", anchor="center")
    # cavas.create_window(x/2, y/2, window=EntryUser, anchor="center")
    Password = tkinter.Label(windowAdd, text="Password").pack(side="top", anchor="center")
    # cavas.create_window(x/2, y/2, window=Password, anchor="center")
    PasswordEntry = tkinter.Entry(windowAdd)
    PasswordEntry.pack(side="top", anchor="center")
    # cavas.create_window(x/2, y/2, window=PasswordEntry, anchor="center")
    Add_button = tkinter.Button(windowAdd, text="Add User!", command=lambda : [Database_Add(EntryUser.get(),PasswordEntry.get(),windowAdd)]).pack(anchor="center")





def Delete_User():
    windowDel = tkinter.Tk()  # vytvořeni objektu
    windowDel.minsize(width=800, height=800)  # Nastavení velikosti okna aplikace
    windowDel.title("Delete User")  # Pojmenování aplikace
    Username = tkinter.Label(windowDel, text="Username").pack(side="top", anchor="center")
    EntryUser = tkinter.Entry(windowDel)
    EntryUser.pack(side="top", anchor="center")
    Del_button = tkinter.Button(windowDel, text="Delete User!",command=lambda: [Database_Delete_User(EntryUser.get(),windowDel)]).pack(anchor="center")

def Database_Add(User, Password, window):
    if len(User) < 3:
        messagebox.showerror("Error", "Name must contain atleast 3 characters")
    elif len(Password) < 3:
        messagebox.showerror("Error", "Password must contain atleast 3 characters")
    else:
        Database.insert_to_database(User, Password)
        window.destroy()


def Error_Handle(Name):
    messagebox.showerror("Error", "User with  name" + " " + Name +" " + "already exists")

def Database_Delete_User(Name,window):
    Database.Delete_User(Name)
    window.destroy()