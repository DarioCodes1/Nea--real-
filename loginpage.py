from encryption import encrypt, decrypt
import tkinter
from tkinter import messagebox
import sqlite3 
import random
from captcha.image import ImageCaptcha
from PIL import Image
import numpy as np
from display import open_camera_display
from Movement_Y import move_up, move_down
from Movement_X import move_left, move_right
import threading
from datetime import datetime

# Create a thread for the camera display function
camera_thread = threading.Thread(target=open_camera_display)

button_colour = "#2F7BA3" #Easier to change colours now as one variable can be changed to change the whole colour scheme

class LoginPage(tkinter.Tk):

    #Initialise variables for the class
    def __init__(self):
        super().__init__()
        self.title('Login Page')
        self.geometry('750x500')
        self.configure(bg='#161d29')
        self.attempt_login_count = 0
        #Create a frame to hold the widgets
        self.frame = tkinter.Frame(self, bg="#161d29")
        self.frame.pack()

        self.create_widgets() #Call the method to create widgets on the page

    #Method to create widgets for the login page
    def create_widgets(self):
        #Labels and buttons for username, password, captcha, and login being created
        self.login_label = tkinter.Label(self.frame, text="Login", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 25), pady=25)
        self.username_label = tkinter.Label(self.frame, text="Username", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.username_entry = tkinter.Entry(self.frame, font=("Times New Roman", 12))
        self.password_label = tkinter.Label(self.frame, text="Password", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.password_entry = tkinter.Entry(self.frame, show="*", font=("Times New Roman", 12))
        self.no_account_label = tkinter.Label(self.frame, text="Not got an account? Create one!", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.login_button = tkinter.Button(self.frame, text="Login", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=self.on_login_button_click)
        self.create_login_button = tkinter.Button(self.frame, text="Create Account", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=self.on_open_create_login_click)
        self.change_password_button = tkinter.Button(self.frame, text="Change Password", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=self.on_change_password_click)
        self.captcha_label = tkinter.Label(self.frame, text="Captcha", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.captcha_entry = tkinter.Entry(self.frame, font=("Times New Roman", 12))
        self.generate_captcha_button = tkinter.Button(self.frame, text="Generate Captcha", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=self.generate_captcha)
        self.too_many_login_attempts_label = tkinter.Label(self.frame, text="Too many login attempts! Wait 2 minutes to try again", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)

        #Grid layout for the widgets
        self.create_login_button.grid(row=3, column=4, columnspan=2)
        self.login_label.grid(row=0, column=0, columnspan=2)
        self.username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1)
        self.password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1)
        self.login_button.grid(row=5, column=0, columnspan=2)
        self.change_password_button.grid(row=4, column=3, columnspan=2)
        self.captcha_entry.grid(row=3, column=1, columnspan=2)
        self.captcha_label.grid(row=3, column=0) 
        self.generate_captcha_button.grid(row=4, column=0, columnspan=2)

        self.no_account_label.grid(row=2, column=4)

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
        cursor.execute('SELECT id, username, password FROM users WHERE username=?', (username,)) #Looking for the userID now
        user_credentials = cursor.fetchone()

        # Check if the entered credentials match the database and captcha is correct
        if user_credentials and password == decrypt(user_credentials[2]) and captcha == self.captcha_word: #changed as there is another field in the database table now
            global logged_in_user_id #so NowLoggedIn class can access this data
            logged_in_user_id = user_credentials[0]
            self.now_logged_in()
        else:
            self.attempt_login_count +=1 #Increments attempt count
            messagebox.showerror("Try again", "Invalid username, password or captcha")
            if self.attempt_login_count > 3:
                self.disable_login_widgets()
                self.show_too_many_attempts_message()
                self.after(120000, self.show_login_widgets) # After 2 minutes in milliseconds, the self.show_widgets method is called
            else:
                pass
        conn.close()
           
    def show_too_many_attempts_message(self):
        # Show message for too many attempts
        self.too_many_login_attempts_label.grid(row=1, column=0)
        messagebox.showerror("Wrong Inputs", "You are now locked from attempting to login for the next 2 minutes.")

    def disable_login_widgets(self):
        #Hide login widgets
        self.login_label.grid_forget()
        self.password_label.grid_forget()
        self.password_entry.grid_forget()
        self.username_entry.grid_forget()
        self.username_label.grid_forget() 
        self.captcha_entry.grid_forget()
        self.captcha_label.grid_forget()
        self.login_button.grid_forget()
        self.generate_captcha_button.grid_forget()

    def show_login_widgets(self):
        # Show login widgets again after the 2 minute
        self.create_login_button.grid(row=3, column=4, columnspan=2)
        self.login_label.grid(row=0, column=0, columnspan=2)
        self.username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1)
        self.password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1)
        self.login_button.grid(row=5, column=0, columnspan=2)
        self.change_password_button.grid(row=4, column=3, columnspan=2)
        self.captcha_entry.grid(row=3, column=1, columnspan=2)
        self.captcha_label.grid(row=3, column=0) 
        self.generate_captcha_button.grid(row=4, column=0, columnspan=2)
        self.no_account_label.grid(row=2, column=4)
        self.too_many_login_attempts_label.grid_forget()
        self.attempt_login_count = 0

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
        self.attempt_login_count = 0 #Allows the user to have 3 attempts after they have logged in

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
        create_login_label = tkinter.Label(create_login_frame, text="Create Login", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 25), pady=25)
        create_username_label = tkinter.Label(create_login_frame, text="Username", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.create_username_entry = tkinter.Entry(create_login_frame, font=("Times New Roman", 12))
        create_password_label = tkinter.Label(create_login_frame, text="Password", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.create_password_entry = tkinter.Entry(create_login_frame, show="*", font=("Times New Roman", 12))
        create_login_button = tkinter.Button(create_login_frame, text="Create Account", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=self.create_account)

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
        conn.close()

class ChangePasswordPage(tkinter.Tk):
    #Initialise the change password page
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.title("Change Password")
        self.geometry('400x300')
        self.configure(bg="#161d29")
        self.attempt_change_login = 0
        #Create widgets on the change password page
        self.create_widgets()

    #Method to create widgets on the change password page
    def create_widgets(self):
        change_password_frame = tkinter.Frame(self, bg="#161d29")

        self.username_label = tkinter.Label(change_password_frame, text="Username", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.username_entry = tkinter.Entry(change_password_frame, font=("Times New Roman", 12))
        self.old_password_label = tkinter.Label(change_password_frame, text="Old Password", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.old_password_entry = tkinter.Entry(change_password_frame, show="*", font=("Times New Roman", 12))
        self.new_password_label = tkinter.Label(change_password_frame, text="New Password", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)
        self.new_password_entry = tkinter.Entry(change_password_frame, show="*", font=("Times New Roman", 12))
        self.change_password_button = tkinter.Button(change_password_frame, text="Change Password", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 10), pady=5, command=self.change_password)
        self.too_many_change_password_attempts_label = tkinter.Label(change_password_frame, text="Too many attempts! Wait 2 minutes to try again", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=5)

        #Grid layout for widgets
        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        self.old_password_label.grid(row=1, column=0)
        self.old_password_entry.grid(row=1, column=1)
        self.new_password_label.grid(row=2, column=0)
        self.new_password_entry.grid(row=2, column=1)
        self.change_password_button.grid(row=3, column=0, columnspan=2)

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
        sure = messagebox.askquestion("Ask Question", "Are you sure you would like to change the password to your account? There is no going back", icon="info")
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
                    self.attempt_change_login = 0 #Allows the user to have 3 attempts after they have changed the password
                    self.destroy()
            else:
                conn.close()
                messagebox.showerror("Change Password Failed", "Invalid username or old password.")
                self.attempt_change_login += 1 # Increments the count
                if self.attempt_change_login > 3:
                    self.disable_change_password_widgets() # Gets rid of certain widgets, stopping the user from attempting to change password
                    self.show_too_many_change_password_attempts_message() #Places the label
                    self.after(120000, self.show_change_password_widgets) # After 2 minutes in milliseconds, the self.show_widgets method is called
                else:
                    pass
            conn.close()
        else:
            pass
            
    def show_change_password_widgets(self): #Places the widgets back when called
        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        self.old_password_label.grid(row=1, column=0)
        self.old_password_entry.grid(row=1, column=1)
        self.new_password_label.grid(row=2, column=0)
        self.new_password_entry.grid(row=2, column=1)
        self.change_password_button.grid(row=3, column=0, columnspan=2)
        self.too_many_change_password_attempts_label.grid_forget() #
        self.attempt_change_login = 0 #set the attempts to 0 so that after a further 3 attempts, you will be locked out again

    def show_too_many_change_password_attempts_message(self):
        self.too_many_change_password_attempts_label.grid(row=1, column=0) # Places the label on the screen telling the user that they must wait
        messagebox.showerror("Wrong Inputs", "You are now locked from attempting to change a password for the next 2 minutes.")

    def disable_change_password_widgets(self):
        self.username_label.grid_forget() #Hiding all the labels that have to go temporarily
        self.username_entry.grid_forget()
        self.old_password_label.grid_forget()
        self.old_password_entry.grid_forget()
        self.new_password_label.grid_forget()
        self.new_password_entry.grid_forget()
        self.change_password_button.grid_forget()

class NowLoggedInPage(tkinter.Tk):
    #Initialise the now logged in page
    def __init__(self, master, entered_username, entered_password):
        super().__init__()
        self.fox_count = 0 #Instantiate the counts
        self.pigeon_count = 0
        self.human_count = 0
        self.master = master
        self.title("Logged in")
        self.geometry('1000x1000')
        self.configure(bg="#161d29")
        self.pigeon_datetimes = [] # Create empty lists for the datetimes
        self.fox_datetimes = [] 
        self.human_datetimes = []
        self.entered_username = entered_username
        self.entered_password = entered_password
        #Create widgets on the now logged in page
        self.create_widgets()
        self.gather_data()
    
    def on_add_fox_button(self):
        conn = sqlite3.connect('Data details.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (Userid, DateTime, Type) VALUES (?, ?, ?)", (logged_in_user_id, datetime.now(), "Fox")) # Insert a new record into the users table for the right userid, adding a fox for the right datetime
        conn.commit()
        conn.close()

    def on_add_pigeon_button(self):
        conn = sqlite3.connect('Data details.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (Userid, DateTime, Type) VALUES (?, ?, ?)", (logged_in_user_id, datetime.now(), "Pigeon")) # Insert a new record into the users table for the right userid, adding a pigeon for the right datetime
        conn.commit()
        conn.close()

    def on_add_human_button(self):
        conn = sqlite3.connect('Data details.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (Userid, DateTime, Type) VALUES (?, ?, ?)", (logged_in_user_id, datetime.now(), "Human")) # Insert a new record into the users table for the right userid, adding a human for the right datetime
        conn.commit()
        conn.close()

    def gather_data(self):
        conn = sqlite3.connect('Data details.db')
        cursor = conn.cursor()

        # Fetch pigeon data
        cursor.execute("SELECT Datetime FROM users WHERE Type = ? AND Userid = ?", ("Pigeon", logged_in_user_id)) #Requires the right userid (so not any user can access your data)
        rows = cursor.fetchall()
        # Iterate over fetched rows
        for row in rows:
            Pigeondatetime = row[0]
            self.pigeon_datetimes.append(Pigeondatetime)  # Append fetched datetime to self.fox_datetimes list
            self.pigeon_count += 1 # Increment fox count

        # Fetch fox data
        cursor.execute("SELECT Datetime FROM users WHERE Type = ? AND Userid = ?", ("Fox", logged_in_user_id)) #Requires the right userid (so not any user can access your data)
        rows = cursor.fetchall()
        # Iterate over fetched rows (again)
        for row in rows:
            Foxdatetime = row[0]
            self.fox_datetimes.append(Foxdatetime)  # Append fetched datetime to self.fox_datetimes list
            self.fox_count += 1 # Increment fox count

        # Fetch human data
        cursor.execute("SELECT Datetime FROM users WHERE Type = ? AND Userid = ?", ("Human", logged_in_user_id)) #Requires the right userid (so not any user can access your data)
        rows = cursor.fetchall()
        # Iterate over fetched rows (again)
        for row in rows:
            Humandatetime = row[0]
            self.human_datetimes.append(Humandatetime) # Append fetched datetime to self.human_datetimes list
            self.human_count += 1 # Increment fox count

        # Update count labels with the latest counts
        self.logged_in_pigeon_count.config(text="Pigeon Count: " + str(self.pigeon_count))
        self.logged_in_fox_count.config(text="Fox Count: " + str(self.fox_count))
        self.logged_in_human_count.config(text="Human Count: " + str(self.human_count))
        
        self.display_datetimes(self) # Display the fetched datetimes
        conn.close()

    #Method to create widgets on the now logged in page
    def create_widgets(self):
        now_logged_in_frame = tkinter.Frame(self, bg="#161d29")

        # Labels for the logged in page
        logged_in_title = tkinter.Label(now_logged_in_frame, text="THE MACHINE ", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 25), pady=25)
        self.logged_in_pigeon_count = tkinter.Label(now_logged_in_frame, text="The Pigeon Count: " + str(self.pigeon_count), bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=25) # Concatenated the pigeon count (as a string)
        self.logged_in_fox_count = tkinter.Label(now_logged_in_frame, text="The Fox Count: " + str(self.fox_count), bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=25) # Concatenated the fox count (as a string)
        self.logged_in_human_count = tkinter.Label(now_logged_in_frame, text="The Human Count: " + str(self.human_count), bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=25) # Concatenated the human count (as a string)
        logged_in_delete_account = tkinter.Button(now_logged_in_frame, text="Delete Account", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 12), pady=25, command=self.delete_account)
        print_to_text_file_button = tkinter.Button(now_logged_in_frame, text="Print to File", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 12), pady=25,command=self.print_to_text_file)

        #Animal datetimes labels
        self.pigeon_datetime_label = tkinter.Label(now_logged_in_frame, text="Pigeon Datetimes:", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=25)
        self.fox_datetime_label = tkinter.Label(now_logged_in_frame, text="Fox Datetimes:", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=25)
        self.human_datetime_label = tkinter.Label(now_logged_in_frame, text="Human Datetimes:", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=25)

        # Buttons for movement and display
        speed_value_entry = tkinter.Entry(now_logged_in_frame, font=("Times New Roman", 12))
        steps_value_entry = tkinter.Entry(now_logged_in_frame, font=("Times New Roman", 12))
        display_button = tkinter.Button(now_logged_in_frame, text="Open Display", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 12), pady=25,command=camera_thread.start)
        move_up_button = tkinter.Button(now_logged_in_frame, text = "UP", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 12), pady=25,command=lambda: self.on_move_up_button(speed_value_entry.get(),steps_value_entry.get()))
        move_down_button = tkinter.Button(now_logged_in_frame, text = "DOWN", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 12), pady=25,command=lambda: self.on_move_down_button(speed_value_entry.get(),steps_value_entry.get()))
        move_right_button = tkinter.Button(now_logged_in_frame, text = "-->", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 12), pady=25,command=lambda: self.on_move_right_button(speed_value_entry.get(),steps_value_entry.get()))
        move_left_button = tkinter.Button(now_logged_in_frame, text = "<--", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 12), pady=25,command=lambda: self.on_move_left_button(speed_value_entry.get(),steps_value_entry.get()))
        speed_value_label = tkinter.Label(now_logged_in_frame, text="Speed:", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=25)
        steps_value_label = tkinter.Label(now_logged_in_frame, text="Steps:", bg='#161d29', fg="#FFFFFF", font=("Times New Roman", 12), pady=25)

        #Buttons for adding to counts
        human_count_button = tkinter.Button(now_logged_in_frame, text = "Human Detected", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 12), pady=25, command=self.on_add_human_button)
        fox_count_button = tkinter.Button(now_logged_in_frame, text = "Fox Detected", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 12), pady=25, command=self.on_add_fox_button)
        pigeon_count_button = tkinter.Button(now_logged_in_frame, text = "Pigeon Detected", bg=button_colour, fg="#FFFFFF", font=("Times New Roman", 12), pady=25, command=self.on_add_pigeon_button)

        # Grid layout for widgets
        logged_in_title.grid(row=0, column=0, columnspan=2)
        self.logged_in_pigeon_count.grid(row=1, column=0, columnspan=2)
        self.logged_in_fox_count.grid(row=2, column=0, columnspan=2)
        self.logged_in_human_count.grid(row=3, column=0, columnspan=2)
        logged_in_delete_account.grid(row=0, column=5, columnspan=2)

        self.pigeon_datetime_label.grid(row=4, column=0, columnspan=2)
        self.fox_datetime_label.grid(row=5, column=0, columnspan=2)
        self.human_datetime_label.grid(row=6, column=0, columnspan=2)
        print_to_text_file_button.grid(row=0, column=3, columnspan=2)
        display_button.grid(row=0, column=7, columnspan=1)
        human_count_button.grid(row=0, column=8, columnspan=1)
        pigeon_count_button.grid(row=0, column=9, columnspan=1)
        fox_count_button.grid(row=0, column=10, columnspan=1)

        speed_value_entry.grid(row=5, column=7, columnspan=1)
        steps_value_entry.grid(row=6, column=7, columnspan=1)
        speed_value_label.grid(row=5, column=6, columnspan=1)
        steps_value_label.grid(row=6, column=6, columnspan=1)
        move_up_button.grid(row=2, column=6, columnspan=1)
        move_down_button.grid(row=4, column=6, columnspan=1)
        move_right_button.grid(row=3, column=7, columnspan=1)
        move_left_button.grid(row=3, column=5, columnspan=1)

        now_logged_in_frame.pack()
    
    def on_move_up_button(self,speed, steps):
        if int(speed) > 2:
            messagebox.showerror("Speed too high!","Lower Speed!")
        elif int(steps) > 50:
            messagebox.showerror("Steps too high!","Lower Steps!")
        else:
            move_up(speed,steps)

    def on_move_right_button(self,speed, steps):
        if int(speed) > 2:
            messagebox.showerror("Speed too high!","Lower Speed!")
        elif int(steps) > 50:
            messagebox.showerror("Steps too high!","Lower Steps!")
        else:
            move_right(speed,steps)
    
    def on_move_left_button(self,speed, steps):
        if int(speed) > 2:
            messagebox.showerror("Speed too high!","Lower Speed!")
        elif int(steps) > 50:
            messagebox.showerror("Steps too high!","Lower Steps!")
        else:
            move_left(speed,steps)

    def on_move_down_button(self,speed, steps):
        if int(speed) > 2:
            messagebox.showerror("Speed too high!","Lower Speed!")
        elif int(steps) > 50:
            messagebox.showerror("Steps too high!","Lower Steps!")
        else:
            move_down(speed,steps)
    
    def print_to_text_file(self):
        file_path = "userdata.txt"
        try:
            #Open the file for writing
            file = open(file_path, "w")

            # Write pigeon datetimes and count
            file.write("Pigeon Datetimes:\n")
            for index in range(len(self.pigeon_datetimes)): # Loop through each pigeon datetime
                file.write(str(index + 1) + ". " + str(self.pigeon_datetimes[index]) + "\n") #Write the datetime to the file with its corresponding index
            file.write("Pigeon Count: " + str(self.pigeon_count) + "\n") # Write the pigeon count to the file

            # Write fox datetimes and count
            file.write("Fox Datetimes:\n")
            for index in range(len(self.fox_datetimes)): # Loop through each fox datetime
                file.write(str(index + 1) + ". " + str(self.fox_datetimes[index]) + "\n") #Write the datetime to the file with its corresponding index
            file.write("Fox Count: " + str(self.fox_count) + "\n") # Write the fox count to the file

            # Write fuman datetimes and count
            file.write("Human Datetimes:\n")
            for index in range(len(self.human_datetimes)): # Loop through each fox datetime
                file.write(str(index + 1) + ". " + str(self.human_datetimes[index]) + "\n") #Write the datetime to the file with its corresponding index
            file.write("Human Count: " + str(self.human_count) + "\n") # Write the human count to the file

            file.close() # Close the file after writing

            # Print success message
            messagebox.showinfo("Data Written", f"Data successfully written to {file_path}")
        except Exception as exception:
            # Print error message if an exception occurs
            messagebox.showerror("Error", f"An error occurred while writing to the file: {exception}")

    def display_datetimes(self, frame):
        # Define a list of tuples, each containing animal type, corresponding datetimes list and label (took way too long to figure out a solution here)
        animal_types = [
            ("Pigeon", self.pigeon_datetimes, self.pigeon_datetime_label),
            ("Fox", self.fox_datetimes, self.fox_datetime_label),
            ("Human", self.human_datetimes, self.human_datetime_label)]

        # Iterate over each tuple in the list
        for animal_type, datetimes, label in animal_types:
            datetimes_text = "" # Create an empty string to store the formatted datetimes text

            # Iterate over each datetime in the datetimes list
            for i, datetime in enumerate(datetimes):
                datetime_str = f"{i+1}. {datetime}" # Format the datetime with its corresponding index
                # Append the formatted datetime to the datetimes_text string with a newline
                datetimes_text = datetimes_text + datetime_str + "\n"

            # Set the text of the label to include the animal type and formatted datetimes
            label_text = f"{animal_type} Datetimes:\n{datetimes_text}"
            label.config(text=label_text)

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

#Subroutine to create the login details database
def create_login_database():
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

#Subroutine to create a temporary database storing supposed data of datetime of arrival and type of visitor ID, and the userId of the user to which the data belongs

def create_data_database():
    conn = sqlite3.connect('Data details.db') 
    cursor = conn.cursor() 
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Userid INTEGER NOT NULL,
                    DateTime DATETIME NOT NULL,
                    Type STRING NOT NULL
                    )
        ''') 
    conn.commit()
    conn.close()

#Main method to create the database and start the login page
if __name__ == "__main__":
    create_data_database()
    create_login_database()
    window = LoginPage()
    window.mainloop()
