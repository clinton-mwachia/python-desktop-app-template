import tkinter as tk
from tkinter import messagebox
from auth.auth import AuthController

class RegisterView:
    def __init__(self, root, show_login_callback):
        self.root = root
        self.show_login_callback = show_login_callback
        self.root.title("Register")
        self.root.geometry("400x400")
        self.auth_controller = AuthController()

        # base frame
        self.frame = tk.Frame(root, bg='white', borderwidth=2, relief='groove', padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor='center', width=300, height=300)

        # Username
        self.username_label = tk.Label(self.frame, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack()

        # Email
        self.email_label = tk.Label(self.frame, text="Email")
        self.email_label.pack()
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack()

        # Password
        self.password_label = tk.Label(self.frame, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()

        # Register Button
        self.register_button = tk.Button(self.frame, text="Register", command=self.register)
        self.register_button.pack()

        # Back to Login
        self.back_button = tk.Button(self.frame, text="Back to Login", command=self.go_back)
        self.back_button.pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        if self.auth_controller.register(username, password, email):
            messagebox.showinfo("Register", "Registration successful")
            self.show_login_callback()
        else:
            messagebox.showerror("Register", "User already exists")

    def go_back(self):
        self.show_login_callback()
