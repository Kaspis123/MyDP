import tkinter as tk
import io
from tkinter import *
from tkinter import messagebox

import pyperclip

import Change_Link
import Database_scripts
import Database_teams
import InsideApp
from PIL import ImageTk, Image
import customtkinter
number = 1
i=1
resize_count = 0
s=1
visited_ids = []

def Test():
    global number
    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    window = customtkinter.CTk()  # vytvořeni objektu
    window_width = 500
    window_height = 500
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    # Nastavení velikosti okna aplikace
    window.title("Test")  # Pojmenování aplikace
    window.resizable(False, False)

    btn = customtkinter.CTkButton(window, text="Back", width=10, hover=True,
                                   command=lambda: buttonfunctions(window))
    btn.pack(side="top", anchor="w", padx=10, pady=10)

    search_frame = customtkinter.CTkFrame(window)
    search_frame.pack(side="top", fill="x", padx=10, pady=10)

    # Define the "Name of the Script" label
    lbl_search = customtkinter.CTkLabel(search_frame, text='Name of the Script', font=customtkinter.CTkFont(size=15,
                                                                                                            weight="bold"),
                                        corner_radius=5)
    lbl_search.pack(side="left", padx=(30, 0), pady=10)

    # Define the "Hostname Search" entry field
    hostname_search = StringVar()
    hostname_search_entry = customtkinter.CTkEntry(search_frame, textvariable=hostname_search, width=80, height=2,
                                                   border_width=2, corner_radius=5)
    hostname_search_entry.pack(side="left", padx=(0, 10), pady=10)

    # Define the "Choose by name" button
    bt1 = customtkinter.CTkButton(search_frame, text="Choose by name", width=20, height=32,
                                  border_width=0, corner_radius=8,
                                  command=lambda: initialize(hostname_search_entry.get(), window))
    bt1.pack(side="left", padx=(10, 0), pady=10)

    # Define the "Textbox" widget
    Tentry = customtkinter.CTkTextbox(window, height=300, width=150, state="normal", corner_radius=5,
                                      font=customtkinter.CTkFont(size=14, weight="normal"))
    Tentry.pack(side="top", padx=10, pady=20)
    delbutton = customtkinter.CTkButton(window, text="Delete Script",width=20, height=32,
                                  border_width=0, corner_radius=8,
                                  command=lambda: deleteScript(hostname_search_entry.get(), Tentry))
    delbutton.pack(anchor="center")


    update_listbox(Tentry)
    Tentry.bind("<Double-1>", lambda event: select_row(Tentry, window))
    window.mainloop()
def update_listbox(Tentry):
    Tentry.configure(state=NORMAL)
    Tentry.delete("1.0", END)
    for row in Database_teams.conn.execute('SELECT DISTINCT name FROM skripty'):

        Tentry.insert(END, f"{row[0]}\n")
    Tentry.configure(state=DISABLED)

def select_row(Tentry,window):
    index = Tentry.index(INSERT)
    row = index.split(".")[0]
    # Get the index of the start of the row
    start_index = f"{row}.0"
    # Get the index of the end of the row
    end_index = f"{row}.end"
    # Get the text in the row
    text = Tentry.get(start_index, end_index)
    # Strip any trailing newline characters
    text = text.rstrip("\n")
    # Return the text
    open_new_window_script(text,window)

def initialize(name,window):
    x = Database_teams.conn.execute("SELECT Name FROM skripty WHERE Name = ?", (name,))
    t = x.fetchone()
    if t == None:
        messagebox.showerror('Error', 'Error: Script with name' + " " + name + " "+ 'not found!')
    else:
        open_new_window_script(name,window)
def close(window,window2,text,event):
    data = text.get("1.0", END)
    window.destroy()
    window2.destroy()
    Database_teams.insertinfoabouattack(event, data)
