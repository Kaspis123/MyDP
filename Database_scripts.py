
import sqlite3 as sq3



idp = 1
value = True
rodic = 1
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
    (id INT ,
     Name CHAR(25),
     Text String (1000),
     left String,
     right String,
     parent_id INT);
     
''')
conn.commit()

def deleteScript(Name):

    cur = conn.cursor()
    cur.execute("DELETE FROM Scripts WHERE Name = ?", [Name])
    conn.commit()


def databaseforscriptsinsert(Name, Text):

    cur = conn.cursor()
    global idp
    negative = "negative"
    positive = "positive"
    # if Name == '':
    #     messagebox.showerror("Error", "Name must be provided and Option selected")
    #
    # if Name == "default":
    #     messagebox.showerror("Error", "Name 'default' is reserved")
    if idp == 1:
        cur.execute("INSERT INTO Scripts (id, Name, Text) VALUES (?,?,?)",
                    (idp, Name, Text,))
        idp+=1
    elif value == True:
        cur.execute("INSERT INTO Scripts (id, Name, Text, left, parent_id) VALUES (?,?,?,?,?)", (idp, Name, Text,negative,rodic))
        print("Zadává se negativní věta, která má rodiče" + str(rodic))
        idp +=1
    else:
        cur.execute("INSERT INTO Scripts (id, Name, Text,right, parent_id) VALUES (?,?,?,?,?)", (idp, Name, Text,positive,rodic))
        print("Zadává se pozitivní věta, která má rodiče" + str(rodic))
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

def increate_idp():
    global idp
    idp+=1
    return idp



def set_flag(flag):
    global value
    value = flag

def set_number(parent):
    global rodic
    rodic = parent









