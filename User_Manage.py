
from tkinter import messagebox
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import Database_teams
import InsideApp
import customtkinter

def Managemet():
    window = customtkinter.CTk()
    window.title("Management")
    window.resizable(False,False)
    window_width = 700
    window_height = 500
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    z = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"{window_width}x{window_height}+{z}+{y}")


    btn = customtkinter.CTkButton(window,text="Back", command=lambda: backbuttonfunctions(window))

    btn.pack(anchor="nw", padx=10, pady=10)

    # Create a label and entry for searching by name
    search_frame = customtkinter.CTkFrame(window)
    search_frame.pack(side="top", fill="x", padx=10, pady=(20, 10))

    lbl_search = customtkinter.CTkLabel(search_frame, text='Search by Name', font=customtkinter.CTkFont(size=15, weight="normal"))
    lbl_search.pack(side="left", padx=100, pady=10)

    hostname_search = tk.StringVar()
    hostname_search_entry = customtkinter.CTkEntry(search_frame, textvariable=hostname_search, width=100)
    hostname_search_entry.pack(side="left", padx=(0,50), pady=10)

    search_btn = customtkinter.CTkButton(search_frame, text='Search', width=12,
                           command=lambda: update_Listbox2(hostname_search_entry.get()))
    search_btn.pack(side="left", padx=10, pady=10)

    # Create a listbox with a scrollbar for displaying user information
    frame = customtkinter.CTkFrame(window)
    frame.pack(side="top", expand=True, fill="both", padx=10, pady=10)



    scrollbar = tk.Scrollbar(frame, orient="vertical")
    scrollbar.pack(side="left", fill="y")

    listbox = tk.Listbox(frame, height=10, width=25, font=("Helvetica", 13), bd=2, bg="#323332",
                            selectbackground="#323332", highlightthickness=0, yscrollcommand=scrollbar.set, selectmode=BROWSE)
    listbox.pack(side="left", expand=False, fill="both", padx=10)

    scrollbar.config(command=listbox.yview)

    scrollbar2 = tk.Scrollbar(frame, orient="vertical")
    scrollbar2.pack(side="right", fill="y")
    listbox_teams = tk.Listbox(frame, height=10, width=25, font=("Helvetica", 13), bd=2, bg="#323332",
                               selectbackground="#323332", highlightthickness=0,
                               selectmode=BROWSE,justify="center",yscrollcommand=scrollbar2.set)
    listbox_teams.pack(side="right", expand=False, fill="both", padx=20,)
    scrollbar2.config(command=listbox_teams.yview)

    # Create a frame for the add and delete user buttons
    button_frame = customtkinter.CTkFrame(window)
    button_frame.pack(side="bottom", fill="x", padx=10, pady=10)

    btn_add_user = customtkinter.CTkButton(button_frame, width= 50, text="Add User", command=lambda: open_new_window())
    btn_add_user.pack(side="left", padx=10, pady=10)

    btn_del_user = customtkinter.CTkButton(button_frame,width= 50, text="Delete User", command=lambda: open_new_delete())
    btn_del_user.pack(side="left", padx=10, pady=10)
    btn_add_user_to_team = customtkinter.CTkButton(button_frame,width= 50, text="Add User to Existing Team", command=lambda: add_user_to_team())
    btn_add_user_to_team.pack(side="left", padx=10, pady=10)


    btn_add_team = customtkinter.CTkButton(button_frame,text="Add Team",width= 50, command= lambda: add_team())
    btn_add_team.pack(side= "right",padx=(10), pady=10 )
    btn_del_team = customtkinter.CTkButton(button_frame,text="Delete Team" ,command= lambda: del_team())
    btn_del_team.pack(side= "right",padx=10, pady=10 )
    listbox_teams.bind('<Double-1>', lambda event: show_team_members(listbox_teams.get(ANCHOR)))


    def update_listbox():
        listbox.delete(0, tk.END)
        listbox.configure(fg="#d7d6d7")
        listbox.insert(0, 'ID   Name')
        for row in Database_teams.conn.execute('SELECT id, name FROM members'):
            listbox.insert(tk.END, f'{row[0]:<3} {row[1]}')

    update_listbox()


    def Add_User(hostname, password,new_window, team_dropdown):
        if hostname == '' or password == '':
            messagebox.showerror('Required Fields', 'Please include all fields')
            return

        x = Database_Add(hostname, password)
        if x != 0:

            c = Database_teams.conn.cursor()
            if len(team_dropdown) == 0:
                team_dropdown = "Teamless"
            c.execute('SELECT team_id FROM Teams WHERE team_name=?', (team_dropdown,))
            team_id = c.fetchone()[0]
            c.execute('INSERT INTO Users (user_name, team_id) VALUES (?, ?)', (hostname, team_id))
            p=Database_teams.conn
            p.commit()

            update_listbox()
            new_window.destroy()
        else:
            new_window.lift()

    def remove_User(Name, new_window):

        p = Database_teams.is_last_user_in_team(Name)
        if Database_teams.user_exists(Name) != 0:
            messagebox.showerror("Error", "No user found")
        elif p == True:
            messagebox.showerror("Error", "Last person in management")
        else:
            Database_teams.delete_user_from_team(Name)
            Database_teams.delete_user(Name)
            update_listbox()
            new_window.destroy()



    def open_new_window():
        # Create a new window
        new_window = customtkinter.CTkToplevel(window)
        new_window.resizable(False,False)
        new_window.title("Add User")
        window_width = 280
        window_height = 180
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Add labels and entry fields for name and password
        name_label = customtkinter.CTkLabel(new_window, text="Name:")
        name_entry = customtkinter.CTkEntry(new_window)
        password_label = customtkinter.CTkLabel(new_window, text="Password:")
        password_entry = customtkinter.CTkEntry(new_window, show="*")
        team_entry = customtkinter.CTkEntry(new_window)

        # Add a button to save the data and close the window
        save_button = customtkinter.CTkButton(new_window, text="Add", command=lambda :Add_User(name_entry.get(),password_entry.get(),new_window,team_dropdown.get()))


        # Grid the labels, entry fields, and button
        name_label.grid(row=0, column=0, padx=10, pady=10)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        password_label.grid(row=1, column=0, padx=10, pady=10)
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        team_label = customtkinter.CTkLabel(new_window, text="Team:")
        team_label.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)

        teams = Database_teams.conn.execute("SELECT * FROM Teams").fetchall()
        team_names = [team[1] for team in teams]
        team_dropdown = customtkinter.CTkComboBox(new_window, values=team_names)
        team_dropdown.grid(column=1, row=2, padx=10, pady=5, sticky=tk.W)

        team_label.grid(row=2, column=0, padx=10, pady=10)
        team_entry.grid(row=2, column=1, padx=10, pady=10)



        save_button.grid(row=3, column=0, columnspan=2, padx=(70, 0), pady=(5, 0))
        new_window.attributes("-topmost", True)
    def open_new_delete():
        # Create a new window
        new_window = customtkinter.CTkToplevel(window)
        new_window.resizable(False,False)
        new_window.title("Delete User")
        window_width = 210
        window_height = 100
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Add labels and entry fields for name and password
        name_label = customtkinter.CTkLabel(new_window, text="Name:")
        name_entry = customtkinter.CTkEntry(new_window)


        # Add a button to save the data and close the window
        save_button = customtkinter.CTkButton(new_window, text="Delete", command=lambda :remove_User(name_entry.get(),new_window))

        # Grid the labels, entry fields, and button
        name_label.grid(row=0, column=0, padx=10, pady=10)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        save_button.grid(row=2, column=0, columnspan=2, padx=(45,0), pady=10)
        new_window.attributes("-topmost", True)

    def Database_Add(User, Password):
        if len(User) < 3:
            messagebox.showerror("Error", "Name must contain atleast 3 characters")
            return 0
        elif len(Password) < 3:
            messagebox.showerror("Error", "Password must contain atleast 3 characters")
            return 0
        else:
           p = Database_teams.insert_user(User, Password)
           if p == 0:
               messagebox.showerror("Error","User with this name exists")
               return 0


    def update_Listbox2(Name):
        listbox.delete(0, tk.END)
        listbox.configure(fg="#d7d6d7")
        listbox.insert(0, 'ID   Name')

        cur = Database_teams.conn.cursor()
        cur.execute('SELECT id, name FROM members WHERE name=?', (Name,))
        rows = cur.fetchall()
        for row in rows:
            listbox.insert(tk.END, f'{row[0]:<3} {row[1]}')

    def update_listbox_team():
        listbox_teams.configure(fg="#d7d6d7")
        listbox_teams.delete(0, tk.END)

        listbox_teams.insert(0, 'Teams')
        listbox_teams.insert(0, 'Default')
        cur = Database_teams.conn.cursor()
        cur.execute("Select team_name from TEAMS")
        rows = cur.fetchall()
        for row in rows:
            listbox_teams.insert(tk.END, row)


    update_listbox_team()
    def Back():
        InsideApp.InsideApp()

    def backbuttonfunctions(window):
        window.destroy()
        Back()

    def add_team():

        new_window = customtkinter.CTkToplevel(window)
        new_window.resizable(False, False)
        new_window.title("Add Team")
        window_width = 250
        window_height = 100
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Add labels and entry fields for name and password
        name_label = customtkinter.CTkLabel(new_window, text="Name:")
        name_entry = customtkinter.CTkEntry(new_window)
        save_button = customtkinter.CTkButton(new_window, text="Add", command=lambda: add_team_to_database(name_entry.get(), new_window))

        # Grid the labels, entry fields, and button
        name_label.grid(row=0, column=0, padx=10, pady=10)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        save_button.grid(row=2, column=0, columnspan=2, padx=(55, 0), pady=10)
        new_window.attributes("-topmost", True)

    def add_team_to_database(team_name, window4):

        x = Database_teams.insert_team(team_name)
        if x ==0:
            messagebox.showerror("Error", " Team with name " + team_name + " exists!")
        else:
            update_listbox_team()
            window4.destroy()



    def show_team_members(team_name):
        # Get the team name from the selected item in the team Listbox

        if team_name == "Default":
            update_listbox()
            return
        if team_name == "Teams":

            return
        team_name = team_name[0]


        # Clear the members Listbox
        listbox.delete(0, 'end')

        # Get the members of the team from the database
        members = get_team_members(team_name)
        team_name_str = f"{team_name:^47}"
        listbox.insert(0, team_name_str)
        # Populate the members Listbox with the members of the team
        for member in members:
            listbox.insert('end', member[0])



    def del_team():
        new_window = customtkinter.CTkToplevel(window)
        new_window.resizable(False, False)
        new_window.title("Delete Team")
        window_width = 250
        window_height = 100
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Add labels and entry fields for name and password
        name_label = customtkinter.CTkLabel(new_window, text="Name:")
        name_entry = customtkinter.CTkEntry(new_window)

        teams = Database_teams.conn.execute("SELECT * FROM Teams").fetchall()
        team_names = [team[1] for team in teams]
        team_dropdown = customtkinter.CTkComboBox(new_window, values=team_names)
        team_dropdown.grid(column=1, row=0, padx=10, pady=5, sticky=tk.W)
        save_button = customtkinter.CTkButton(new_window, text="Delete",
                                command=lambda: delete_team_from_database(team_dropdown.get(), new_window))


        # Grid the labels, entry fields, and button
        name_label.grid(row=0, column=0, padx=10, pady=10)
        name_entry.grid(row=0, column=1, padx=10, pady=10)

        save_button.grid(row=2, column=0, columnspan=2, padx=(55, 0), pady=10)
        new_window.attributes("-topmost", True)
    def delete_team_from_database(team_name,windwod):
        if team_name == "Management":
            messagebox.showerror('Error', 'Management team can not be deleted')
        else:
            Database_teams.delete_team(team_name)
            windwod.destroy()
            update_listbox_team()

    def add_user_to_team():
        new_window = customtkinter.CTkToplevel()
        new_window.resizable(False, False)
        new_window.title("Add User to Team")
        window_width = 250
        window_height = 150
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Add labels and entry fields for name and password
        name_label = customtkinter.CTkLabel(new_window, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=10)

        names = Database_teams.conn.execute("SELECT * FROM Users").fetchall()
        list_names = [name[1] for name in names]
        list_dropdown = customtkinter.CTkComboBox(new_window, values=list_names)
        list_dropdown.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)



        # Add a button to save the data and close the window
        save_button = customtkinter.CTkButton(new_window, text="Add",
                                command=lambda: usertodatabase(team_dropdown.get(),list_dropdown.get(),new_window))

        # Grid the labels, entry fields, and button


        team_label = customtkinter.CTkLabel(new_window, text="Team:")
        team_label.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)

        teams = Database_teams.conn.execute("SELECT * FROM Teams").fetchall()
        team_names = [team[1] for team in teams]
        team_dropdown = customtkinter.CTkComboBox(new_window, values=team_names)
        team_dropdown.grid(column=1, row=2, padx=5, pady=5, sticky=tk.W)


        save_button.grid(row=3, column=0, columnspan=2, padx=(50, 0), pady=(5, 0))
        new_window.attributes("-topmost", True)
    window.mainloop()
def get_team_members(team_name):


    c = Database_teams.conn.execute("SELECT team_id FROM Teams WHERE team_name=?",
              (team_name,))  # pass team_name as a tuple with str()
    team_id = c.fetchone()[0]

    # Get the members of the team from the database
    c.execute("SELECT user_name FROM Users WHERE team_id=?", (team_id,))
    members = c.fetchall()
    print(members)

    return members

def usertodatabase(team, list,window):
    p = Database_teams.add_user_to_team(team, list)
    if p == 0:
        messagebox.showerror("Error", "Admin must stay in team Management")
    window.destroy()