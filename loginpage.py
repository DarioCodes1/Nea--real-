import tkinter
from tkinter import messagebox
import sqlite3 

window = tkinter.Tk() #Initialise the window
window.title('Login Page') #Title the Window
window.geometry('750x500') #Give the dimensions of the desired window
window.configure(bg='#467D6F') #Give the background a colour

frame = tkinter.Frame(bg="#467D6F")

def new_user(username, password):
    conn = sqlite3.connect("Login details.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users(username, password) VALUES (?,?)',(username, password)) #Add a new username and password for a new user
    conn.commit() #Save changes to database
    conn.close() #Close database

def create_login_page():
    create_login_page = tkinter.Tk()
    create_login_page.title("Create Login")
    create_login_page.geometry('750x500')
    create_login_page.configure(bg="#467D6F")
    
    #Create a frame for the widgets
    create_login_frame = tkinter.Frame(create_login_page, bg="#467D6F")

    #Creating widgets to create an account
    create_login_label = tkinter.Label(create_login_frame, text="Create Login", bg='#467D6F', fg="#AABF11", font=("Times New Roman", 25), pady=25)
    create_username_label = tkinter.Label(create_login_frame, text="Username", bg='#467D6F', fg="#FFFFFF", font=("Times New Roman", 12) ,pady=5)
    create_username_entry = tkinter.Entry(create_login_frame, font=("Times New Roman", 12))
    create_password_label = tkinter.Label(create_login_frame, text="Password", bg='#467D6F', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
    create_password_entry = tkinter.Entry(create_login_frame, show="*", font=("Times New Roman", 12))
    create_login_button = tkinter.Button(create_login_frame, text="Create Account", bg="#AABF11", fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=lambda: new_user(create_username_entry.get(), create_password_entry.get()))

    #Placing the wqidgets to create an account
    create_login_label.grid(row=0, column=5, columnspan=2)
    create_username_label.grid(row=1, column=5)
    create_username_entry.grid(row=1, column=6)
    create_password_label.grid(row=2, column=5)
    create_password_entry.grid(row=2, column=6)
    create_login_button.grid(row=3, column=5, columnspan =2)

    #Packing the frame onto the screen
    create_login_frame.pack()
    
    create_login_page.mainloop()
    
def login(): #function for logging in
    entered_username = username_entry.get()
    entered_password = password_entry.get()
    conn = sqlite3.connect('Login details.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM users WHERE username=?', (entered_username,))
    user_credentials = cursor.fetchone()
    if user_credentials and entered_password == user_credentials[1]:
        print("Successful login")
    else:
        print("Invalid username or password")

def check_username_and_password():
    if len(str(username_entry))<8:
        print("Username must be at least 8 characters")
    if len(str(password_entry))<8:
        print("password must be at least 8 characters")

def on_login_button_click():
    check_username_and_password()
    login()

def on_open_create_login_click():
    create_login_page()

#Creating widgets for the login
login_label = tkinter.Label(frame, text="Login", bg='#467D6F', fg="#AABF11", font=("Times New Roman", 25), pady=25)
username_label = tkinter.Label(frame, text="Username", bg='#467D6F', fg="#FFFFFF", font=("Times New Roman", 12) ,pady=5)
username_entry = tkinter.Entry(frame, font=("Times New Roman", 12))
password_label = tkinter.Label(frame, text="Password", bg='#467D6F', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
password_entry = tkinter.Entry(frame, show="*", font=("Times New Roman", 12))
login_button = tkinter.Button(frame, text="Login", bg="#AABF11", fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=on_login_button_click)

no_account_label = tkinter.Label(frame, text="Not got an account? Create one!", bg='#467D6F', fg="#FFFFFF", font=("Times New Roman", 12) ,pady=5)
create_login_button = tkinter.Button(frame, text="Create Account", bg="#AABF11", fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=on_open_create_login_click)

#Placing the widgets on the fisrt page
login_label.grid(row=0, column=0, columnspan=2)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1)
login_button.grid(row=3, column=0, columnspan =2)

no_account_label.grid(row=2, column=4)
create_login_button.grid(row=3, column=4, columnspan =2)

frame.pack()

def createdatabase():
    conn = sqlite3.connect('Login details.db') 
    cursor = conn.cursor() 
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT NOT NULL,
                       password TEXT NOT NULL
                    )
        ''') #Create database 
    conn.commit() #Save changes to database
    conn.close() #Close database 

createdatabase()

window.mainloop() #Refresh the page (run the code)