def on_closing(new):
    datawindow= customtkinter.CTk()
    frame = customtkinter.CTkFrame(datawindow)
    frame.pack(side="top", padx=5, pady=5)

    text = customtkinter.CTkTextbox(datawindow, width=500, height=300)
    label = customtkinter.CTkLabel(frame,text="Select task!").pack(side="left")
    teams = Database_teams.conn.execute("SELECT * FROM tasks").fetchall()
    team_names = [team[0] for team in teams]
    team_dropdown = customtkinter.CTkComboBox(frame, values=team_names)
    team_dropdown.pack(side="left")
    text.pack()

    text.insert("1.0", "Zadejte prosím data o průběhu útoku, pokud se jednalo o útok jaká je Uspěšnost, jaké informace"
                       " byly získány, co s nimi bylo poté uděláno atd. Nemusí být nutně podrobné. Pokud se nejednalo o"
                       " útok můžete tuto část ignorovat. !\n")

    btext = customtkinter.CTkButton(datawindow, text="Save", command=lambda: close(datawindow, new, text,team_dropdown.get())).pack()

    datawindow.mainloop()
def open_new_window_script(event,window):
    # Create a new window
    new_window = customtkinter.CTkToplevel()
    new_window.resizable(False,False)
    new_window.title(event)
    window_width = 500
    window_height = 500
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2)+40)
    y = int((screen_height / 2) - (window_height / 2)+40)
    new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    # selection = event.widget.curselection()
    # if selection:
    #     index = selection[0]
    #     item = event.widget.get(index)
    T = customtkinter.CTkTextbox(new_window, height=150, width=500)
    T.grid(row=5, column=1)
    # x = Database_teams.databaseforscriptsread(event, number)
    x= Database_teams.databaseforscriptsread(event,number)
    T.insert(INSERT, x)
    T.configure(state=DISABLED)
    # btn3 = tk.Button(new_window, text='Back', fg='black', command=lambda: [backbutton(T, item)]).grid(row=7,column=1)
    btn2 = customtkinter.CTkButton(new_window, text="Negativni", command=lambda: update3(T, event)).grid(row=6,
                                                                                                         column=1,sticky="w")
    btn1 = customtkinter.CTkButton(new_window, text="Pozitivni",  command=lambda: update4(T, event)).grid(row=6,column=1,)

    bitly_var = StringVar()
    bitly = customtkinter.CTkEntry(new_window, textvariable=bitly_var)
    bitly.grid(row=10, column=1, pady=50, sticky="w")
    bitly_buttin = customtkinter.CTkButton(new_window, text="Get Short URL",command = lambda: Changelink(bitly.get(), bitly_var))
    bitly_buttin.grid(row=10, column=1, padx=150)

    new_window.protocol("WM_DELETE_WINDOW", lambda : on_closing(new_window))
    new_window.wm_attributes("-topmost", True)
    open_new_window_image(event)
    new_window.mainloop()

def Changelink(url, bitly_var):
    x = Change_Link.bitlylink(url)
    bitly_var.set(x)
    pyperclip.copy(bitly_var.get())
def deleteScript(Name, Tentry):
    Database_teams.deleteScript(Name)
    update_listbox(Tentry)
