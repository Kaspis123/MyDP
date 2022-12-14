
import sqlite3 as sq3
from tkinter import messagebox

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

