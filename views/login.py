import tkinter as tk
from tkinter import messagebox
from auth.auth import AuthController

class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.auth_controller = AuthController()

        self.setup_login_frame()

    def setup_login_frame(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.login_frame, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        login_button.pack(pady=10)

        register_button = tk.Button(self.login_frame, text="Register", command=self.register)
        register_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth_controller.login(username, password):
            self.login_frame.pack_forget()
            self.on_login_success(username)  # Call the callback with the username
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth_controller.register(username, password):
            messagebox.showinfo("Registration Success", "User registered successfully.")
        else:
            messagebox.showerror("Registration Error", "Username already exists.")
