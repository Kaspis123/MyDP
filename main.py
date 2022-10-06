import tkinter
import InsideApp
from PIL import ImageTk,Image
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


window = tkinter.Tk()  # Zmena názvu Aplikace
window.minsize(width=500, height=500)  # Nastavení velikosti okna aplikace
window.title("Log In")  # Pojmenování aplikace





def print_hi():
    x, y = 1920, 1040
    cavas = tkinter.Canvas(window, width=1920, height=1080)
    cavas.pack(anchor="s")
    login_button = tkinter.Button(window, text="Click To Log In!", anchor="center", command=Log_in)
    cavas.create_window(x/2, y/2,  window=login_button)
    image = ImageTk.PhotoImage(file="png-1.png")
    cavas.create_image(960, 540, image=image)
    Username = tkinter.Label(window, text="Username")
    cavas.create_window(870, 460, window = Username)
    EntryUser = tkinter.Entry(window)
    cavas.create_window(970, 460,window=EntryUser)
    Password = tkinter.Label(window, text="Password")
    cavas.create_window(870, 485, window=Password)
    PasswordEntry = tkinter.Entry(window, show="*")
    cavas.create_window(970, 485, window=PasswordEntry)
    window.mainloop()  # spuštění

def Log_in():
    tkinter.Label(window, text="Logged in!").pack()
    window.destroy()
    InsideApp.InsideApp()





if __name__ == '__main__':
    print_hi()