def open_new_window_image(skript):
    # Create a new window
    new_window_image = customtkinter.CTkToplevel()
    new_window_image.resizable(False,False)
    new_window_image.title("Images")
    window_width = 200
    window_height = 200
    screen_width = new_window_image.winfo_screenwidth()
    screen_height = new_window_image.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))+700
    y = int((screen_height / 2) - (window_height / 2))-300
    new_window_image.geometry(f"{window_width}x{window_height}+{x}+{y}")
    listbox_images = Listbox(new_window_image, height=10, width=50, font=("Helvetica", 14), bd=2, bg="#3F373C", highlightthickness=0)


    listbox_images.grid(row=75, column=3)

    def update_listbox_image():
        DEFAULT_COLOR = "red"

        # Insert the default items
        listbox_images.insert(END, "Default Images")
        listbox_images.itemconfig(0, fg=DEFAULT_COLOR)
        for row in Database_teams.conn.execute('SELECT name FROM images WHERE skript=?', ("default",)):
            listbox_images.insert(END, row[0])
            listbox_images.itemconfig(END, fg="white")
        listbox_images.insert(END, "End of Default Images")
        p = listbox_images.size()
        listbox_images.itemconfig(p - 1, fg=DEFAULT_COLOR)

        for row in Database_teams.conn.execute('SELECT name FROM images WHERE skript=?', (skript,)):
            listbox_images.insert(END, row[0])
            listbox_images.itemconfig(END, fg="white")


    update_listbox_image()


    def display_image(event):
        # Get the selected item from the listbox
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            item = event.widget.get(index)
            if item == "Default Images" or item == "End of Default Images":
                return
            image_data = Database_teams.conn.execute('SELECT data FROM images WHERE name=?', (item,)).fetchone()[0]

            # Load the image data into a PIL Image object
            pil_image = Image.open(io.BytesIO(image_data))

            # Create a new window to display the image
            top = tk.Toplevel()
            top.title(item)
            top.maxsize(width=1200, height=1200)
            top.protocol("WM_DELETE_WINDOW", lambda: on_closing(top))

            # Create a Tkinter PhotoImage from the PIL Image object
            tk_image = ImageTk.PhotoImage(pil_image)

            # Add the image to a label and display it in the window
            label = tk.Label(top, image=tk_image)
            label.pack(fill=tk.BOTH, expand=True, anchor="center")

            # Bind the resize function to the <Configure> event of the window
            top.bind('<Configure>', lambda e: resize_image(label, tk_image, e.width, e.height))
            top.bind("<Destroy>", lambda e: on_closing(top))


        def on_closing(window):
            global resize_count
            resize_count = 0
            window.destroy()

        def resize_image(label, tk_image, new_width, new_height):
            global resize_count

            # Only resize the image if the window has been resized by the user
            if resize_count > 1:
                # Get the PIL Image from the PhotoImage object
                pil_image = ImageTk.getimage(tk_image).copy()
                # Resize the PIL Image
                pil_image = pil_image.resize((new_width, new_height), Image.ANTIALIAS)
                # Convert the PIL Image to a PhotoImage object
                resized_image = ImageTk.PhotoImage(pil_image)
                # Update the PhotoImage object in the label
                label.configure(image=resized_image)
                # Store a reference to the PhotoImage object to prevent it from being garbage collected
                label.image = resized_image

            # Increment the resize count
            resize_count += 1

        resize_count = 0




    listbox_images.bind('<Double-1>', display_image)









def increment_number(T, name):
    global number  # use global keyword to access and update the global variable
    global s  # use global keyword to access and update the global variable
    global visited_ids
    # print(s)
    x = Database_scripts.conn.execute("SELECT Text, id FROM Scripts WHERE Name = ? AND right = ? AND parent_id = ?", (name, "positive", s))
    row = x.fetchone()
    if row is not None:
        data = row[0]
        dat2 = row[1]
        number = dat2
        s = dat2
        visited_ids.append(dat2)
        T.configure(state="normal")
        T.delete("1.0", END)
        T.insert(INSERT, data)
        T.configure(state=DISABLED)

def update2(T, name):
    global number
    x = Database_scripts.conn.execute("SELECT Text, id FROM Scripts WHERE Name = ? AND left = ? AND parent_id = ?",
                                      (name, "negative", number))
    row = x.fetchone()
    if row is not None:
        dat2 = row[1]
        number = dat2
        visited_ids.append(dat2)
        x = Database_scripts.databaseforscriptsread(name, number)
        T.configure(state="normal")
        T.delete("1.0", END)
        T.insert(INSERT, x)
        T.configure(state=DISABLED)


def Back():
    global number
    global s
    number = 1
    s = 1
    InsideApp.InsideApp()
def destor():
    global number
    global s
    number = 1
    s = 1
    Test()
def buttonfunctions(window):
    window.destroy()
    Back()


def update4(T,name):
    global number
    T.configure(state="normal")
    if number >= 3:
        number = (number * 2) + 1
    else:
        number += 2
    x = Database_teams.databaseforscriptsread(name, number)
    T.delete("1.0", END)
    T.insert(INSERT, x)
    T.configure(state=DISABLED)


def update3(T,name):
    global number
    T.configure(state="normal")
    if number >= 2:
        number = (number * 2)
    else:
        number +=1
    x = Database_teams.databaseforscriptsread(name, number)
    T.delete("1.0", END)
    T.insert(INSERT, x)
    T.configure(state=DISABLED)