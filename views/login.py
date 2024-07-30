import tkinter as tk
from tkinter import messagebox
from auth.auth import AuthController

class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("Login User") # title of the main frame
        self.root.geometry("400x400") # width and height of the main frame
        self.on_login_success = on_login_success
        self.auth_controller = AuthController()

        self.frame = tk.Frame(root, bg='white', borderwidth=2, relief='groove', padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor='center', width=300, height=200)

        tk.Label(self.frame, text="Username").pack()
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack()

        tk.Label(self.frame, text="Password").pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()

        login_button = tk.Button(self.frame, text="Login", command=self.login)
        login_button.pack(pady=10)

        register_button = tk.Button(self.frame, text="Register", command=self.register)
        register_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth_controller.login(username, password):
            self.on_login_success(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth_controller.register(username, password):
            messagebox.showinfo("Registration Successful", "You can now log in")
        else:
            messagebox.showerror("Registration Failed", "Username already exists")
