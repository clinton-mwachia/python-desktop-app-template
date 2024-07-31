import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from models.todo import TodoModel
from auth.auth import AuthController
from bson.objectid import ObjectId

class TodoView:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.todo_model = TodoModel()
        self.page_size = 10
        self.current_page = 1

        # Get user information from AuthController
        self.auth_controller = AuthController()
        self.user = self.auth_controller.user_model.find_user(username)

        self.todos_frame = tk.Frame(root)
        self.todos_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_todos_frame()
        self.load_todos()  # Load todos after setting up the UI

    def setup_todos_frame(self):
        self.add_button = tk.Button(self.todos_frame, text="Add Todo", command=self.add_todo)
        self.add_button.pack(pady=10)

        self.tree_frame = tk.Frame(self.todos_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("title", "description", "status", "actions"), show="headings")
        self.tree.heading("title", text="Title")
        self.tree.heading("description", text="Description")
        self.tree.heading("status", text="Status")
        self.tree.heading("actions", text="Actions")
        self.tree.column("actions", width=150, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

        self.pagination_frame = tk.Frame(self.todos_frame)
        self.pagination_frame.pack(pady=10)

        self.prev_button = tk.Button(self.pagination_frame, text="Previous", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT)

        self.page_label = tk.Label(self.pagination_frame, text=f"Page {self.current_page}")
        self.page_label.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.pagination_frame, text="Next", command=self.next_page)
        self.next_button.pack(side=tk.LEFT)

    def load_todos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        total_todos = self.todo_model.collection.count_documents({"user_id": self.user['_id']})
        start = (self.current_page - 1) * self.page_size
        todos = self.todo_model.collection.find({"user_id": self.user['_id']}).skip(start).limit(self.page_size)

        for todo in todos:
            self.tree.insert("", tk.END, iid=str(todo['_id']),
                             values=(todo['title'], todo['description'], todo.get('status', 'NA'), 'Edit/Delete'))

        self.page_label.config(text=f"Page {self.current_page}")
        self.prev_button.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_page * self.page_size < total_todos else tk.DISABLED)

    def add_todo(self):
        self.add_todo_window = tk.Toplevel(self.root)
        self.add_todo_window.title("Add Todo")
        self.add_todo_window.geometry("300x300")

        tk.Label(self.add_todo_window, text="Title").pack(pady=5)
        self.title_entry = tk.Entry(self.add_todo_window)
        self.title_entry.pack(pady=5)

        tk.Label(self.add_todo_window, text="Description").pack(pady=5)
        self.description_entry = tk.Entry(self.add_todo_window)
        self.description_entry.pack(pady=5)

        tk.Label(self.add_todo_window, text="Status").pack(pady=5)
        self.status_combobox = ttk.Combobox(self.add_todo_window, values=["completed", "active", "dormant"])
        self.status_combobox.current(1)  # Set default status to 'active'
        self.status_combobox.pack(pady=5)

        add_button = tk.Button(self.add_todo_window, text="Add", command=self.save_todo)
        add_button.pack(pady=10)

    def save_todo(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        status = self.status_combobox.get()
        if title and description and status:
            self.todo_model.add_todo(self.user['_id'], title, description, status)
            self.load_todos()
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")
        self.add_todo_window.destroy()

    def update_todo(self, todo_id):
        todo = self.todo_model.collection.find_one({"_id": ObjectId(todo_id)})
        if not todo:
            return

        self.update_todo_window = tk.Toplevel(self.root)
        self.update_todo_window.title("Update Todo")
        self.update_todo_window.geometry("300x300")

        tk.Label(self.update_todo_window, text="Title").pack(pady=5)
        self.title_entry = tk.Entry(self.update_todo_window)
        self.title_entry.insert(0, todo['title'])
        self.title_entry.pack(pady=5)

        tk.Label(self.update_todo_window, text="Description").pack(pady=5)
        self.description_entry = tk.Entry(self.update_todo_window)
        self.description_entry.insert(0, todo['description'])
        self.description_entry.pack(pady=5)

        tk.Label(self.update_todo_window, text="Status").pack(pady=5)
        self.status_combobox = ttk.Combobox(self.update_todo_window, values=["completed", "active", "dormant"])
        self.status_combobox.set(todo.get('status', 'No status'))
        self.status_combobox.pack(pady=5)

        save_button = tk.Button(self.update_todo_window, text="Save", command=lambda: self.save_updated_todo(todo_id))
        save_button.pack(pady=10)

    def save_updated_todo(self, todo_id):
        new_title = self.title_entry.get()
        new_description = self.description_entry.get()
        new_status = self.status_combobox.get()
        if new_title and new_description and new_status:
            self.todo_model.update_todo(todo_id, new_title, new_description, new_status)
            self.load_todos()
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")
        self.update_todo_window.destroy()

    def delete_todo(self, todo_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this todo?"):
            self.todo_model.delete_todo(todo_id)
            self.load_todos()

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        todo_id = selected_item[0]

        self.action_window = tk.Toplevel(self.root)
        self.action_window.title("Todo Actions")

        edit_button = tk.Button(self.action_window, text="Edit", command=lambda: self.update_todo(todo_id))
        edit_button.pack(pady=5)

        delete_button = tk.Button(self.action_window, text="Delete", command=lambda: self.confirm_delete(todo_id))
        delete_button.pack(pady=5)

    def confirm_delete(self, todo_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this todo?"):
            self.delete_todo(todo_id)

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_todos()

    def next_page(self):
        total_todos = self.todo_model.collection.count_documents({"user_id": self.user['_id']})
        if self.current_page * self.page_size < total_todos:
            self.current_page += 1
            self.load_todos()
