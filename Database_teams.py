import sqlite3 as sq3
from tkinter import messagebox, filedialog

import Database_users
import NewQ
from User_Manage import get_team_members

conn = sq3.connect('teams.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Teams
             (team_id INTEGER PRIMARY KEY,
              team_name TEXT)''')


c.execute('''CREATE TABLE IF NOT EXISTS Users
             (user_id INTEGER PRIMARY KEY,
              user_name TEXT,
              team_id INTEGER,
              FOREIGN KEY (team_id)
                REFERENCES Teams(team_id))''')

c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (name text, description text, creation_date text, due_date text, employee text, viewed bool, pdf text)''')

c.execute('''
    CREATE TABLE IF NOT EXISTS members
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     name CHAR(25),
     password CHAR(25));
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS images
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT,
     data BLOB,
     skript TEXT);
''')

c.execute("CREATE TABLE IF NOT EXISTS tree (id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, value INTEGER)")

def insert_team(team_name):
    c.execute("INSERT INTO Teams (team_name) VALUES (?)", (team_name,))
    conn.commit()


def delete_team(team_name):
    # Get the team_id of the team to be deleted
    c.execute("SELECT team_id FROM Teams WHERE team_name = ?", (team_name,))
    result = c.fetchone()
    if result is None:
        print(f"Team '{team_name}' does not exist.")
        return

    team_id = result[0]

    # Delete the team from the Teams table
    c.execute("DELETE FROM Teams WHERE team_id = ?", (team_id,))

    # Delete all users that belong to the team from the Users table
    c.execute("DELETE FROM Users WHERE team_id = ?", (team_id,))

    # Commit the changes to the database
    conn.commit()


def add_user_to_team(selected_team, selected_user):
    # Get the selected user and team from their respective Listboxes

    c.execute('SELECT team_id FROM Teams WHERE team_name=?', (selected_team,))
    team_id = c.fetchone()[0]

    # Update the user's team ID in the database
    c.execute("UPDATE Users SET team_id=? WHERE user_name=?", (team_id, selected_user))
    conn.commit()

def delete_user_from_team(user_name):
    c.execute("DELETE FROM Users WHERE user_name=?", (user_name,))
    conn.commit()


def insert_task(task_name, task_description, task_creation_date, task_due_date, task_employee, pdf_name):
    c = conn.cursor()
    c.execute("SELECT name FROM tasks WHERE name=? ", (task_name,))
    check = c.fetchone()
    print(check)
    check2 = user_exists(task_employee)
    print(check2)
    if check != None:
        NewQ.error_task_name()
        return 0
    elif check2 == None:
        NewQ.error_user_name()
        return 1
    else:
        c.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?,?,?)",
              (task_name, task_description, task_creation_date, task_due_date, task_employee, False, pdf_name))
        conn.commit()
        return 2


def delete_task(task_name):
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE name=?", (task_name,))
    conn.commit()


def get_new_tasks(name1):


    c = conn.cursor()

    i=0
    c.execute("SELECT * FROM tasks WHERE employee=? AND viewed=False", (name1,))
    tasks = c.fetchall()
    for task in tasks:
        # Show popup message for new tasks
        # popup_message("New Task Assigned", f"You have a new task: {task[0]}.", "info")
        # Mark the task as viewed
        c.execute("UPDATE tasks SET viewed=True WHERE name=?", (task[0],))
        conn.commit()
        i+=1
    return i


def add_task_for_team(team_name, task_name, creation_date, task_description, task_due_date, pdf):
    # Get the members of the team from the database
    members = get_team_members(team_name)
    print(members)

    # Add the task for each member of the team
    for member in members:
        # Add the task to the tasks table for the member
        conn.execute('''INSERT INTO tasks (name, description, creation_date, due_date, employee, viewed, pdf)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', (task_name, task_description, creation_date, task_due_date, member[0], False, pdf))

    conn.commit()

def insert_user(name, password):
    # Check if the user already exists
    cursor = conn.execute('SELECT id FROM members WHERE name=?', (name,))
    if cursor.fetchone() is not None:
        return
    # Insert the new user
    conn.execute('INSERT INTO members (name, password) VALUES (?, ?)', (name, password))
    conn.commit()

def delete_user(name):
    # Check if the user exists
    cursor = conn.execute('SELECT id FROM members WHERE name=?', (name,))
    if cursor.fetchone() is None:
        print(f'User "{name}" not found in the database')
        return
    # Delete the user
    conn.execute('DELETE FROM members WHERE name = ?', (name,))
    conn.commit()
    print(f'User "{name}" deleted from the database')


def user_exists(name):
    print(name)
    cursor = conn.execute("SELECT name FROM members WHERE name=? ", (name,))
    check = cursor.fetchone()
    print(check)
    if check != None:
        return 0
    conn.commit()


def insert_image(skript):
    try:
        # Open a file dialog and get the selected file path
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

        # Load the image file using the PIL library
        with open(file_path, 'rb') as f:
            data = f.read()

        # Extract the filename from the path
        file_name = file_path.split("/")[-1]  # For Unix-based systems
        # file_name = file_path.split("\\")[-1]  # For Windows
        print(file_name)

        # Check if the image already exists in the database
        cur = conn.cursor()
        cur.execute('SELECT * FROM images WHERE name = ?', (file_name,))
        if cur.fetchone() is not None:
            # Display an error message if the image already exists
            messagebox.showerror("Error", "An image with the same name already exists in the database!")
            return

        # Insert the image data into the database
        conn.execute('INSERT INTO images (name, data, skript) VALUES (?, ?, ?)', (file_name, data, skript))
        conn.commit()

        # Display a success message
        messagebox.showinfo("Success", "Image inserted successfully!")

    except FileNotFoundError:
        # Display an error message if the file was not found
        messagebox.showerror("Error", "File not found!")

    except Exception as e:
        # Display an error message for all other exceptions
        messagebox.showerror("Error", f"Error: {e}")

def delete_image_from_db(name):
    # Delete the selected image from the database
    cur = conn.cursor()
    cur.execute('DELETE FROM images WHERE name = ?', (name,))
    conn.commit()

class Node:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
def insert_node_to_database(parent_id, name, value):
    c.execute("INSERT INTO tree (parent_id, name, value) VALUES (?, ?, ?)", (parent_id, name, value))

def get_node_from_database(value):
    c.execute("SELECT name FROM tree WHERE value=? ", (value))
