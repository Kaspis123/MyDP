
import sqlite3 as sq3


def create_database():
    con = sq3.connect("users.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE Users(
                id INT PRIMARY KEY,
                Name CHAR(25), 
                Password CHAR(25));
                """)

def insert_to_database():
    con = sq3.connect("users.db")
    cur = con.cursor()
    # id = getmaxid()
    cur.execute("INSERT INTO Users VALUES('1', 'user', '123')")
    # cur.execute("INSERT INTO Users (id, Name, Password) VALUES (?,?,?)", (id, Name, Password))
    # cur.execute("INSERT INTO Users (id, Name, Password) VALUES (?,?,?)", (id, Name, Password))
    con.commit()

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



