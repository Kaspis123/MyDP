import tkinter as tk
import io
from tkinter import *
from tkinter.ttk import *
import Database_scripts
import Database_teams
import InsideApp
from PIL import ImageTk, Image
number = 1
resize_count = 0
def Test():
    global number
    window = tk.Tk()  # vytvořeni objektu
    window_width = 800
    window_height = 800
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    # Nastavení velikosti okna aplikace
    window.title("Test")  # Pojmenování aplikace
    window.resizable(False, False)

    image = PhotoImage(file="arrow.jpg")
    btn = Button(window, image=image, command=lambda: [window.destroy(), Back()])
    btn.image = image
    btn.grid(row=0, column=0)

    lbl_search = Label(window, text='Name of the Script', font=('bold', 12))
    lbl_search.grid(row=1, column=15)

    hostname_search = StringVar()
    hostname_search_entry = Entry(window, textvariable=hostname_search)
    hostname_search_entry.grid(row=2, column=15)

    bt1 = tk.Button(window, text="Chose by name", fg="red",
                    command=lambda: [initialize(window, hostname_search_entry.get())])
    bt1.grid(row=2, column=4, padx=(10, 0), pady=(0, 10))

    bt2 = tk.Button(window, text="Search by name", fg="black")
    bt2.grid(row=2, column=3, padx=(10, 10), pady=(0, 10))
    b2 = Button(window, text="Delete Script", command=lambda: [deleteScript(hostname_search.get())])
    b2.grid(row=3, column=4, sticky=W)

    def initialize(window,name):
        T = tk.Text(window, height=10, width=40)
        T.grid(row=5, column=3)
        x = Database_scripts.databaseforscriptsread(name,number)
        T.insert(INSERT, x)
        btn3 = tk.Button(window,text='Back',fg='black', command= lambda: [backbutton(T, name)]).grid(row=6,column=6)
        btn1 = tk.Button(window, text="Pozitivni", fg="green",command=lambda: [update(T,name)]).grid(row= 7, column=4)
        btn2 = tk.Button(window, text="Negativni", fg="blue",command= lambda: [update2(T,name)]).grid(row=7, column=5)




    def open_new_window_script(event):
        # Create a new window
        new_window = tk.Toplevel()
        new_window.resizable(False,False)
        new_window.title("Script")
        window_width = 500
        window_height = 500
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            item = event.widget.get(index)
            T = tk.Text(new_window, height=10, width=40)
            T.grid(row=5, column=3)
            x = Database_scripts.databaseforscriptsread(item, number)
            T.insert(INSERT, x)
            btn3 = tk.Button(new_window, text='Back', fg='black', command=lambda: [backbutton(T, item)]).grid(row=7,column=1)
            btn1 = tk.Button(new_window, text="Pozitivni", fg="green", command=lambda: [update(T, item)]).grid(row=7,column=3)
            btn2 = tk.Button(new_window, text="Negativni", fg="blue", command=lambda: [update2(T, item)]).grid(row=7,column=4)
            open_new_window_image(item)
    def open_new_window_image(skript):
        # Create a new window
        new_window_image = tk.Toplevel()
        new_window_image.resizable(False,False)
        new_window_image.title("Images")
        window_width = 200
        window_height = 200
        screen_width = new_window_image.winfo_screenwidth()
        screen_height = new_window_image.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))+700
        y = int((screen_height / 2) - (window_height / 2))-300
        new_window_image.geometry(f"{window_width}x{window_height}+{x}+{y}")
        listbox_images = Listbox(new_window_image)
        listbox_images.grid(row=75, column=3)

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

        def update_listbox_image():
            DEFAULT_COLOR = "red"

            # Insert the default items
            listbox_images.insert(END, "Default Images")
            listbox_images.itemconfig(0, fg=DEFAULT_COLOR)
            for row in Database_teams.conn.execute('SELECT name FROM images WHERE skript=?', ("default",)):
                listbox_images.insert(END, row[0])
            listbox_images.insert(END, "End of Default Images")
            p = listbox_images.size()
            listbox_images.itemconfig(p-1 , fg=DEFAULT_COLOR)

            for row in Database_teams.conn.execute('SELECT name FROM images WHERE skript=?', (skript,)):
                listbox_images.insert(END, row[0])

        update_listbox_image()
        listbox_images.bind('<Double-1>', display_image)
        # listbox_images.bind("<Button-3>", delete_image)

    def update_listbox():
        # Clear the listbox
        listbox.delete(0, END)

        # Insert the current distinct script names from the database into the listbox
        for row in Database_scripts.conn.execute('SELECT DISTINCT name FROM scripts'):
            listbox.insert(END, row[0])

    # Create a scrollbar
    scrollbar = Scrollbar(window)
    scrollbar.grid(row=75, column=4, sticky=N + S)

    # Create a Listbox widget
    listbox = Listbox(window, yscrollcommand=scrollbar.set)
    listbox.grid(row=75, column=3)

    # Configure the scrollbar to work with the Listbox widget
    scrollbar.config(command=listbox.yview)

    # Populate the Listbox with data
    update_listbox()
    listbox.bind('<Double-1>', open_new_window_script)


    def backbutton(T,name):
        global number
        if (number % 2) == 1:
            number -= 1
            number = number / 2
            T.delete("1.0", END)
            x = Database_scripts.databaseforscriptsread(name, number)
            T.insert(INSERT, x)
        else:
            number = number / 2
            T.delete("1.0", END)
            x = Database_scripts.databaseforscriptsread(name, number)
            T.insert(INSERT, x)



    def deleteScript(Name):
        Database_scripts.deleteScript(Name)
        update_listbox()


    def update(T,name):
        global number
        if number >= 3:
            number = (number * 2) + 1
        else:
            number += 2
        x = Database_scripts.databaseforscriptsread(name, number)
        T.delete("1.0", END)
        T.insert(INSERT, x)

    def update2(T,name):
        global number
        if number >= 2:
            number = (number * 2)
        else:
            number +=1
        x = Database_scripts.databaseforscriptsread(name,number)
        T.delete("1.0", END)
        T.insert(INSERT, x)


    def Back():
        global number
        number = 1
        InsideApp.InsideApp()

