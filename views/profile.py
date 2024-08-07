import tkinter as tk
from tkinter import messagebox,PhotoImage
from bson.objectid import ObjectId
from models.user import UserModel
from views.notification import NotificationManager
import logging

# Initialize the logger
logger = logging.getLogger("application_logger")

class ProfileView:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.user_model = UserModel()
        self.user = self.user_model.find_user(username)

        # notification manager
        # Create a frame for the toolbar
        self.toolbar_frame = tk.Frame(root)
        self.toolbar_frame.pack(fill=tk.X)

        self.notification_manager = NotificationManager(self.toolbar_frame)

        self.profile_frame = tk.Frame(root, borderwidth=2, relief='groove', padx=20, pady=20)
        self.profile_frame.place(relx=0.5, rely=0.2, anchor='center')

        self.setup_profile_frame()

    def setup_profile_frame(self):
        # User details
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.active_var = tk.StringVar()
        self.role_var = tk.StringVar()

        details_frame = tk.Frame(self.profile_frame)
        details_frame.grid(row=0, column=1, sticky='w')

        tk.Label(details_frame, text="Username:", font=("Helvetica", 14)).grid(row=0, column=0, sticky='w')
        tk.Label(details_frame, textvariable=self.name_var, font=("Helvetica", 14)).grid(row=0, column=1, sticky='w')

        tk.Label(details_frame, text="Email:", font=("Helvetica", 14)).grid(row=1, column=0, sticky='w')
        tk.Label(details_frame, textvariable=self.email_var, font=("Helvetica", 14)).grid(row=1, column=1, sticky='w')

        tk.Label(details_frame, text="Active:", font=("Helvetica", 14)).grid(row=2, column=0, sticky='w')
        tk.Label(details_frame, textvariable=self.active_var, font=("Helvetica", 14)).grid(row=2, column=1, sticky='w')

        tk.Label(details_frame, text="Role:", font=("Helvetica", 14)).grid(row=3, column=0, sticky='w')
        tk.Label(details_frame, textvariable=self.role_var, font=("Helvetica", 14)).grid(row=3, column=1, sticky='w')

        # Buttons for updating details and password
        button_frame = tk.Frame(self.profile_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        self.update_button = tk.Button(button_frame, text="Update Details", command=self.update_details)
        self.update_button.pack(side='left', padx=10)

        self.change_password_button = tk.Button(button_frame, text="Change Password", command=self.change_password)
        self.change_password_button.pack(side='left', padx=10)

        # Load user data
        self.load_user_data()

    def load_user_data(self):
        user = self.user_model.find_user(self.user['username']) 
        if user:
            self.name_var.set(user.get('username', ''))
            self.email_var.set(user.get('email', ''))
            self.active_var.set(user.get('active', ''))
            self.role_var.set(user.get('role', ''))

    def update_details(self):
        user = self.user_model.collection.find_one({"_id": ObjectId(self.user['_id'])})
        if not user:
            return
        
        # Create a new window for changing the user details
        self.update_details_window = tk.Toplevel(self.root)
        self.update_details_window.title("Update user details")
        self.update_details_window.geometry("300x300")

        # email
        tk.Label(self.update_details_window, text="Email:").pack(pady=5)
        self.new_email_entry = tk.Entry(self.update_details_window)
        self.new_email_entry.insert(0, user['email'])
        self.new_email_entry.pack(pady=5)

        # submit button
        save_button = tk.Button(self.update_details_window, text="Submit", command=lambda: self.submit_details_change(
            user_id=self.user['_id']
        ))
        save_button.pack(pady=10)

    def submit_details_change(self, user_id):
        new_email = self.new_email_entry.get(),
    
        if new_email:
            self.user_model.update_user(user_id, email=new_email)
            messagebox.showinfo("Update Details", "user details have been Updated!")
            self.load_user_data()
            logger.info(f"{self.username}: updated email")
            self.notification_manager.add_notification(f"{self.username}: updated email")
            self.update_details_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please enter required fields.")
            logger.error(f"{self.username}: Please enter required fields.")
            self.update_user_window.destroy()

    def change_password(self):
        # Create a new window for changing the password
        self.password_window = tk.Toplevel(self.root)
        self.password_window.geometry("300x300")
        self.password_window.title("Change Password")

        # old password
        tk.Label(self.password_window, text="Old Password:").pack(pady=5)
        old_password_entry = tk.Entry(self.password_window, show='*')
        old_password_entry.pack(pady=5)

        # new password
        tk.Label(self.password_window, text="New Password:").pack(pady=5)
        new_password_entry = tk.Entry(self.password_window, show='*')
        new_password_entry.pack(pady=5)

        # confirm new password
        tk.Label(self.password_window, text="Confirm New Password:").pack(pady=5)
        confirm_password_entry = tk.Entry(self.password_window, show='*')
        confirm_password_entry.pack(pady=5)

        tk.Button(self.password_window, text="Submit", command=lambda: self.submit_password_change(
            old_password_entry.get(),
            new_password_entry.get(),
            confirm_password_entry.get()
        )).pack(pady=10)

    def submit_password_change(self, old_password, new_password, confirm_password):
        # Validate and update the password
        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match.")
            logger.error(f"{self.username}: New passwords do not match.")
            return
        
        if new_password == old_password:
            messagebox.showerror("Error", "new password cannot be old password")
            logger.error(f"{self.username}: new password cannot be old password.")
            return

        result = self.user_model.update_password(user_id=self.user['_id'],old_password=old_password, new_password=new_password)
        if result:
            messagebox.showinfo("Success", "Password updated successfully.")
            logger.info(f"{self.username}:  updated Password successfully.")
            self.notification_manager.add_notification(f"{self.username}: updated Password successfully.")
            self.password_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to update password.")
            logger.error(f"{self.username}: Failed to update password")

