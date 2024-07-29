import tkinter as tk
from tkinter import messagebox
from auth.auth import AuthController
from views.todo import TodoView

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.auth_controller = AuthController()

        # Username
        self.username_label = tk.Label(root, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        # Password
        self.password_label = tk.Label(root, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        # Login Button
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.pack()

        # Register Button
        self.register_button = tk.Button(root, text="Register", command=self.open_register_view)
        self.register_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth_controller.login(username, password):
            self.show_todo_view(username)
        else:
            messagebox.showerror("Login", "Invalid credentials")

    def open_register_view(self):
        self.clear_frame()
        from views.register import RegisterView
        RegisterView(self.root)

    def show_todo_view(self, username):
        self.clear_frame()
        TodoView(self.root, username)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
