import tkinter as tk
import io
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import Send_SMS
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

    my_image = customtkinter.CTkImage(light_image=Image.open("arrow.jpg"))
    btn = customtkinter.CTkButton(window, text="", width=10, image=my_image, hover=True,
                                  command=lambda: buttonfunctions(window))
    btn.grid(row=0, column=0, padx=10, pady=10)

    lbl_search = customtkinter.CTkLabel(window, text='Name of the Script', width=10, font=customtkinter.CTkFont(size=15,
                                                                                        weight="bold"), corner_radius=5)
    lbl_search.grid(row=1, column=1, padx=(30, 0))

    hostname_search = StringVar()
    hostname_search_entry = customtkinter.CTkEntry(window, textvariable=hostname_search, width=100, height=10,
                                                   border_width=2, corner_radius=5)
    hostname_search_entry.grid(row=1, column=2, padx=(0, 150))

    bt1 = customtkinter.CTkButton(window, text="Chose by name", width=100,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,command = lambda: initialize(hostname_search_entry.get(),window))
    bt1.grid(row=1, column=2, padx=(70, 0))
    Tentry = customtkinter.CTkTextbox(window, height=100, width=200, state="normal", corner_radius=5, font=customtkinter.CTkFont(size=14,
                                                                                        weight="normal"))
    Tentry.grid(row=2, column=1, pady=20, sticky="NSEW")


    # command = lambda: [initialize(window, hostname_search_entry.get())])
    # bt2 = tk.Button(window, text="Search by name", fg="black")
    # bt2.grid(row=2, column=3, padx=(10, 10), pady=(0, 10))
    # b2 = Button(window, text="Delete Script", command=lambda: [deleteScript(hostname_search.get())])
    # b2.grid(row=3, column=4, sticky=W)
    def update_listbox():
        # Clear the listbox
        # listbox.delete(0, END)

        # Insert the current distinct script names from the database into the listbox
        for row in Database_teams.conn.execute('SELECT DISTINCT name FROM skripty'):
        # for row in Database_scripts.conn.execute('SELECT DISTINCT name FROM scripts'):
            # listbox.insert(END, row[0])
            Tentry.insert(END, f"{row[0]}\n")
        Tentry.configure(state=DISABLED)
    # Create a scrollbar
    # scrollbar = Scrollbar(window)
    # scrollbar.grid(row=75, column=4, sticky=N + S)

    # Create a Listbox widget
    # listbox = Listbox(window, height=10, width=50, font=("Helvetica", 14), bd=2, bg="#ffffff",
    #                         selectbackground="#cccccc", highlightthickness=0, justify="center", yscrollcommand=scrollbar.set)
    # listbox.grid(row=5, column=3,padx=(0,10),pady=100)
    def select_row(event):
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
        print(text)

    # Configure the scrollbar to work with the Listbox widget
    # scrollbar.config(command=listbox.yview)

    # Populate the Listbox with data
    update_listbox()
    Tentry.bind("<Double-1>", select_row)
    window.mainloop()



def initialize(name,window):
    x = Database_scripts.conn.execute("SELECT Name FROM scripts WHERE Name = ?", (name,))
    t = x.fetchone()
    if t == None:
        messagebox.showerror('Error', 'Error: Script with name' + " " + name + " "+ 'not found!')
    else:
        open_new_window_script(name,window)

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
    bitly.grid(row=10, column=1,pady=50, padx = 40,sticky="w")
    bitly_buttin = customtkinter.CTkButton(new_window, text="Get Short URL",command = lambda: Changelink(bitly.get(), bitly_var))
    bitly_buttin.grid(row=10, column=1,padx = 150)
    #

    new_window.wm_attributes("-topmost", True)
    open_new_window_image(event)

