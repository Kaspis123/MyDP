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
    btn = Button(window, image=image, command=lambda: [window.destroy(), Back()])
    btn.image = image
    btn.grid(row=0, column=0)
    T = tk.Text(window, height=10, width=40)
    T.grid(row=5, column=3)
    print(number)
    x = DatabaseForScripts.ReadDataFromDatabase(number)
    T.insert(INSERT, x)
    btn1 = tk.Button(window, text="Pozitivni", fg="green",command=lambda: [update(T)]).grid(row= 7, column=4)
    btn2 = tk.Button(window, text="Negativni", fg="blue",command= lambda: [update2(T)]).grid(row=7, column=5)
def update(T):
    global number
    if number >= 3:
        number = (number * 2) + 1
    else:
        number += 2
    x = DatabaseForScripts.ReadDataFromDatabase(number)
    T.delete("1.0", END)
    T.insert(INSERT, x)

def update2(T):
    global number
    if number >= 2:
        number = (number * 2)
    else:
        number +=1
    x = DatabaseForScripts.ReadDataFromDatabase(number)
    T.delete("1.0", END)
    T.insert(INSERT, x)


def Back():
    global number
    number = 1
    InsideApp.InsideApp()

