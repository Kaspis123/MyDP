import sqlite3
from datetime import datetime

import NewQ
import Database_users
from User_Manage import get_team_members

conn = sqlite3.connect('tasks.db')
# Create a table to hold the image data
conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (name text, description text, creation_date text, due_date text, employee text, viewed bool)''')
conn.commit()


def insert_task(task_name, task_description, task_creation_date, task_due_date, task_employee):

    c = conn.cursor()
    c.execute("SELECT name FROM tasks WHERE name=? ", (task_name,))
    check = c.fetchone()
    print(check)
    check2 = Database_users.user_exists(task_employee)
    print(check2)
    if check != None:
        NewQ.error_task_name()
        return 0
    elif check2 == None:
        NewQ.error_user_name()
        return 1
    else:
        c.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?,?)",
              (task_name, task_description, task_creation_date, task_due_date, task_employee, False))
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


def add_task_for_team(team_name, task_name, task_description, task_due_date):
    # Get the members of the team from the database
    members = get_team_members(team_name)
    print(members)

    # Add the task for each member of the team
    for member in members:
        # Add the task to the tasks table for the member
        conn.execute('''INSERT INTO tasks (name, description, creation_date, due_date, employee, viewed)
                        VALUES (?, ?, ?, ?, ?, ?)''', (task_name, task_description, datetime.now(), task_due_date, member[0], False))

    conn.commit()



