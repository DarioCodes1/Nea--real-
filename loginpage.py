import tkinter
from tkinter import messagebox
import sqlite3 

window = tkinter.Tk()
window.title('Login Page')
window.geometry('750x500')
window.configure(bg='#467D6F')

def createdatabase():
    conn = sqlite3.connect('Login details.db')
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users(
                       id INTEGER PRIMARY KEY AUTOINCREMENT
                       username TEXT NOT NULL,
                       password TEXT NOT NULL
                    )
        ''')
    conn.commit()
    conn.close()
                
def new_user(username, password):
    conn = sqlite3.connect("Login details.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users(username, password) VALUES (?,?)',(username, password))
    conn.commit()
    conn.close()
    print("hello")

window.mainloop()
