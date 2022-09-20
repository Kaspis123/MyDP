import tkinter
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


window = tkinter.Tk()  # Zmena názvu Aplikace
window.minsize(width=220, height=80)  # Nastavení velikosti okna aplikace
window.title("Application")  # Pojmenování aplikace

def print_hi():



    # label = tkinter.Label(window, text="Please log in").pack(side="top", anchor="nw") # Zobrazení zprávy uvnitř pack - nahoru dolu, anchor - uhlopřička

    # label = tkinter.Label(window, text='Please log in', font="Arial").grid(row=0)

    tkinter.Label(window, text="Username").grid(row=0)  # 'username' is placed on position 00 (row - 0 and column - 0)
    # 'Entry' class is used to display the input-field for 'username' text label
    tkinter.Entry(window).grid(row=0, column=1)  # first input-field is placed on position 01 (row - 0 and column - 1)

    tkinter.Label(window, text="Password").grid(row=1)  # 'password' is placed on position 10 (row - 1 and column - 0)

    tkinter.Entry(window, show="*").grid(row=1, column=1)  # second input-field is placed on position 11 (row - 1 and column - 1)
    # tkinter.Button(window, text="Click Me!", command=DataCamp_Tutorial).grid()
    tkinter.Button(window, text="Click To Log In!", command=Log_in).grid(row=2, column=1)

    window.mainloop()  # spuštění

def Log_in():
    tkinter.Label(window, text="Logged in!").grid()





if __name__ == '__main__':
    print_hi()