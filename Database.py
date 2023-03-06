import io
import sqlite3 as sq3
from tkinter import messagebox, filedialog, Label

from PIL import Image, ImageTk

import User_Manage
id = 1
# def databaseforscripts():
#     con = sq3.connect("scripts.db")
#     cur = con.cursor()
#     cur.execute("""CREATE TABLE Scripts(
#                     id INT ,
#                     Option Char(25),
#                     Name CHAR(50),
#                     Text String(500));
#                     """)

conn = sq3.connect('images.db')

# Create a table to hold the image data
conn.execute('''
    CREATE TABLE IF NOT EXISTS images
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT,
     data BLOB);
''')
conn.commit()

def deleteScript(Name):
    con = sq3.connect("Scripts.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Scripts WHERE Name = ?", [Name])
    con.commit()


def databaseforscriptsinsert(Option,Name,Text):
    print(Name, Text)
    if Name == '' or Option == '':
        print ("nope")
    else:
        global id
        con = sq3.connect("scripts.db")
        cur = con.cursor()
        cur.execute("INSERT INTO Scripts (id, Option, Name, Text) VALUES (?,?,?,?)", (id, Option, Name, Text))

        # cur.execute("INSERT INTO Users (id, Name, Password) VALUES (?,?,?)", (id, Name, Password))
        id +=1
        con.commit()
def databaseforscriptsread(Name, number):
    con = sq3.connect("scripts.db")
    cur = con.cursor()
    # cur.execute("SELECT ? FROM Data where ?=?", (column, goal, constrain,))
    cur.execute("Select Text FROM Scripts WHERE Name = ? and  id = ?", [Name, number])
    print(cur.execute("Select Text FROM Scripts WHERE Name = ? and  id = ?", [Name, number]))
    data = cur.fetchone()[0]
    print(data)
    return str(data)



def create_database():
    con = sq3.connect("users.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE Users(
                id INT PRIMARY KEY,
                Name CHAR(25), 
                Password CHAR(25));
                """)

def insert_to_database(Name, Password):
    con = sq3.connect("users.db")
    cur = con.cursor()
    if Database_Check(Name) !=False:
        id = getmaxid()
        # cur.execute("INSERT INTO Users VALUES('1', 'user', '123')") ruční přidávání id nyní 1
        cur.execute("INSERT INTO Users (id, Name, Password) VALUES (?,?,?)", (id, Name, Password))
        # cur.execute("INSERT INTO Users (id, Name, Password) VALUES (?,?,?)", (id, Name, Password))
        con.commit()
    else:
        User_Manage.Error_Handle(Name)


def getmaxid():
    a = sq3.connect("users.db", detect_types=sq3.PARSE_DECLTYPES)
    cur = a.cursor()
    cur.execute("SELECT MAX(id) from Users")
    data = cur.fetchone()[0]
    try:
        return data + 1
    except:
        return 0

def get_data_from_database(Name, Password):
    con = sq3.connect("users.db")
    cur = con.cursor()
    cur.execute("Select Name  FROM Users WHERE Name = ?", [Name])
    try:
        records = cur.fetchone()[0]
    except:
        return False
    cur.execute("Select Password FROM Users WHERE Name = ?", [Name])
    try:
        records2 = cur.fetchone()[0]
    except:
        return False
    if Name == records:
        if Password == records2:
            return True
        else:
            return False


def Database_Check(Name):
    con = sq3.connect("users.db")
    cur = con.cursor()
    cur.execute("Select Name  FROM Users WHERE Name = ?", [Name])
    try:
        records = cur.fetchone()[0]
    except:
        return True
    if Name == records:
        return False
    else:
        return True

def Delete_User(Name):
    if Database_Check(Name) == True:
        messagebox.showerror("Error", "No such user exists")
    else:
        con = sq3.connect("users.db")
        cur = con.cursor()
        cur.execute("DELETE FROM Users WHERE Name = ?", [Name])
        con.commit()

def Show_All_Database():
    con = sq3.connect("users.db")
    cur = con.cursor()
    cur.execute("Select id,Name,Password  FROM Users")
    print(cur.fetchall())

def fetch( hostname=''):
    con = sq3.connect("users.db")
    cur = con.cursor()
    cur.execute(
            "SELECT * FROM Users WHERE Name LIKE ?", ('%'+hostname+'%',))
    rows = cur.fetchall()
    return rows

def fetchscript( hostname=''):
    con = sq3.connect("scripts.db")
    cur = con.cursor()
    cur.execute("SELECT Name FROM Scripts WHERE Name LIKE ?", ('%'+hostname+'%',))
    rows = cur.fetchall()
    m = [*set(rows)]
    print (m)
    return m


def insert_image():
    # Open a file dialog and get the selected file path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

    # Load the image file using the PIL library
    with open(file_path, 'rb') as f:
        data = f.read()

    # Extract the filename from the path
    file_name = file_path.split("/")[-1]  # For Unix-based systems
    # file_name = file_path.split("\\")[-1]  # For Windows
    print(file_name)


    # Insert the image data into the database
    conn.execute('INSERT INTO images (name, data) VALUES (?, ?)', (file_name, data))
    conn.commit()


def display_image(event, window):
    # Get the selected item from the listbox
    selection = event.widget.curselection()
    if selection:

            selected_item = event.widget.get(selection[0])

            # Query the database for the image data
            result = conn.execute('SELECT data FROM images WHERE name = ?', (selected_item,))

            # Load the image data into memory using the BytesIO class
            image_data = io.BytesIO(result.fetchone()[0])

            # Create a PIL Image from the loaded image data
            pil_image = Image.open(image_data)

            # Create a Tkinter PhotoImage from the PIL image
            photo = ImageTk.PhotoImage(pil_image)
            label = Label(window)
            label.pack()
            label.config(image=photo)
            label.image = photo

def delete_image_from_db(name):
    # Delete the selected image from the database
    con = sq3.connect("images.db")
    cur = con.cursor()
    cur.execute('DELETE FROM images WHERE name = ?', (name,))
    con.commit()











