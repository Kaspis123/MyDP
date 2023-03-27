import tkinter
from tkinter import messagebox

import Database_tasks
import Running
import NewQ
import Done
import NewS
import User_Manage
import Testovaci
import Send_SMS
import Change_Link
import Testik
import Quests
name = 0

def InsideApp():
    windowAPP = tkinter.Tk()  # vytvořeni objektu
    windowAPP.minsize(width=800, height=800)  # Nastavení velikosti okna aplikace
    windowAPP.title("Application")  # Pojmenování aplikace
    btn1 = tkinter.Button(windowAPP, text="New Quest",fg="green",command=lambda: [NewQuest()]).pack(side="left",anchor="nw")  # 'fg or foreground' is for coloring the contents (buttons)

    btn2 = tkinter.Button(windowAPP, text="Running", fg="purple",command=RunningQuests).pack(side="left",anchor="nw")

    btn3 = tkinter.Button(windowAPP, text="Finished", fg="black",command=Finished).pack(side="left",anchor="nw")  # 'side' is used to left or right align the widgets

    btn4 = tkinter.Button(windowAPP, text="New Scam", fg="orange",command=lambda :[windowAPP.destroy(),NewScript()]).pack(side="left",anchor="nw")
    # if check == "admin":
    btn5 = tkinter.Button(windowAPP, text="User Management", fg="black", command=lambda :[windowAPP.destroy(),User_Mana()]).pack(side="left", anchor="nw")
    btn6 = tkinter.Button(windowAPP, text="test", fg="black", command=lambda :[windowAPP.destroy(),Testov()]).pack(side="left", anchor="nw")

    btn7 = tkinter.Button(windowAPP, text="testik", fg="black", command=lambda: [windowAPP.destroy(), Testi()]).pack(
        side="left", anchor="nw")
    btn8 = tkinter.Button(windowAPP, text="Quests", fg="black", command=lambda: [ Quest(name)]).pack(
        side="left", anchor="nw")
    popup()


    windowAPP.mainloop()  # spuštění

def set_name(name1):
    global name
    name = name1

def popup():
     d = Database_tasks.get_new_tasks(name)
     if d > 0:
         messagebox.showinfo("Update", "You have" + " " +str(d) + " " +  "new tasks")

def Quest(User_name):
    Quests.show(User_name)
def Testi():
    Testik.Testi()
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