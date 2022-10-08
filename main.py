import tkinter
import InsideApp
from PIL import ImageTk,Image
import sqlite3 as sq3
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


window = tkinter.Tk()  # Zmena názvu Aplikace
window.minsize(width=500, height=500)  # Nastavení velikosti okna aplikace
window.title("Log In")  # Pojmenování aplikace
window.resizable()
x, y = 1924, 1061

list1 = [0, 0, 15, -65, 10, -65, 10]
list2 = [0, 0, -20, -80, -80, -55, -55]
def resize_widgets(event):
    global resized
    for items in cavas.find_all():
        if items != 1:
            cavas.moveto(items,  window.winfo_width()/2 + list1[items],  window.winfo_height()/2 + list2[items])

cavas = tkinter.Canvas(window, width=1980, height=1080)
cavas.pack(expand=True, fill='both')
cavas.bind('<Configure>', resize_widgets)

image = ImageTk.PhotoImage(file="login.png")
cavas.create_image(960, 540, image=image)
def print_hi():

    login_button = tkinter.Button(window, text="Click To Log In!", anchor="center", command=Log_in)
    cavas.create_window(x/2, y/2-20,  window=login_button, anchor="center")
    Username = tkinter.Label(window, text="Username")
    cavas.create_window(x/2-90, y/2-80, window = Username, anchor="center")
    EntryUser = tkinter.Entry(window)
    cavas.create_window(x/2+10, y/2-80,window=EntryUser, anchor="center")
    Password = tkinter.Label(window, text="Password")
    cavas.create_window(x/2-90, y/2-55, window=Password, anchor="center")
    PasswordEntry = tkinter.Entry(window, show="*")
    cavas.create_window(x/2+10, y/2-55, window=PasswordEntry, anchor="center")
    window.mainloop()  # spuštění

def Log_in():
    tkinter.Label(window, text="Logged in!").pack()
    window.destroy()
    InsideApp.InsideApp()





if __name__ == '__main__':
    print_hi()