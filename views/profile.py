import tkinter as tk
from tkinter import messagebox
from models.user import UserModel

class ProfileView:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.user_model = UserModel()
        self.user = self.user_model.find_user(username)

        self.profile_frame = tk.Frame(root)
        self.profile_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_profile_frame()

    def setup_profile_frame(self):
        tk.Label(self.profile_frame, text="Profile").pack(pady=10)

        # Display user profile picture
        if 'profile_picture' in self.user and self.user['profile_picture']:
            try:
                # Load the image file (ensure the path is correct and the file exists)
                self.photo = tk.PhotoImage(file=self.user['profile_picture'])
                tk.Label(self.profile_frame, image=self.photo).pack(pady=10)
            except tk.TclError:
                tk.Label(self.profile_frame, text="Profile Picture Not Found").pack(pady=10)
        else:
            tk.Label(self.profile_frame, text="No Profile Picture").pack(pady=10)

        # Display user details
        tk.Label(self.profile_frame, text=f"Username: {self.user['username']}").pack(pady=5)
        tk.Label(self.profile_frame, text=f"Email: {self.user.get('email', 'No email')}").pack(pady=5)
