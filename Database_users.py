
import sqlite3 as sq3

conn = sq3.connect('users.db')

# Create a table to hold the users data
conn.execute('''
    CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
     name CHAR(25),
     password CHAR(25));
''')

# Function to insert a user into the database
def insert_user(name, password):
    # Check if the user already exists
    cursor = conn.execute('SELECT id FROM users WHERE name=?', (name,))
    if cursor.fetchone() is not None:
        return
    # Insert the new user
    conn.execute('INSERT INTO users (name, password) VALUES (?, ?)', (name, password))
    conn.commit()

def delete_user(name):
    # Check if the user exists
    cursor = conn.execute('SELECT id FROM users WHERE name=?', (name,))
    if cursor.fetchone() is None:
        print(f'User "{name}" not found in the database')
        return
    # Delete the user
    conn.execute('DELETE FROM users WHERE name = ?', (name,))
    conn.commit()
    print(f'User "{name}" deleted from the database')
