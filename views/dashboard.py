import tkinter as tk
from views.todo import TodoView
from views.user import UserView
from views.profile import ProfileView

class DashboardView:
    def __init__(self, sidebar_frame, content_frame, username, logout_callback):
        self.sidebar_frame = sidebar_frame
        self.content_frame = content_frame
        self.username = username
        self.logout_callback = logout_callback

        self.setup_sidebar()

        # Initially show the todos view
        self.show_todos()

    def setup_sidebar(self):
        tk.Button(self.sidebar_frame, text="Dashboard", command=self.show_dashboard, width=15).pack(fill=tk.X)
        tk.Button(self.sidebar_frame, text="Todos", command=self.show_todos).pack(fill=tk.X)
        tk.Button(self.sidebar_frame, text="Users", command=self.show_users).pack(fill=tk.X)
        tk.Button(self.sidebar_frame, text="Profile", command=self.show_profile).pack(fill=tk.X)
        tk.Button(self.sidebar_frame, text="Logout", command=self.logout).pack(fill=tk.X)

    def show_dashboard(self):
        self.clear_content()
        # Add any dashboard-specific widgets here
        tk.Label(self.content_frame, text="Welcome to the Dashboard").pack(pady=20)

    def show_todos(self):
        self.clear_content()
        TodoView(self.content_frame, self.username)

    def show_users(self):
        self.clear_content()
        UserView(self.content_frame)

    def show_profile(self):
        self.clear_content()
        ProfileView(self.content_frame, self.username)

    def logout(self):
        self.clear_content()
        self.logout_callback()  # Call the logout callback function

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
