import tkinter

import DatabaseForScripts
import Running
import NewQ
import Done
import NewS
import User_Manage
import Testovaci

def InsideApp():
    windowAPP = tkinter.Tk()  # vytvořeni objektu
    windowAPP.minsize(width=800, height=800)  # Nastavení velikosti okna aplikace
    windowAPP.title("Application")  # Pojmenování aplikace
    btn1 = tkinter.Button(windowAPP, text="New Quest",fg="green",command=NewQuest).pack(side="left",anchor="nw")  # 'fg or foreground' is for coloring the contents (buttons)

    btn2 = tkinter.Button(windowAPP, text="Running", fg="purple",command=RunningQuests).pack(side="left",anchor="nw")

    btn3 = tkinter.Button(windowAPP, text="Finished", fg="black",command=Finished).pack(side="left",anchor="nw")  # 'side' is used to left or right align the widgets

    btn4 = tkinter.Button(windowAPP, text="New Scam", fg="orange",command=lambda :[windowAPP.destroy(),NewScript()]).pack(side="left",anchor="nw")
    # if check == "admin":
    btn5 = tkinter.Button(windowAPP, text="User Management", fg="black", command=lambda :[windowAPP.destroy(),User_Mana()]).pack(side="left", anchor="nw")
    btn6 = tkinter.Button(windowAPP, text="test", fg="black", command=lambda :[windowAPP.destroy(),Testov()]).pack(side="left", anchor="nw")

    windowAPP.mainloop()  # spuštění

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