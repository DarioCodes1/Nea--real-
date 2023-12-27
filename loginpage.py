import tkinter
from tkinter import messagebox
import sqlite3 

window = tkinter.Tk() #Initialise the window
window.title('Login Page') #Title the Window
window.geometry('750x500') #Give the dimensions of the desired window
window.configure(background='#467D6F') #Give the background a colour

#Creating widgets
login_label = tkinter.Label(window, text="Login", background='#467D6F')
username_label = tkinter.Label(window, text="Username", background='#467D6F')
username_entry = tkinter.Entry(window)
password_label = tkinter.Label(window, text="Password", background='#467D6F')
password_entry = tkinter.Entry(window)
button = tkinter.Button(window, text="Login")

#Placing the widgets on the page
login_label.grid(row=0, column=0, columnspan=2)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1)
button.grid(row=3, column=0, columnspan =2)



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
