import tkinter
from tkinter import messagebox
import sqlite3 
import random

window = tkinter.Tk() #Initialise the window
window.title('Login Page') #Title the Window
window.geometry('750x500') #Give the dimensions of the desired window
window.configure(bg='#467D6F') #Give the background a colour

frame = tkinter.Frame(bg="#467D6F")

def change_password(username, old_password, new_password):
    total_upper = 0
    conn = sqlite3.connect('Login details.db')
    cursor = conn.cursor()
    for i in new_password:
        if i.isupper() == True:
            total_upper = total_upper + 1
        else:
            pass
    total_upper = sum(1 for i in new_password if i.isupper())

    # Check if the username and old password match
    cursor.execute('SELECT username, password FROM users WHERE username=? AND password=?', (username, old_password))
    user_credentials = cursor.fetchone()

    sure = messagebox.askquestion("Ask Question","Are you sure you would like to delete your account? There is no going back", icon="info")
    if sure == "yes":
        if user_credentials:
            if total_upper == 0: # Checking if there is at least 1 capital letter or not
             messagebox.showerror("Invalid password", "Password must contain at least 1 upper case letter", icon="error")
            elif len(new_password) < 8: # Checking if there are at least 8 characters or not
                messagebox.showerror("Invalid password", "Password must be at least 8 characters or longer", icon="error")
            else:
                cursor.execute('UPDATE users SET password=? WHERE username=?', (new_password, username))
                conn.commit()
                conn.close()
                messagebox.showinfo("Password Changed", "Password has been changed successfully!", icon="info")
        else:
            conn.close()
            messagebox.showerror("Change Password Failed", "Invalid username or old password.", icon="error")
    else:
        pass

