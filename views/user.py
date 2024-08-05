import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from models.user import UserModel
from bson.objectid import ObjectId
from views.notification import NotificationManager
import csv

class UserView:
    def __init__(self, root):
        self.root = root
        self.user_model = UserModel()
        self.page_size = 10
        self.current_page = 1

        # search query
        self.search_query = ""
        self.search_timer = None

        # filter status
        self.filter_status = "All"

        # sort
        self.sort_by = "username"

        # notification manager
        # Create a frame for the toolbar
        self.toolbar_frame = tk.Frame(root)
        self.toolbar_frame.pack(fill=tk.X)

        self.notification_manager = NotificationManager(self.toolbar_frame)

        self.users_frame = tk.Frame(root)
        self.users_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_users_frame()
        self.load_users()  # Load users after setting up the UI

    def setup_users_frame(self):
         # creating buttons frame
        self.button_frame = tk.Frame(self.users_frame)
        self.button_frame.pack()

        # add todo button
        self.add_button = tk.Button(self.button_frame, text="Add User", command=self.add_user)
        self.add_button.pack(side=tk.LEFT, pady=5)

        # export to csv button
        self.export_csv_button = tk.Button(self.button_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_csv_button.pack(side=tk.LEFT, pady=5)
       
        # search input
        self.search_frame = tk.Frame(self.users_frame)
        self.search_frame.pack(pady=5)

        tk.Label(self.search_frame, text="Status:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        self.search_entry.insert(0, "Search Users")
        self.search_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, "Search Users"))
        self.search_entry.bind("<FocusOut>", lambda event: self.set_placeholder(event, "Search Users"))

        # filter input
        self.filter_frame = tk.Frame(self.users_frame)
        self.filter_frame.pack(pady=5)

        tk.Label(self.filter_frame, text="Filter by Role:").pack(side=tk.LEFT, padx=5)
        self.role_combobox = ttk.Combobox(self.filter_frame, values=["All", "admin", "user"])
        self.role_combobox.set("All")
        self.role_combobox.pack(side=tk.LEFT)
        self.role_combobox.bind("<<ComboboxSelected>>", self.on_filter_change)

        # sorting frame
        tk.Label(self.filter_frame, text="Sort By:").pack(side=tk.LEFT, padx=5)
        self.sort_combobox = ttk.Combobox(self.filter_frame, values=["NONE", "username", "role"])
        self.sort_combobox.set("NONE")
        self.sort_combobox.pack(side=tk.LEFT)
        self.sort_combobox.bind("<<ComboboxSelected>>", self.on_sort_change)

        self.tree_frame = tk.Frame(self.users_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("username", "email", "active", "role","actions"), show="headings")
        self.tree.heading("username", text="Username")
        self.tree.heading("email", text="Email")
        self.tree.heading("active", text="Active")
        self.tree.heading("role", text="Role")
        self.tree.heading("actions", text="Actions")
        self.tree.column("actions", width=150, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

        self.pagination_frame = tk.Frame(self.users_frame)
        self.pagination_frame.pack(pady=10)

        self.prev_button = tk.Button(self.pagination_frame, text="Previous", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT)

        self.page_label = tk.Label(self.pagination_frame, text=f"Page {self.current_page}")
        self.page_label.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.pagination_frame, text="Next", command=self.next_page)
        self.next_button.pack(side=tk.LEFT)

    def on_search(self, event):
        if self.search_timer:
            self.root.after_cancel(self.search_timer)
        self.search_timer = self.root.after(300, self.update_search_query)

    def update_search_query(self):
        self.search_query = self.search_entry.get()
        self.load_users()

    def on_filter_change(self, event):
        self.filter_status = self.role_combobox.get()
        self.load_users()

    def on_sort_change(self, event):
        self.sort_by = self.sort_combobox.get()
        self.load_users()

    def export_to_csv(self):
        users = self.user_model.collection.find()
        filtered_users = [user for user in users if self.search_query.lower() in user['username'].lower()]

        if self.filter_status != "All":
            filtered_users = [user for user in filtered_users if user.get('role', '') == self.filter_status]

        with open('users.csv', 'w', newline='') as csvfile:
            fieldnames = ['Username', 'Email', 'Active', 'Role' ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user in filtered_users:
                writer.writerow({'Username': user['username'], 'Email': user['email'], 'Active': user.get('active',''), 'Role': user.get('role', '')})

        messagebox.showinfo("Export to CSV", "Users have been exported to users.csv")


    def load_users(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        total_users = self.user_model.collection.count_documents({})
        start = (self.current_page - 1) * self.page_size
        users = self.user_model.collection.find().skip(start).limit(self.page_size)
        filtered_users = [user for user in users if self.search_query.lower() in user['username'].lower()]

        # filter users based on filter
        if self.filter_status != "All":
            filtered_users = [user for user in filtered_users if user.get('role', '') == self.filter_status]

        # handle sorting
        if self.sort_by == "NONE":
            filtered_users
        elif self.sort_by == "username":
                    filtered_users.sort(key=lambda x: x['username'])
        elif self.sort_by == "role":
                    filtered_users.sort(key=lambda x: x.get('role', ''))

        if not filtered_users:
                    self.tree.insert("", tk.END, iid="no_user", values=("No users found", "", "", ""))
                    self.prev_button.config(state=tk.DISABLED)
                    self.next_button.config(state=tk.DISABLED)
        else:
            for user in filtered_users:
                self.tree.insert("", tk.END, iid=str(user['_id']),
                             values=(user['username'], user.get('email', 'No email'), user.get('active',''), user.get('role',''),'Edit/Delete'))

            self.page_label.config(text=f"Page {self.current_page}")
            self.prev_button.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
            self.next_button.config(state=tk.NORMAL if self.current_page * self.page_size < total_users else tk.DISABLED)
    
    def add_user(self):
        self.add_user_window = tk.Toplevel(self.root)
        self.add_user_window.title("Add User")
        self.add_user_window.geometry("300x300")

        tk.Label(self.add_user_window, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.add_user_window)
        self.username_entry.pack(pady=5)

        tk.Label(self.add_user_window, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.add_user_window, show="*")
        self.password_entry.pack(pady=5)

        tk.Label(self.add_user_window, text="Email (optional)").pack(pady=5)
        self.email_entry = tk.Entry(self.add_user_window)
        self.email_entry.pack(pady=5)

        tk.Label(self.add_user_window, text="Role").pack(pady=5)
        self.role_combobox = ttk.Combobox(self.add_user_window, values=["admin", "user"])
        self.role_combobox.current(1)  # Set default role to 'user'
        self.role_combobox.pack(pady=5)

        add_button = tk.Button(self.add_user_window, text="Add", command=self.save_user)
        add_button.pack(pady=10)

    def save_user(self):
        username = self.username_entry.get().lower()
        password = self.password_entry.get().lower()
        email = self.email_entry.get().lower()
        role = self.role_combobox.get().lower()
        if username and password and role:
            self.user_model.create_user(username, password, email, role)
            self.load_users()
            self.notification_manager.add_notification(f"New user added: {username}")
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")
        self.add_user_window.destroy()

    def update_user(self, user_id):
        user = self.user_model.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return

        self.update_user_window = tk.Toplevel(self.root)
        self.update_user_window.title("Update User")
        self.update_user_window.geometry("300x300")

        tk.Label(self.update_user_window, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.update_user_window)
        self.username_entry.insert(0, user['username'])
        self.username_entry.pack(pady=5)

        tk.Label(self.update_user_window, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.update_user_window, show="*")
        self.password_entry.insert(0, user['password'])
        self.password_entry.pack(pady=5)

        tk.Label(self.update_user_window, text="Email (optional)").pack(pady=5)
        self.email_entry = tk.Entry(self.update_user_window)
        self.email_entry.insert(0, user.get('email', ''))
        self.email_entry.pack(pady=5)

        tk.Label(self.update_user_window, text="Status").pack(pady=5)
        self.role_combobox = ttk.Combobox(self.update_user_window, values=["admin", "user"])
        self.role_combobox.set(user.get('role', 'No role'))
        self.role_combobox.pack(pady=5)

        save_button = tk.Button(self.update_user_window, text="Save", command=lambda: self.save_updated_user(user_id))
        save_button.pack(pady=10)

    def save_updated_user(self, user_id):
        new_username = self.username_entry.get().lower()
        new_password = self.password_entry.get().lower()
        new_email = self.email_entry.get().lower()
        new_role = self.role_combobox.get().lower()
        if new_username and new_password:
            self.user_model.update_user(user_id, username=new_username, email=new_email, role=new_role)
            self.load_users()
            self.notification_manager.add_notification(f"user {new_username} updated")
        else:
            messagebox.showwarning("Input Error", "Please enter required fields.")
        self.update_user_window.destroy()

    def delete_user(self, user_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
            self.user_model.collection.delete_one({"_id": ObjectId(user_id)})
            self.load_users()
            self.notification_manager.add_notification(f"user: {user_id} deleted")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        user_id = selected_item[0]

        self.action_window = tk.Toplevel(self.root)
        self.action_window.title("User Actions")

        edit_button = tk.Button(self.action_window, text="Edit", command=lambda: self.perform_action(user_id, "edit"))
        edit_button.pack(pady=5)

        delete_button = tk.Button(self.action_window, text="Delete", command=lambda: self.perform_action(user_id, "delete"))
        delete_button.pack(pady=5)

    def perform_action(self, user_id, action):
        if action == "edit":
            self.update_user(user_id)
        elif action == "delete":
            self.delete_user(user_id)
        self.action_window.destroy()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_users()

    def next_page(self):
        total_users = self.user_model.collection.count_documents({})
        if self.current_page * self.page_size < total_users:
            self.current_page += 1
            self.load_users()

    # search clear placeholder
    def clear_placeholder(self, event, placeholder_text):
        if event.widget.get() == placeholder_text:
            event.widget.delete(0, tk.END)
            event.widget.config(fg="black")

    def set_placeholder(self, event, placeholder_text):
        if event.widget.get() == "":
            event.widget.insert(0, placeholder_text)
            event.widget.config(fg="grey")
