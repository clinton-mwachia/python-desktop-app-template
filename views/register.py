import tkinter as tk
from tkinter import messagebox
from auth.auth import AuthController

class RegisterView:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
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

        # Register Button
        self.register_button = tk.Button(root, text="Register", command=self.register)
        self.register_button.pack()

        # Back to Login
        self.back_button = tk.Button(root, text="Back to Login", command=self.go_back)
        self.back_button.pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth_controller.register(username, password):
            messagebox.showinfo("Register", "Registration successful")
            self.root.destroy()
            self.open_login_view()
        else:
            messagebox.showerror("Register", "User already exists")

    def go_back(self):
        self.root.destroy()
        self.open_login_view()

    def open_login_view(self):
        from views.login import LoginView
        login_root = tk.Tk()
        LoginView(login_root)
        login_root.mainloop()
