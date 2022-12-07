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
    window.minsize(width=800, height=800)  # Nastavení velikosti okna aplikace
    window.title("Management")  # Pojmenování aplikace
    image = PhotoImage(file="arrow.jpg")
    frame_search = Frame(window)
    frame_search.grid(row=1, column=2)
    lbl_search = Label(frame_search, text='Name of the script', font=('bold', 12))
    lbl_search.grid(row=1, column=1, sticky=W)
    hostname_search = StringVar()
    hostname_search_entry = Entry(frame_search, textvariable=hostname_search)
    hostname_search_entry.grid(row=1, column=2)
    btn = Button(window, image=image, command=lambda: [window.destroy(), Back()])
    btn.image = image
    btn.grid(row=0, column=0)
    bt1 = tk.Button(window, text="Chose by name", fg="red",command= lambda: [initialize(window,hostname_search_entry.get())]).grid(row= 6, column=4)
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

