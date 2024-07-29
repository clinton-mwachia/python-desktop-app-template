import tkinter as tk
from views.login import LoginView
from views.todo import TodoView
from views.user import UserView

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo Manager")

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Sidebar Frame for Tabs
        self.sidebar_frame = tk.Frame(self.main_frame, width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Sidebar Buttons (Tabs)
        self.dashboard_button = tk.Button(self.sidebar_frame, text="Dashboard", command=self.show_dashboard)
        self.dashboard_button.pack(fill=tk.X, pady=5)

        self.todos_button = tk.Button(self.sidebar_frame, text="Todos", command=self.show_todos)
        self.todos_button.pack(fill=tk.X, pady=5)

        self.users_button = tk.Button(self.sidebar_frame, text="Users", command=self.show_users)
        self.users_button.pack(fill=tk.X, pady=5)

        # Frames for different views
        self.dashboard_frame = tk.Frame(self.main_frame)
        self.todos_view = None
        self.users_view = None

        # Initially show Login View
        self.login_view = LoginView(self.root, self.login_success)

    def login_success(self, username):
        self.username = username
        self.show_dashboard()

    def show_dashboard(self):
        if self.todos_view:
            self.todos_view.todos_frame.pack_forget()
        if self.users_view:
            self.users_view.users_frame.pack_forget()
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)

    def show_todos(self):
        if self.todos_view is None:
            self.todos_view = TodoView(self.main_frame, self.username)
        self.dashboard_frame.pack_forget()
        if self.users_view:
            self.users_view.users_frame.pack_forget()
        self.todos_view.todos_frame.pack(fill=tk.BOTH, expand=True)

    def show_users(self):
        if self.users_view is None:
            self.users_view = UserView(self.main_frame)
        self.dashboard_frame.pack_forget()
        if self.todos_view:
            self.todos_view.todos_frame.pack_forget()
        self.users_view.users_frame.pack(fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
