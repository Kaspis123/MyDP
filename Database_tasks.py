import sqlite3

conn = sqlite3.connect('tasks.db')
# Create a table to hold the image data
conn.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (name text, description text, creation_date text, due_date text, employee text, viewed bool)''')
conn.commit()


def insert_task(task_name, task_description, task_creation_date, task_due_date, task_employee):
    c = conn.cursor()
    c.execute("INSERT INTO tasks VALUES (?, ?, ?, ?, ?,?)",
              (task_name, task_description, task_creation_date, task_due_date, task_employee, False))
    conn.commit()


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




