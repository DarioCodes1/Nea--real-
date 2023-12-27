import tkinter
from tkinter import messagebox
import sqlite3 

window = tkinter.Tk() #Initialise the window
window.title('Login Page') #Title the Window
window.geometry('750x500') #Give the dimensions of the desired window
window.configure(bg='#467D6F') #Give the background a colour

frame = tkinter.Frame()

#Creating widgets
login_label = tkinter.Label(frame, text="Login", bg='#467D6F', fg="#AABF11", font=("Times New Roman", 25), pady=25)
username_label = tkinter.Label(frame, text="Username", bg='#467D6F', fg="#FFFFFF", font=("Times New Roman", 12) ,pady=5)
username_entry = tkinter.Entry(frame, font=("Times New Roman", 12))
password_label = tkinter.Label(frame, text="Password", bg='#467D6F', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
password_entry = tkinter.Entry(frame, show="*", font=("Times New Roman", 12))
button = tkinter.Button(frame, text="Login", bg="#AABF11", fg="#FFFFFF", font=("Times New Roman", 10), pady=5)

#Placing the widgets on the page
login_label.grid(row=0, column=0, columnspan=2)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1)
button.grid(row=3, column=0, columnspan =2)

frame.pack()


def createdatabase():
    conn = sqlite3.connect('Login details.db') 
    cursor = conn.cursor() 
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users(
                       id INTEGER PRIMARY KEY AUTOINCREMENT
                       username TEXT NOT NULL,
                       password TEXT NOT NULL
                    )
        ''') #Create database 
    conn.commit() #Save changes to database
    conn.close() #Close database 
                
def new_user(username, password):
    conn = sqlite3.connect("Login details.db") 
    cursor = conn.cursor() 
    cursor.execute('INSERT INTO users(username, password) VALUES (?,?)',(username, password)) #Add a new username and password for a new user
    conn.commit() #Save changes to database
    conn.close() #Close database

window.mainloop() #Refresh the page (run the code)
