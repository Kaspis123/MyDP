import io
import tkinter as tk

from tkinter import Canvas, messagebox
from tkinter import *
from tkinter.ttk import *

import Change_Link
import Database_scripts

import Database_teams
import InsideApp
import pyperclip
from PIL import ImageTk, Image


x = 1
number = 1
y = 1
resize_count = 0
flag = True


def button(T,name,window):
    # T.delete("1.0", END)  # Clear the text from the input area
    # T.insert(INSERT,"Zadejte text při negativní odpovědi na " + Database_scripts.databaseforscriptsread(name, number))
    global x
    global y
    global number
    global flag
    flag = True
    x-=1
    y=+1
    # Database_scripts.increate_idp()
    retrieve_input(T, name, window)

def retrieve_input(T,name,window):
    global x
    global number
    global y
    global flag
    Database_scripts.set_number(number)
    Database_scripts.set_flag(flag)
    input = T.get("1.0", END)
    T.delete("1.0", END)  # Clear the text from the input area
    Button(window, text="Stop this Branch", command=lambda : [button(T,name,window)]).grid(row=50, column=2, sticky=E)
    if name == '':
        x = 1
        number = 1
        window.destroy()
        NewS()
        messagebox.showerror("Error", "No data provided")
    else:
        if flag:
            T.insert(INSERT, "Zadejte text při negativní odpovědi na " + Database_scripts.databaseforscriptsread(name, number))
            y += 1
        else:
            T.insert(INSERT, "Zadejte text při pozitivní odpovědi na " + Database_scripts.databaseforscriptsread(name, number))
            x += 1
        if y > x:
            flag = False
            y = 1
        else:
            flag = True
            number += 1
    return input


def NewS():

    window = tk.Tk()  # vytvořeni objektu
    window.minsize(width=800, height=800)  # Nastavení velikosti okna aplikace
    window.title("New Script")  # Pojmenování aplikace

    frame_search = Frame(window)
    frame_search.grid(row=1, column=3)

    lbl_search = Label(frame_search, text='Name of the new Script', font=('bold', 12))
    lbl_search.grid(row=1, column=1, sticky=tk.W)

    hostname_search = StringVar()
    hostname_search_entry = Entry(frame_search, textvariable=hostname_search)
    hostname_search_entry.grid(row=1, column=3)

    # var1 = tk.IntVar()
    # var2 = tk.IntVar()

    # c1 = tk.Checkbutton(window, variable=var1, text='Phishing', onvalue=1, offvalue=0)
    # c1.grid(row=11, column=2, padx=(10, 0), pady=0)
    #
    # c2 = tk.Checkbutton(window, variable=var2, text='Vishing  ', onvalue=1, offvalue=0)
    # c2.grid(row=12, column=2, padx=(10, 0), pady=0)
    image = PhotoImage(file="arrow.jpg")
    btn = Button(window, image=image, command=lambda: [window.destroy(), Back()])
    btn.image = image
    btn.grid(row=0, column=0)

    # def print_selection():
    #     if (var1.get() == 1) & (var2.get() == 0):
    #         return 1
    #     elif (var1.get() == 0) & (var2.get() == 1):
    #         return 0
    #     elif (var1.get() == 0) & (var2.get() == 0):
    #         messagebox.showerror("Error", "Atleast one must be chosen")
    #     else:
    #         messagebox.showerror("Error", "Cant use both")

    T = tk.Text(window, height=10, width=40)
    T.grid(row=10, column=3, rowspan=35, padx=10, pady=10, sticky="NSEW")
    T.insert(tk.INSERT, "Úvodní věta")
    # Create button for next text.
    b1 = Button(window, text="Next and Save", command= lambda: [Database_scripts.databaseforscriptsinsert(hostname_search.get(), T.get("1.0", END)), retrieve_input(T,hostname_search_entry.get(), window)])

    # b1 = Button(window, text="Next", command=lambda: [DatabaseForScripts.Datafromscripts(hostname_search.get(), print_selection(), T.get("1.0", END)),retrieve_input(T,hostname_search_entry.get())])
    b1.grid(row=50, column=3, sticky=E)

    bitly_var = StringVar()
    bitly = Entry(window, textvariable=bitly_var)
    bitly.grid(row=70, column=3, sticky=E)
    Button(window, text="Get Short URL", command=lambda: [Changelink(bitly.get(),bitly_var)]).grid(row=71, column=3)



    # Create a button to open the file dialog
    button = Button(window, text="Select Image", command=lambda : [Database_teams.insert_image(hostname_search.get()),update_listbox()])
    button.grid(row = 72, column= 3)


    def display_image(event):
        # Get the selected item from the listbox
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            item = event.widget.get(index)
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
    # print(resize_count)



    def delete_image(event):
        # Get the selected item from the listbox
        selection = event.widget.curselection()
        if selection:
            selected_item = event.widget.get(selection[0])

            # Create a popup menu with the option to delete the selected image
            popup_menu = Menu(window, tearoff=0)
            popup_menu.add_command(label="Delete", command=lambda :[Database_teams.delete_image_from_db(selected_item), update_listbox()])
            popup_menu.add_command(label="Show", command=lambda event=event: [display_image(event), update_listbox()])

            # Display the popup menu at the mouse position
            try:
                popup_menu.tk_popup(event.x_root, event.y_root, 0)
            finally:
                popup_menu.grab_release()


    def update_listbox():
        # Clear the listbox
        listbox.delete(0, END)

        # Insert the current image names from the database into the listbox
        for row in Database_teams.conn.execute('SELECT name FROM images'):
            listbox.insert(END, row[0])

    listbox = Listbox(window)
    update_listbox()
    listbox.grid(row=75, column=3)
    listbox.bind('<Double-1>', display_image)
    listbox.bind("<Button-3>", delete_image)

    window.mainloop()




def Changelink(url,bitly_var):
    x = Change_Link.bitlylink(url)
    print(x)
    bitly_var.set(x)
    pyperclip.copy(bitly_var.get())


def Back():
    global x
    x = 1
    global number
    number = 1
    global y
    y = 1
    global flag
    flag = True
    InsideApp.InsideApp()





