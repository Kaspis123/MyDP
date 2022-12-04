import tkinter as tk
import tkinter.scrolledtext
from tkinter import Canvas, messagebox
from tkinter import *
from tkinter.ttk import *
from Tools.scripts.pindent import start

import DatabaseForScripts
import InsideApp
a = 60
b = 3
x = 0
def retrieve_input(T):
    input = T.get("1.0", END)
    print(input)
    T.delete("1.0", END)
    global x
    x += 1
    if (x % 2) == 1:
        T.insert(INSERT, "Zadejte text při negativní odpovědi")
        return input
    else:
        T.insert(INSERT, "Zadejte text při pozitivní odpovědi")
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
    b1 = Button(window, text="Next", command=lambda: [DatabaseForScripts.Datafromscripts(hostname_search.get(), print_selection(), retrieve_input(T)), ctverec(window)])
    b1.grid(row=50, column=3, sticky=E)
    b2 = Button(window, text="Save", command=lambda: [retrieve_input(T), print_selection()])
    b2.grid(row=50, column=3, sticky=W)

    window.mainloop()


def ctverec(window):
    global a, b

    b2 = Button(window).grid(row=a, column=b, sticky=W)
    b = b +1
    print(b)

def Back():
    InsideApp.InsideApp()


