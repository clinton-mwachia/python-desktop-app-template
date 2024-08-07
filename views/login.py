import tkinter as tk
from tkinter import messagebox
from auth.auth import AuthController
import logging

# Initialize the logger
logger = logging.getLogger("application_logger")

class LoginView:
    def __init__(self, root, show_dashboard_callback, show_register_callback):
        self.root = root
        self.root.title("TEMPLATE") # title of the main frame
        self.root.geometry("400x400") # width and height of the main frame
        self.show_dashboard_callback = show_dashboard_callback
        self.show_register_callback = show_register_callback
        self.auth_controller = AuthController()

        self.frame = tk.Frame(root, bg='white', borderwidth=2, relief='groove', padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor='center', width=300, height=300)

        tk.Label(self.frame, text="Username").pack()
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack()

        tk.Label(self.frame, text="Password").pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()

        login_button = tk.Button(self.frame, text="Login", command=self.login)
        login_button.pack(pady=10)

        tk.Label(self.frame, text="No account?").pack()
        register_button = tk.Button(self.frame, text="Register", command=self.show_register_callback)
        register_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            if self.auth_controller.login(username, password):
                messagebox.showinfo("Login Success", "User logged in successfull")
                logger.info(f'{username} logged in')
                self.show_dashboard_callback(username)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
                logger.error(f'{username}: Invalid username or password')
        else:
            messagebox.showerror("Login Failed", "Please enter username and password")
            logger.error('Please enter username and password')