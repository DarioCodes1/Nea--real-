from encryption import encrypt, decrypt
import tkinter
from tkinter import messagebox
import sqlite3 
import random
from captcha.image import ImageCaptcha
from PIL import Image
import numpy as np
import egcd

class LoginPage(tkinter.Tk):

    #Initialise variables for the class
    def __init__(self):
        super().__init__()
        self.title('Login Page')
        self.geometry('750x500')
        self.configure(bg='#161d29')

        #Create a frame to hold the widgets
        self.frame = tkinter.Frame(self, bg="#161d29")
        self.frame.pack()

        self.create_widgets() #Call the method to create widgets on the page

    #Method to create widgets for the login page
    def create_widgets(self):
        #Labels and buttons for username, password, captcha, and login being created
        login_label = tkinter.Label(self.frame, text="Login", bg='#161d29', fg="#444A53", font=("Times New Roman", 25), pady=25)
        username_label = tkinter.Label(self.frame, text="Username", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.username_entry = tkinter.Entry(self.frame, font=("Times New Roman", 12))
        password_label = tkinter.Label(self.frame, text="Password", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.password_entry = tkinter.Entry(self.frame, show="*", font=("Times New Roman", 12))
        no_account_label = tkinter.Label(self.frame, text="Not got an account? Create one!", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        login_button = tkinter.Button(self.frame, text="Login", bg="#444A53", fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=self.on_login_button_click)
        create_login_button = tkinter.Button(self.frame, text="Create Account", bg="#444A53", fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=self.on_open_create_login_click)
        change_password_button = tkinter.Button(self.frame, text="Change Password", bg="#444A53", fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=self.on_change_password_click)
        captcha_label = tkinter.Label(self.frame, text="Captcha", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.captcha_entry = tkinter.Entry(self.frame, font=("Times New Roman", 12))
        generate_captcha_button = tkinter.Button(self.frame, text="Generate Captcha", bg="#444A53", fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=self.generate_captcha)

        #Grid layout for the widgets
        create_login_button.grid(row=3, column=4, columnspan=2)
        login_label.grid(row=0, column=0, columnspan=2)
        username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1)
        password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1)
        login_button.grid(row=5, column=0, columnspan=2)
        change_password_button.grid(row=4, column=3, columnspan=2)
        self.captcha_entry.grid(row=3, column=1, columnspan=2)
        captcha_label.grid(row=3, column=0) 
        generate_captcha_button.grid(row=4, column=0, columnspan=2)

        no_account_label.grid(row=2, column=4)

    #Method to handle login button click
    def on_login_button_click(self):
        #Get the entered username, password, and captcha and check 
        username = self.username_entry.get()
        password = self.password_entry.get()
        captcha = self.captcha_entry.get()

        #Connect to the database
        conn = sqlite3.connect('Login details.db')
        cursor = conn.cursor()

        #Retrieve user credentials from the database
        cursor.execute('SELECT username, password FROM users WHERE username=?', (username,))
        user_credentials = cursor.fetchone()

        # Check if the entered credentials match the database and captcha is correct
        if user_credentials and password == decrypt(user_credentials[1]) and captcha == self.captcha_word:
            self.now_logged_in()
        else:
            messagebox.showerror("Try again", "Invalid username or password or captcha")

    #Method to open the create login page
    def on_open_create_login_click(self):
        create_login_page = CreateLoginPage(self)
        create_login_page.mainloop()

    #Method to open the change password page
    def on_change_password_click(self):
        change_password_page = ChangePasswordPage(self)
        change_password_page.mainloop()

    #Method to generate captcha
    def generate_captcha(self):
        #List of words for captcha
        word_list = [
            "Tiger",
            "Sunshine", 
            "Butterfly", 
            "Adventure", 
            "Serenity",
            "Harmony", 
            "Chocolate", 
            "Mystery", 
            "Rainbow", 
            "Whimsical",
            "Tranquility", 
            "Elegance", 
            "Enchantment", 
            "Radiance", 
            "Blissful",
            "Carousel", 
            "Delightful", 
            "Jubilant", 
            "Luminescent", 
            "Symphony"
            ]
        #Randomly select a word from the list
        captcha_index = random.randint(0, 19)
        self.captcha_word = word_list[captcha_index]

        #Generate captcha image
        captcha = ImageCaptcha(width=500, height=500, font_sizes=(40, 70, 100, 120))
        captcha.write(self.captcha_word, "captcha.png")

        #Open a captcha image
        captcha_image = Image.open("captcha.png")
        captcha_image.show()

    #method to open the now logged in page
    def now_logged_in(self):
        now_logged_in_page = NowLoggedInPage(self, self.username_entry.get(), self.password_entry.get())
        now_logged_in_page.mainloop()


class CreateLoginPage(tkinter.Tk):
    #Initialise the create login page
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.title("Create Login")
        self.geometry('400x300')
        self.configure(bg="#161d29")

        #Create widgets on the create login page
        self.create_widgets()

    #Method to create widgets on the create login page
    def create_widgets(self):
        create_login_frame = tkinter.Frame(self, bg="#161d29")

        #creating the labels, buttons and entries for the create login page 
        create_login_label = tkinter.Label(create_login_frame, text="Create Login", bg='#161d29', fg="#444A53", font=("Times New Roman", 25), pady=25)
        create_username_label = tkinter.Label(create_login_frame, text="Username", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.create_username_entry = tkinter.Entry(create_login_frame, font=("Times New Roman", 12))
        create_password_label = tkinter.Label(create_login_frame, text="Password", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.create_password_entry = tkinter.Entry(create_login_frame, show="*", font=("Times New Roman", 12))
        create_login_button = tkinter.Button(create_login_frame, text="Create Account", bg="#444A53", fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=self.create_account)

        #Grid layout for widgets
        create_login_label.grid(row=0, column=5, columnspan=2)
        create_username_label.grid(row=1, column=5)
        self.create_username_entry.grid(row=1, column=6)
        create_password_label.grid(row=2, column=5)
        self.create_password_entry.grid(row=2, column=6)
        create_login_button.grid(row=3, column=5, columnspan=2)

        create_login_frame.pack()

    #Method to create a new account
    def create_account(self):
        username = self.create_username_entry.get()
        password = self.create_password_entry.get()
        total_upper = sum(1 for i in password if i.isupper())

        #Connect to the database
        conn = sqlite3.connect('Login details.db')
        cursor = conn.cursor()

        #Check if username already exists
        cursor.execute('SELECT username, password FROM users WHERE username=?', (username,))
        existing_username = cursor.fetchone()

        #Validation for the username and password
        if existing_username:
            messagebox.showerror("The entered username already exists. Please choose a different username.", "Username already exists")
        elif total_upper == 0:
            messagebox.showerror("Password must contain at least 1 upper case letter", "Invalid password")
        elif len(password) < 8:
            messagebox.showerror("Password must be at least 8 characters or longer", "Invalid password")
        elif len(username) < 5:
            messagebox.showerror("Username must be at least 5 characters or longer", "Invalid username")
        else:
            cursor.execute('INSERT INTO users(username, password) VALUES (?,?)', (username, encrypt(password)))
            conn.commit()
            conn.close()
            messagebox.showinfo("Account Created", "Account created successfully!")
            self.destroy()

class ChangePasswordPage(tkinter.Tk):
    #Initialise the change password page
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.title("Change Password")
        self.geometry('400x300')
        self.configure(bg="#161d29")

        #Create widgets on the change password page
        self.create_widgets()

    #Method to create widgets on the change password page
    def create_widgets(self):
        change_password_frame = tkinter.Frame(self, bg="#161d29")

        username_label = tkinter.Label(change_password_frame, text="Username", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.username_entry = tkinter.Entry(change_password_frame, font=("Times New Roman", 12))
        old_password_label = tkinter.Label(change_password_frame, text="Old Password", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.old_password_entry = tkinter.Entry(change_password_frame, show="*", font=("Times New Roman", 12))
        new_password_label = tkinter.Label(change_password_frame, text="New Password", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.new_password_entry = tkinter.Entry(change_password_frame, show="*", font=("Times New Roman", 12))
        change_password_button = tkinter.Button(change_password_frame, text="Change Password", bg="#444A53", fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=self.change_password)

        #Grid layout for widgets
        username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        old_password_label.grid(row=1, column=0)
        self.old_password_entry.grid(row=1, column=1)
        new_password_label.grid(row=2, column=0)
        self.new_password_entry.grid(row=2, column=1)
        change_password_button.grid(row=3, column=0, columnspan=2)

        change_password_frame.pack()

    #Method to change password
    def change_password(self):
        #Get username, old password, and new password entered by the user
        username = self.username_entry.get()
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        total_upper = sum(1 for i in new_password if i.isupper())

        #Connect to the database
        conn = sqlite3.connect('Login details.db')
        cursor = conn.cursor()

        #Check if old username and password match
        cursor.execute('SELECT username, password FROM users WHERE username=? AND password=?', (username, encrypt(old_password)))
        user_credentials = cursor.fetchone()

        #Confirm password change
        sure = messagebox.askquestion("Ask Question", "Are you sure you would like to delete your account? There is no going back", icon="info")
        if sure == "yes":
            if user_credentials:
                #Validate new password
                if total_upper == 0:
                    messagebox.showerror("Invalid password", "Password must contain at least 1 upper case letter")
                elif len(new_password) < 8:
                    messagebox.showerror("Invalid password", "Password must be at least 8 characters or longer")
                else:
                    #Update password in the database
                    cursor.execute('UPDATE users SET password=? WHERE username=?', (encrypt(new_password), username))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Password Changed", "Password has been changed successfully!")
                    self.destroy()
            else:
                conn.close()
                messagebox.showerror("Change Password Failed", "Invalid username or old password.")
        else:
            pass


class NowLoggedInPage(tkinter.Tk):
    #Initialise the now logged in page
    def __init__(self, master, entered_username, entered_password):
        super().__init__()
        self.master = master
        self.title("Logged in")
        self.geometry('750x500')
        self.configure(bg="#161d29")
        self.entered_username = entered_username
        self.entered_password = entered_password
        #Create widgets on the now logged in page
        self.create_widgets()

    #Method to create widgets on the now logged in page
    def create_widgets(self):
        now_logged_in_frame = tkinter.Frame(self, bg="#161d29")

        #labels for the loggedin page
        logged_in_title = tkinter.Label(now_logged_in_frame, text="THE MACHINE ", bg='#161d29', fg="#444A53", font=("Times New Roman", 25), pady=25)
        logged_in_pigeon = tkinter.Label(now_logged_in_frame, text="Pigeon Count: ", bg='#161d29', fg="#444A53", font=("Times New Roman", 12), pady=25)
        logged_in_fox = tkinter.Label(now_logged_in_frame, text="Fox Count: ", bg='#161d29', fg="#444A53", font=("Times New Roman", 12), pady=25)
        logged_in_title = tkinter.Label(now_logged_in_frame, text="THE MACHINE ", bg='#161d29', fg="#444A53", font=("Times New Roman", 25), pady=25)
        logged_in_pigeon = tkinter.Label(now_logged_in_frame, text="Pigeon Count: ", bg='#161d29', fg="#444A53", font=("Times New Roman", 12), pady=25)
        logged_in_fox = tkinter.Label(now_logged_in_frame, text="Fox Count: ", bg='#161d29', fg="#444A53", font=("Times New Roman", 12), pady=25)
        logged_in_human = tkinter.Label(now_logged_in_frame, text="Human Count: ", bg='#161d29', fg="#444A53", font=("Times New Roman", 12), pady=25)
        logged_in_delete_account = tkinter.Button(now_logged_in_frame, text="Delete Account", bg="#444A53", fg="#FFFFFF", font=("Times New Roman", 12), pady=25, command=self.delete_account)

        #Grid layout for widgets
        logged_in_title.grid(row=0, column=0, columnspan=2)
        logged_in_pigeon.grid(row=1, column=0, columnspan=2)
        logged_in_fox.grid(row=2, column=0, columnspan=2)
        logged_in_human.grid(row=3, column=0, columnspan=2)
        logged_in_delete_account.grid(row=0, column=5, columnspan=2)

        now_logged_in_frame.pack()

    #Method to delete the account
    def delete_account(self):
        sure = messagebox.askquestion("Ask Question", "Are you sure you would like to delete your account? There is no going back", icon="info")

        if sure == "yes":
            # Connect to the database
            conn = sqlite3.connect("Login details.db")
            cursor = conn.cursor()
            # Remove user account from the database
            cursor.execute("DELETE FROM users WHERE username = ? AND password = ?", (self.master.username_entry.get(), encrypt(self.master.password_entry.get())))
            conn.commit()
            conn.close()
            self.destroy()
        else:
            pass

#Method to create the database
def create_database():
    conn = sqlite3.connect('Login details.db') 
    cursor = conn.cursor() 
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT NOT NULL,
                       password TEXT NOT NULL
                    )
        ''') 
    conn.commit()
    conn.close()

#Main method to create the database and start the login page
if __name__ == "__main__":
    create_database()
    window = LoginPage()
    window.mainloop()