def change_password_page():
    change_password_window = tkinter.Tk()
    change_password_window.title("Change Password")
    change_password_window.geometry('400x300')
    change_password_window.configure(bg="#467D6F")

    #Creating a frame
    change_password_frame = tkinter.Frame(change_password_window, bg="#467D6F")

    # Creating widgets for changing password
    username_label = tkinter.Label(change_password_frame, text="Username", bg='#467D6F', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
    username_entry = tkinter.Entry(change_password_frame, font=("Times New Roman", 12))
    old_password_label = tkinter.Label(change_password_frame, text="Old Password", bg='#467D6F', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
    old_password_entry = tkinter.Entry(change_password_frame, show="*", font=("Times New Roman", 12))
    new_password_label = tkinter.Label(change_password_frame, text="New Password", bg='#467D6F', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
    new_password_entry = tkinter.Entry(change_password_frame, show="*", font=("Times New Roman", 12))
    change_password_button = tkinter.Button(change_password_frame, text="Change Password", bg="#AABF11", fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=lambda: change_password(username_entry.get(), old_password_entry.get(), new_password_entry.get()))

    # Placing the widgets
    username_label.grid(row=0, column=0)
    username_entry.grid(row=0, column=1)
    old_password_label.grid(row=1, column=0)
    old_password_entry.grid(row=1, column=1)
    new_password_label.grid(row=2, column=0)
    new_password_entry.grid(row=2, column=1)
    change_password_button.grid(row=3, column=0, columnspan=2)

    # Packing the frame onto the screen
    change_password_frame.pack()
    change_password_window.mainloop()

def on_change_password_click():
    change_password_page()

def new_user(username, password):
    total_upper = 0
    conn = sqlite3.connect('Login details.db')
    cursor = conn.cursor()
    for i in password:
        if i.isupper() == True:
            total_upper = total_upper + 1
        else:
            pass
    total_upper = sum(1 for i in password if i.isupper())
    conn = sqlite3.connect('Login details.db')
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute('SELECT username, password FROM users WHERE username=?', (username,))
    existing_username = cursor.fetchone()
    if existing_username:
        messagebox.showerror("Username already exists", "The entered username already exists. Please choose a different username.", icon="error")
    elif total_upper == 0:
        messagebox.showerror("Invalid password", "Password must contain at least 1 upper case letter", icon="error")
    elif len(password) < 8:
        messagebox.showerror("Invalid password", "Password must be at least 8 characters or longer", icon="error")
    elif len(username) < 5:
        messagebox.showerror("Invalid username", "Username must be at least 5 characters or longer", icon="error")
    else:
        conn = sqlite3.connect("Login details.db")
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users(username, password) VALUES (?,?)',(username, password)) #Add a new username and password for a new user
        conn.commit() #Save changes to database
        conn.close() #Close database

def now_logged_in():
    global now_logged_in
    now_logged_in = tkinter.Tk() #Initialising window
    now_logged_in.title("Logged in")
    now_logged_in.geometry('750x500')
    now_logged_in.configure(bg="#467D6F")
    
    #Creating a frame
    now_logged_in_frame = tkinter.Frame(now_logged_in, bg="#467D6F")

    #Adding data (widgets) now that you are logged in
    logged_in_title = tkinter.Label(now_logged_in_frame, text="THE MACHINE ", bg='#467D6F', fg="#AABF11", font=("Times New Roman", 25), pady=25)
    logged_in_pigeon = tkinter.Label(now_logged_in_frame, text="Pigeon Count: ", bg='#467D6F', fg="#AABF11", font=("Times New Roman", 12), pady=25)
    logged_in_fox = tkinter.Label(now_logged_in_frame, text="Fox Count: ", bg='#467D6F', fg="#AABF11", font=("Times New Roman", 12), pady=25)
    logged_in_human = tkinter.Label(now_logged_in_frame, text="Human Count: ", bg='#467D6F', fg="#AABF11", font=("Times New Roman", 12), pady=25)
    logged_in_delete_account = tkinter.Button(now_logged_in_frame, text="Delete Account", bg="#AABF11", fg="#FFFFFF", font=("Times New Roman", 12), pady=25, command=lambda: delete_account(entered_username, entered_password))

    #Place widgets onto the frame
    logged_in_title.grid(row=0, column=0, columnspan=2)
    logged_in_pigeon.grid(row=1, column=0, columnspan=2)
    logged_in_fox.grid(row=2, column=0, columnspan=2)
    logged_in_human.grid(row=3, column=0, columnspan=2)
    logged_in_delete_account.grid(row=0, column=5, columnspan=2)

    now_logged_in_frame.pack()

    now_logged_in.mainloop()

def delete_account(username, password): #Deletes account that you are logged in with
    sure = messagebox.askquestion("Ask Question","Are you sure you would like to delete your account? There is no going back", icon="info")
    
    if sure == "yes":
        conn = sqlite3.connect("Login details.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ? AND password = ?", (username, password))
        conn.commit()
        conn.close()
        now_logged_in.destroy()
    else:
        pass

def create_login_page():
    create_login_page = tkinter.Tk()
    create_login_page.title("Create Login")
    create_login_page.geometry('400x300')
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
    global entered_username
    entered_username = username_entry.get()
    global entered_password
    entered_password = password_entry.get()
    conn = sqlite3.connect('Login details.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM users WHERE username=?', (entered_username,))
    user_credentials = cursor.fetchone()
    if user_credentials and entered_password == user_credentials[1]:
        print("Successful login")
        now_logged_in()
    else:
        messagebox.showerror("Invalid username or password", "Try again")

def on_login_button_click():
    login()

def on_open_create_login_click():
    create_login_page()

#Creating widgets for the login
login_label = tkinter.Label(frame, text="Login", bg='#467D6F', fg="#AABF11", font=("Times New Roman", 25), pady=25)
username_label = tkinter.Label(frame, text="Username", bg='#467D6F', fg="#FFFFFF", font=("Times New Roman", 12) ,pady=5)
username_entry = tkinter.Entry(frame, font=("Times New Roman", 12))
password_label = tkinter.Label(frame, text="Password", bg='#467D6F', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
password_entry = tkinter.Entry(frame, show="*", font=("Times New Roman", 12))
no_account_label = tkinter.Label(frame, text="Not got an account? Create one!", bg='#467D6F', fg="#FFFFFF", font=("Times New Roman", 12) ,pady=5)
login_button = tkinter.Button(frame, text="Login", bg="#AABF11", fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=on_login_button_click)
create_login_button = tkinter.Button(frame, text="Create Account", bg="#AABF11", fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=on_open_create_login_click)
change_password_button = tkinter.Button(frame, text="Change Password", bg="#AABF11", fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=on_change_password_click)

#Placing the widgets on the fisrt page
login_label.grid(row=0, column=0, columnspan=2)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1)
login_button.grid(row=3, column=0, columnspan =2)
change_password_button.grid(row=3, column=2, columnspan=2)

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