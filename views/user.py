import tkinter as tk
from tkinter import ttk
from models.user import UserModel

class UserView:
    def __init__(self, root):
        self.root = root
        self.user_model = UserModel()

        self.users_frame = tk.Frame(root)
        self.users_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_users_frame()

    def setup_users_frame(self):
        self.users_tree_frame = tk.Frame(self.users_frame)
        self.users_tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for displaying users
        self.users_tree = ttk.Treeview(self.users_tree_frame, columns=("username", "email"), show="headings")
        self.users_tree.heading("username", text="Username")
        self.users_tree.heading("email", text="Email")
        self.users_tree.pack(fill=tk.BOTH, expand=True)

        self.load_users()

    def load_users(self):
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        users = list(self.user_model.get_all_users())
        for user in users:
            self.users_tree.insert("", tk.END, iid=str(user['_id']),
                                   values=(user['username'], user.get('email', 'No email')))
