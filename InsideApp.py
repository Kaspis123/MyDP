import tkinter
from tkinter import messagebox

import Database_teams
import Running
import NewQ
import Done
import NewS
import User_Manage
import Testovaci
import customtkinter

import Quests
name = 0

def InsideApp():
    windowAPP = customtkinter.CTk()  # vytvořeni objektu
    windowAPP.minsize(width=190, height=200)  # Nastavení velikosti okna aplikace
    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")
    windowAPP.title("Application")  # Pojmenování aplikace
    if Database_teams.ismanagement(name) == True:
        btn1 = customtkinter.CTkButton(windowAPP, text="New Quest",command=lambda: NewQuest()).pack(pady=10)  # 'fg or foreground' is for coloring the contents (buttons)

        btn2 = customtkinter.CTkButton(windowAPP, text="Running",command=RunningQuests).pack(pady=10)

        btn3 = customtkinter.CTkButton(windowAPP, text="Finished",command=Finished).pack(pady=10)  # 'side' is used to left or right align the widgets
        btn5 = customtkinter.CTkButton(windowAPP, text="User Management",
                                  command=lambda: bt5(windowAPP) ).pack(pady=10)

    btn4 = customtkinter.CTkButton(windowAPP, text="New Scam",command=lambda :bt4(windowAPP)).pack(pady=10)


    btn6 = customtkinter.CTkButton(windowAPP, text="test", command=lambda :bt6(windowAPP)).pack(pady=10)


    btn8 = customtkinter.CTkButton(windowAPP, text="Quests", command=lambda: Quest(name)).pack(pady=10
        )
    popup()


    windowAPP.mainloop()  # spuštění
def bt5(window):
    window.destroy()
    User_Mana()
def bt4(window):
    window.destroy()
    NewScript()
def bt6(window):
    window.destroy()
    Testov()


def set_name(name1):
    global name
    name = name1

def popup():
     d = Database_teams.get_new_tasks(name)
     if d > 0:
         messagebox.showinfo("Update", "You have" + " " +str(d) + " " +  "new tasks")

def Quest(User_name):
    Quests.show(User_name)

def Testov():
    Testovaci.Test()
def User_Mana():
    User_Manage.Managemet()

def NewQuest():
    NewQ.NewQ()

def RunningQuests():
    Running.Running()

def Finished():
    Done.Done()

def NewScript():
    NewS.NewS()