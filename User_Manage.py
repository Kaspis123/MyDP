import tkinter
from tkinter import messagebox
import tkinter as tk
from PIL import ImageTk
from tkinter import *
from tkinter.ttk import *
import Database_users
import InsideApp


def Managemet():
    window = tkinter.Tk()  # vytvořeni objektu
    window.minsize(width=800, height=800)  # Nastavení velikosti okna aplikace
    window.title("Management")  # Pojmenování aplikace
    image = PhotoImage(file="arrow.jpg")
    btn = Button(window, image=image, command=lambda: [window.destroy(), Back()])
    btn.image = image
    btn.grid(row=0, column=0,sticky=W)

    lbl_search = Label(window, text='Search by Name', font=('bold', 12))
    lbl_search.grid(row=1, column=3, padx=(180, 0))
    hostname_search = StringVar()
    hostname_search_entry = Entry(window, textvariable=hostname_search)
    hostname_search_entry.grid(row=1, column=4)



    # btn1 = tkinter.Button(window, text="Add User", fg="Black", command=lambda: Add_User(hostname_entry.get(), Password_entry.get(), hostname_entry, Password_entry, router_tree_view))
    btn1 = tkinter.Button(window, text="Add User", fg="Black", command=lambda :open_new_window())
    btn1.grid(row=11, column=5,padx=(0, 100),sticky=N)
    btn2 = tkinter.Button(window, text="Delete User", fg="Black", command=lambda: open_new_delete())
    btn2.grid(row=11, column=4,padx=(100, 0))
    search_btn = Button(window, text='Search', width=12, command=lambda: update_Listbox2(hostname_search_entry.get()))
    search_btn.grid(row=1, column=5, padx=(0, 110))

    def update_listbox():
        listbox.delete(0, tk.END)
        listbox.insert(0, 'ID   Name')
        for row in Database_users.conn.execute('SELECT id, name FROM users'):
            listbox.insert(tk.END, f'{row[0]:<3} {row[1]}')

    listbox = Listbox(window)
    update_listbox()
    listbox.grid(row=4, column=3, columnspan=4, rowspan=6, pady=(50,0), padx=(180, 0))

    def Add_User(hostname, password,new_window):
        if hostname == '' or password == '':
            messagebox.showerror('Required Fields', 'Please include all fields')
            return
        Database_Add(hostname, password)
        update_listbox()
        new_window.destroy()

    def remove_User(Name, new_window):
        if Name == '':
            messagebox.showerror("Error", "No user found")

        else:
            Database_users.delete_user(Name)
            update_listbox()
            new_window.destroy()


    def open_new_window():
        # Create a new window
        new_window = tk.Toplevel()
        new_window.resizable(False,False)
        window_width = 250
        window_height = 130
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Add labels and entry fields for name and password
        name_label = tk.Label(new_window, text="Name:")
        name_entry = tk.Entry(new_window)
        password_label = tk.Label(new_window, text="Password:")
        password_entry = tk.Entry(new_window, show="*")

        # Add a button to save the data and close the window
        save_button = tk.Button(new_window, text="Add", command=lambda :[Add_User(name_entry.get(),password_entry.get(),new_window)])

        # Grid the labels, entry fields, and button
        name_label.grid(row=0, column=0, padx=10, pady=10)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        password_label.grid(row=1, column=0, padx=10, pady=10)
        password_entry.grid(row=1, column=1, padx=10, pady=10)
        save_button.grid(row=2, column=0, columnspan=2, padx=(50,0), pady=(5,0))
    def open_new_delete():
        # Create a new window
        new_window = tk.Toplevel()
        new_window.resizable(False,False)
        window_width = 200
        window_height = 80
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Add labels and entry fields for name and password
        name_label = tk.Label(new_window, text="Name:")
        name_entry = tk.Entry(new_window)


        # Add a button to save the data and close the window
        save_button = tk.Button(new_window, text="Delete", command=lambda :[remove_User(name_entry.get(),new_window)])

        # Grid the labels, entry fields, and button
        name_label.grid(row=0, column=0, padx=10, pady=10)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        save_button.grid(row=2, column=0, columnspan=2, padx=(45,0), pady=10)

    def Database_Add(User, Password):
        if len(User) < 3:
            messagebox.showerror("Error", "Name must contain atleast 3 characters")
        elif len(Password) < 3:
            messagebox.showerror("Error", "Password must contain atleast 3 characters")
        else:
            Database_users.insert_user(User, Password)

    def update_Listbox2(Name):
        listbox.delete(0, tk.END)
        listbox.insert(0, 'ID   Name')
        cur = Database_users.conn.cursor()
        cur.execute('SELECT id, name FROM users WHERE name=?', (Name,))
        rows = cur.fetchall()
        for row in rows:
            listbox.insert(tk.END, f'{row[0]:<3} {row[1]}')

    def Back():
        InsideApp.InsideApp()


