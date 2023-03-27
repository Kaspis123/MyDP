import sqlite3 as sq3

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
