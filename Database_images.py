#
# import sqlite3 as sq3
# from tkinter import messagebox, filedialog
#
# conn = sq3.connect('images.db')
#
# # Create a table to hold the image data
# conn.execute('''
#     CREATE TABLE IF NOT EXISTS images
#     (id INTEGER PRIMARY KEY AUTOINCREMENT,
#      name TEXT,
#      data BLOB,
#      skript TEXT);
#
# ''')
# conn.commit()
#
# def insert_image(skript):
#     try:
#         # Open a file dialog and get the selected file path
#         file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
#
#         # Load the image file using the PIL library
#         with open(file_path, 'rb') as f:
#             data = f.read()
#
#         # Extract the filename from the path
#         file_name = file_path.split("/")[-1]  # For Unix-based systems
#         # file_name = file_path.split("\\")[-1]  # For Windows
#         print(file_name)
#
#         # Check if the image already exists in the database
#         cur = conn.cursor()
#         cur.execute('SELECT * FROM images WHERE name = ?', (file_name,))
#         if cur.fetchone() is not None:
#             # Display an error message if the image already exists
#             messagebox.showerror("Error", "An image with the same name already exists in the database!")
#             return
#
#         # Insert the image data into the database
#         conn.execute('INSERT INTO images (name, data, skript) VALUES (?, ?, ?)', (file_name, data, skript))
#         conn.commit()
#
#         # Display a success message
#         messagebox.showinfo("Success", "Image inserted successfully!")
#
#     except FileNotFoundError:
#         # Display an error message if the file was not found
#         messagebox.showerror("Error", "File not found!")
#
#     except Exception as e:
#         # Display an error message for all other exceptions
#         messagebox.showerror("Error", f"Error: {e}")
#
# def delete_image_from_db(name):
#     # Delete the selected image from the database
#     cur = conn.cursor()
#     cur.execute('DELETE FROM images WHERE name = ?', (name,))
#     conn.commit()