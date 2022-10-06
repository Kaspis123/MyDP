import tkinter
import tkinter.scrolledtext
from tkinter import Canvas, messagebox

from Tools.scripts.pindent import start

x = 100
y = 60




def NewS():
    windowAPP = tkinter.Tk()  # vytvořeni objektu
    windowAPP.minsize(width=800, height=800)  # Nastavení velikosti okna aplikace
    windowAPP.title("New Script")  # Pojmenování aplikace


    def onMove(event):


        print(event.x)
        C.move(Myrec, event.x, 0)


    def Edit():
        windowAPPEdditing = tkinter.Tk()
        windowAPPEdditing.title("Editor")
        text = tkinter.Text(windowAPPEdditing, height=8)
        text.pack()
        text['state'] = 'normal'
        text_content = text.get('1.0', 'end')
        btnSave = tkinter.Button(windowAPPEdditing, text="Save & Quit", fg="black", command=Negative).pack(anchor="center")

    def Positive():
        P = Canvas(windowAPP,  height=50, width=100)
        Myrec = C.create_rectangle(x, y, 0, 0, fill="Green", tags="playbutton")
        windowAPP.bind('<Button 1 >', onMove)
        windowAPP.bind('<Button 3 >', editing)
        P.pack()

    def Negative():
        N = Canvas(windowAPP, bg="Red", height=50, width=100)
        N.bind('<Button 1 >', onMove)
        N.bind('<Button 3 >', editing)
        N.pack()

    def editing(event):
        # choices = ['Edit', 'Add Positive', 'Add Negative']
        # variable = tkinter.StringVar()
        # variable.set(choices[0])
        # w = tkinter.OptionMenu(windowAPP, variable, *choices)
        # w.pack()
        windowAPPEdit = tkinter.Tk()
        # windowAPPEdit.geometry(f'2x75+{event.x}+{event.y}')
        windowAPPEdit.title("Pick")
        btn1 = tkinter.Button(windowAPPEdit, text="Edit", fg="black", command= lambda :[Edit(), windowAPPEdit.destroy()]).grid(row=0,column=0)
        btn2 = tkinter.Button(windowAPPEdit, text="Positive", fg="black", command=lambda :[Positive(), windowAPPEdit.destroy()]).grid(row=1,column=0)
        btn3 = tkinter.Button(windowAPPEdit, text="Negative", fg="black", command=lambda :[Negative(), windowAPPEdit.destroy()]).grid(row=2,column=0)




    C = Canvas(windowAPP, height=500, width=500)
    Myrec = C.create_rectangle(x, y, 0, 0, fill="Blue", tags="playbutton")
    C.create_text(50, 25, text="START", anchor="center")
    windowAPP.bind('<Button 1 >', onMove)
    windowAPP.bind('<Button 3 >', editing)

    C.pack()
    windowAPP.mainloop()