def Changelink(url,bitly_var):
    x = Change_Link.bitlylink(url)
    print(x)
    bitly_var.set(x)
    pyperclip.copy(bitly_var.get())

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
        print("yy")
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
        print(resize_count)

        # def delete_image(event):
        #     # Get the selected item from the listbox
        #     selection = event.widget.curselection()
        #     if selection:
        #         selected_item = event.widget.get(selection[0])
        #
        #
        #         # Create a popup menu with the option to delete the selected image
        #         popup_menu = Menu(new_window_image, tearoff=0)
        #         popup_menu.add_command(label="Delete",
        #                                command=lambda: [Database_images.delete_image_from_db(selected_item),
        #                                                 update_listbox_image()])
        #         popup_menu.add_command(label="Show",
        #                                command=lambda event=event: [display_image(event), update_listbox_image()])
        #
        #         # Display the popup menu at the mouse position
        #         try:
        #             popup_menu.tk_popup(event.x_root, event.y_root, 0)
        #         finally:
        #             popup_menu.grab_release()


        # listbox_images.bind("<Button-3>", delete_image)

    # def update_listbox():
    #     # Clear the listbox
    #     # listbox.delete(0, END)
    #
    #     # Insert the current distinct script names from the database into the listbox
    #     for row in Database_scripts.conn.execute('SELECT DISTINCT name FROM scripts'):
    #         # listbox.insert(END, row[0])
    #         Tentry.insert(END, f"{row[0]}\n")
    #     Tentry.configure(state=DISABLED)
    # # Create a scrollbar
    # # scrollbar = Scrollbar(window)
    # # scrollbar.grid(row=75, column=4, sticky=N + S)
    #
    # # Create a Listbox widget
    # # listbox = Listbox(window, height=10, width=50, font=("Helvetica", 14), bd=2, bg="#ffffff",
    # #                         selectbackground="#cccccc", highlightthickness=0, justify="center", yscrollcommand=scrollbar.set)
    # # listbox.grid(row=5, column=3,padx=(0,10),pady=100)
    #
    #
    # # Configure the scrollbar to work with the Listbox widget
    # # scrollbar.config(command=listbox.yview)
    #
    # # Populate the Listbox with data
    # update_listbox()

    # listbox.bind('<Double-1>', open_new_window_script)










    # def backbutton(T,name):
    #     global s, number
    #     global visited_ids
    #     # check if there is a previous node
    #     # if s is not None:
    #     #     # query the database for the previous node
    #     #     x = Database_scripts.conn.execute("SELECT parent_id,left,right FROM Scripts WHERE id = ?", (number,))
    #     #
    #     #     # fetch the row and update the variables
    #     #     row = x.fetchone()
    #     #     if row is not None:
    #     #         data = row[0]
    #     #         data1 = row[1]
    #     #         data2 = row[2]
    #     #         print(data1, data2)
    #     #         p =  Database_scripts.conn.execute("SELECT Text, id FROM Scripts WHERE Name = ? AND id = ?", (name, data,))
    #     #         h = p.fetchone()[0]
    #     #         T.delete("1.0", END)
    #     #         T.insert(INSERT, h)
    #     #         # if data1 == None:
    #     #         print("changed")
    #     #         number = data
    #     #         s = data
    #             #     print(number)
    #             # else:
    #             #     print("changed")
    #             #     s=data
    #             #     print(s)
    #     prev_id = visited_ids[-2]
    #     x = Database_scripts.conn.execute("SELECT Text, id, parent_id,left FROM Scripts WHERE id = ?", (prev_id,))
    #     row = x.fetchone()
    #
    #     data = row[0]
    #     dat2 = row[1]
    #     daata = row[2]
    #     dd = row[3]
    #
    #     T.delete("1.0", END)
    #     T.insert(INSERT, data)
    #
    #
    #     # update the global variables
    #     global number
    #     global s
    #     if dd == "negative":
    #         number = dat2
    #     else:
    #         s = dat2
    #         print(s)
    #
    #     print("Moved back to node with ID:", daata)
    #     visited_ids.pop()

    listbox_images.bind('<Double-1>', display_image)




    def deleteScript(Name):
        Database_scripts.deleteScript(Name)




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