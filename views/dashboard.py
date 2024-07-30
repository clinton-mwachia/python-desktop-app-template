import tkinter as tk
from views.todo import TodoView
from views.user import UserView

class DashboardView:
    def __init__(self, sidebar_frame, content_frame, username):
        self.sidebar_frame = sidebar_frame
        self.content_frame = content_frame
        self.username = username

        self.setup_sidebar()

        # Initially show the todos view
        self.show_todos()

    def setup_sidebar(self):
        tk.Button(self.sidebar_frame, text="Dashboard", command=self.show_dashboard).pack(fill=tk.X)
        tk.Button(self.sidebar_frame, text="Todos", command=self.show_todos).pack(fill=tk.X)
        tk.Button(self.sidebar_frame, text="Users", command=self.show_users).pack(fill=tk.X)

    def show_dashboard(self):
        self.clear_content()
        # Add any dashboard-specific widgets here

    def show_todos(self):
        self.clear_content()
        TodoView(self.content_frame, self.username)

    def show_users(self):
        self.clear_content()
        UserView(self.content_frame)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
