import io
import sqlite3 as sq3
from tkinter import messagebox, filedialog, Label

from PIL import Image, ImageTk

import User_Manage
idp = 1
# def databaseforscripts():
#     con = sq3.connect("scripts.db")
#     cur = con.cursor()
#     cur.execute("""CREATE TABLE Scripts(
#                     id INT ,
#                     Option Char(25),
#                     Name CHAR(50),
#                     Text String(500));
#                     """)

conn = sq3.connect('scripts.db')

# Create a table to hold the image data
conn.execute('''
    CREATE TABLE IF NOT EXISTS scripts
    (id ,
     
     Name CHAR(25),
     Text String (500));
''')
conn.commit()

def deleteScript(Name):

    cur = conn.cursor()
    cur.execute("DELETE FROM Scripts WHERE Name = ?", [Name])
    conn.commit()


def databaseforscriptsinsert( Name, Text):

    if Name == '':
        messagebox.showerror("Error", "Name must be provided and Option selected")

    if Name == "default":
        messagebox.showerror("Error", "Name 'default' is reserved")
    else:
        global idp
        cur = conn.cursor()
        cur.execute("INSERT INTO Scripts (id, Name, Text) VALUES (?,?,?)", (idp, Name, Text))

        # cur.execute("INSERT INTO Users (id, Name, Password) VALUES (?,?,?)", (id, Name, Password))
        idp +=1
        conn.commit()
def databaseforscriptsread(Name, number):
    try:
        cur = conn.cursor()
        # cur.execute("SELECT ? FROM Data where ?=?", (column, goal, constrain,))
        cur.execute("Select Text FROM Scripts WHERE Name = ? and  id = ?", [Name, number])

        data = cur.fetchone()[0]

        return str(data)
    except:
        return

def fetchscript( hostname=''):

    cur = conn.cursor()
    cur.execute("SELECT Name FROM Scripts WHERE Name LIKE ?", ('%'+hostname+'%',))
    rows = cur.fetchall()
    m = [*set(rows)]
    print (m)
    return m














