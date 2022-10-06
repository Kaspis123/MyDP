import tkinter

def Done():
    windowAPP = tkinter.Tk()  # vytvořeni objektu
    windowAPP.minsize(width=800, height=800)  # Nastavení velikosti okna aplikace
    windowAPP.title("Finished Tasks")  # Pojmenování aplikace
    windowAPP.mainloop()