import io
import tkinter as tk


from tkinter import *

import customtkinter

import Change_Link


import Database_teams
import InsideApp
import pyperclip
from PIL import ImageTk, Image



x = 0
number = 1
y = 1
resize_count = 0
flag = True




def retrieve(T,name,window):
    input = T.get("1.0", END)
    T.delete("1.0", END)
    global x
    global number
    x += 1

    if (x % 2) == 1:
        T.insert(INSERT, "Zadejte text při negativní odpovědi na " + Database_teams.databaseforscriptsread(name,number))
        return input
    else:
        T.insert(INSERT, "Zadejte text při pozitivní odpovědi" + Database_teams.databaseforscriptsread(name,number))
        number += 1
        return input


def NewS():
    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green
    window = customtkinter.CTk()  # vytvořeni objektu
    window.minsize(width=500, height=500)  # Nastavení velikosti okna aplikace
    window.title("New Script")  # Pojmenování aplikace
    # window.iconbitmap("icon.ico")  # Set the window icon

    # Define the frames
    frame_search = customtkinter.CTkFrame(window)
    frame_search.grid(row=1, column=3, padx=10, pady=10)

    # Define the widgets
    lbl_search = customtkinter.CTkLabel(frame_search, text='Name of the new Script',width=120,
                               font=customtkinter.CTkFont(size=15, weight="bold"), corner_radius= 5)
    lbl_search.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)

    hostname_search = StringVar()
    hostname_search_entry = customtkinter.CTkEntry(frame_search, textvariable=hostname_search, width=120,
                               height=25,
                               border_width=2,
                               corner_radius=5)
    hostname_search_entry.grid(row=1, column=3, padx=10, pady=10)

    # image = PhotoImage(file="arrow.jpg")

    btn = customtkinter.CTkButton(window, text= "Back", width=10, hover=True,  command=lambda: buttonfunctions(window))
    btn.grid(row=0, column=0, padx=10, pady=10)

    T = customtkinter.CTkTextbox(window, height=150, width=40)
    T.grid(row=10, column=3, padx=10, pady=10, sticky="NSEW")
    T.insert(tk.INSERT, "Úvodní věta")


    b1 = customtkinter.CTkButton(window, text="Next and Save",width=100,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8, command=lambda: b1functions(hostname_search.get(),T,window))
    b1.grid(row=50, column=3, sticky=tk.E, padx=10, pady=10)
    # stop_button = customtkinter.CTkButton(window,width=100,
    #                              height=32,
    #                              border_width=0,
    #                              corner_radius=8, text="Stop this Branch", command=lambda: button(T, hostname_search.get(), window))
    # stop_button.grid(row=50, column=3, pady=10, padx=10, sticky=tk.W)

    window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())



    # bitly_var = StringVar()
    # bitly = Entry(window, textvariable=bitly_var)
    # bitly.grid(row=70, column=3, sticky=E)
    # Button(window, text="Get Short URL", command=lambda: [Changelink(bitly.get(),bitly_var)]).grid(row=71, column=3)
    #
    # # Create a button to open the file dialog
    button_image = customtkinter.CTkButton(window, text="Select Image",width=100,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8, command=lambda : buttonimagefunctions(hostname_search.get()))
    button_image.grid(row = 50, column= 3)


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
    # update_listbox()
    # listbox.grid(row=75, column=3)
    # listbox.bind('<Double-1>', display_image)
    # listbox.bind("<Button-3>", delete_image)
    # messagebox.showinfo("Information", "Prosím dodržujte právní zásady, viz zádání úkolu.")



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

# def b1functions(name ,T, window):
#     Database_scripts.databaseforscriptsinsert(name,  T.get("1.0", END))
#     retrieve_input(T, name, window)

def b1functions(name ,T, window):
    Database_teams.databaseforscriptsinsert(name,T.get("1.0", END))
    retrieve(T,name,window)

def buttonimagefunctions(name):
    Database_teams.insert_image(name)
def buttonfunctions(window):
    window.destroy()
    Back()







