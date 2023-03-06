import tkinter
from tkinter import messagebox
import tkinter as tk
from PIL import ImageTk
from tkinter import *
from tkinter.ttk import *
import Database
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





    frame_router = Frame(window)
    frame_router.grid(row=4, column=3, columnspan=4, rowspan=6, pady=(50,0), padx=(180, 0))

    columns = ['id', 'Name', 'Password']
    router_tree_view = Treeview(frame_router, columns=columns, show="headings")
    router_tree_view.column("id", width=30)
    for col in columns[1:]:
        router_tree_view.column(col, width=120)
        router_tree_view.heading(col, text=col)
    router_tree_view.bind('<<TreeviewSelect>>',)
    router_tree_view.pack(side="left",anchor="center", fill="y")
    scrollbar = Scrollbar(frame_router, orient='vertical')
    scrollbar.configure(command=router_tree_view.yview)
    scrollbar.pack(side="right", fill="y")
    router_tree_view.config(yscrollcommand=scrollbar.set)

    # btn1 = tkinter.Button(window, text="Add User", fg="Black", command=lambda: Add_User(hostname_entry.get(), Password_entry.get(), hostname_entry, Password_entry, router_tree_view))
    btn1 = tkinter.Button(window, text="Add User", fg="Black", command=lambda :open_new_window(router_tree_view))
    btn1.grid(row=11, column=5,padx=(0, 100),sticky=N)
    btn2 = tkinter.Button(window, text="Delete User", fg="Black", command=lambda: open_new_delete(router_tree_view))
    btn2.grid(row=11, column=4,padx=(100, 0))
    search_btn = Button(window, text='Search', width=12, command=lambda: search_hostname(router_tree_view, hostname_search_entry.get()))
    search_btn.grid(row=1, column=5, padx=(0, 110))
    populate_list(router_tree_view,)


def open_new_window(router):
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
    save_button = tk.Button(new_window, text="Add", command=lambda :[Add_User(name_entry.get(),password_entry.get(),name_entry,password_entry,router),new_window.destroy()])

    # Grid the labels, entry fields, and button
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry.grid(row=0, column=1, padx=10, pady=10)
    password_label.grid(row=1, column=0, padx=10, pady=10)
    password_entry.grid(row=1, column=1, padx=10, pady=10)
    save_button.grid(row=2, column=0, columnspan=2, padx=(50,0), pady=(5,0))
def open_new_delete(router):
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
    save_button = tk.Button(new_window, text="Delete", command=lambda :[remove_User(name_entry.get(),name_entry,router),new_window.destroy()])

    # Grid the labels, entry fields, and button
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    save_button.grid(row=2, column=0, columnspan=2, padx=(45,0), pady=10)




def Add_User(hostname, password, hostname_entry, password_entry, router):
    if hostname == '' or password == '':
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    Database_Add(hostname, password)
    clear_text(hostname_entry, password_entry)
    populate_list(router)


def remove_User(Name, hostname_entry, router):
    if Name == '':
        messagebox.showerror("Error", "No user chosen")
    else:
        Database.Delete_User(Name)
        clear_tex2(hostname_entry)
        populate_list(router)

def Database_Add(User, Password):
    if len(User) < 3:
        messagebox.showerror("Error", "Name must contain atleast 3 characters")
    elif len(Password) < 3:
        messagebox.showerror("Error", "Password must contain atleast 3 characters")
    else:
        Database.insert_to_database(User, Password)



def Error_Handle(Name):
    messagebox.showerror("Error", "User with  name" + " " + Name +" " + "already exists")

def Database_Delete_User(Name,window):
    Database.Delete_User(Name)
    window.destroy()
def Show_All_Users():
    Database.Show_All_Database()
def Back():
    InsideApp.InsideApp()

def populate_list(router_tree_view, hostname=''):
    for i in router_tree_view.get_children():
        router_tree_view.delete(i)
    for row in Database.fetch(hostname):
        router_tree_view.insert('', 'end', values=row)
def clear_text(hostname,password):
    hostname.delete(0, END)
    password.delete(0, END)

def clear_tex2(hostname):
    hostname.delete(0, END)


def search_hostname(router, hostname):
    populate_list(router, hostname)

