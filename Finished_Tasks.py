import sqlite3

conn = sqlite3.connect('finished_tasks.db')
# Create a table to hold the image data
conn.execute('''CREATE TABLE IF NOT EXISTS finished_tasks
                 (name text, description text, creation_date text, due_date text, employee text, finished_date text, pdf text)''')
conn.commit()


def insert_task(task_name, task_description, task_creation_date, task_due_date, task_employee, task_finished_date,pdf_file):
    c = conn.cursor()
    c.execute("INSERT INTO finished_tasks VALUES (?, ?, ?, ?, ?,?,?)",
              (task_name, task_description, task_creation_date, task_due_date, task_employee,task_finished_date,pdf_file))
    conn.commit()