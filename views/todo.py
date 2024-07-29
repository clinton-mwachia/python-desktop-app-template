import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
from models.todo import TodoModel
from auth.auth import AuthController

class TodoView:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.auth_controller = AuthController()
        self.todo_model = TodoModel()

        self.user = self.auth_controller.user_model.find_user(username)
        self.todos = list(self.todo_model.get_todos(self.user['_id']))

        self.todos_frame = tk.Frame(root)
        self.todos_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_todos_frame()

    def setup_todos_frame(self):
        self.add_button = tk.Button(self.todos_frame, text="Add Todo", command=self.add_todo)
        self.add_button.pack(pady=10)

        self.tree_frame = tk.Frame(self.todos_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for displaying todos
        self.tree = ttk.Treeview(self.tree_frame, columns=("title", "description", "actions"), show="headings")
        self.tree.heading("title", text="Title")
        self.tree.heading("description", text="Description")
        self.tree.heading("actions", text="Actions")
        self.tree.column("actions", width=150, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

        self.load_todos()

    def load_todos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.todos = list(self.todo_model.get_todos(self.user['_id']))
        for todo in self.todos:
            self.tree.insert("", tk.END, iid=str(todo['_id']),
                             values=(todo['title'], todo['description'], 'Edit/Delete'))

    def add_todo(self):
        # Create a new top-level window for adding a todo
        self.add_todo_window = tk.Toplevel(self.root)
        self.add_todo_window.title("Add Todo")

        # Title label and entry
        tk.Label(self.add_todo_window, text="Title").pack(pady=5)
        self.title_entry = tk.Entry(self.add_todo_window)
        self.title_entry.pack(pady=5)

        # Description label and entry
        tk.Label(self.add_todo_window, text="Description").pack(pady=5)
        self.description_entry = tk.Entry(self.add_todo_window)
        self.description_entry.pack(pady=5)

        # Add button
        add_button = tk.Button(self.add_todo_window, text="Add", command=self.save_todo)
        add_button.pack(pady=10)

    def save_todo(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        if title and description:
            self.todo_model.add_todo(self.user['_id'], title, description)
            self.load_todos()
        else:
            messagebox.showwarning("Input Error", "Please enter both title and description.")
        self.add_todo_window.destroy()  # Close the add todo window

    def update_todo(self, todo_id):
        todo = next((t for t in self.todos if t['_id'] == todo_id), None)
        if not todo:
            return

        # Create a new top-level window for updating a todo
        self.update_todo_window = tk.Toplevel(self.root)
        self.update_todo_window.title("Update Todo")

        # Title label and entry
        tk.Label(self.update_todo_window, text="Title").pack(pady=5)
        self.title_entry = tk.Entry(self.update_todo_window)
        self.title_entry.insert(0, todo['title'])
        self.title_entry.pack(pady=5)

        # Description label and entry
        tk.Label(self.update_todo_window, text="Description").pack(pady=5)
        self.description_entry = tk.Entry(self.update_todo_window)
        self.description_entry.insert(0, todo['description'])
        self.description_entry.pack(pady=5)

        # Save button
        save_button = tk.Button(self.update_todo_window, text="Save", command=lambda: self.save_updated_todo(todo_id))
        save_button.pack(pady=10)

    def save_updated_todo(self, todo_id):
        new_title = self.title_entry.get()
        new_description = self.description_entry.get()
        if new_title and new_description:
            self.todo_model.update_todo(todo_id, new_title, new_description)
            self.load_todos()
        else:
            messagebox.showwarning("Input Error", "Please enter both title and description.")
        self.update_todo_window.destroy()  # Close the update todo window

    def delete_todo(self, todo_id):
        self.todo_model.delete_todo(todo_id)
        self.load_todos()

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item_id = selected_item[0]
        todo_id = self.todos[self.tree.index(item_id)]['_id']

        # Create a new top-level window with Edit and Delete buttons
        self.action_window = tk.Toplevel(self.root)
        self.action_window.title("Todo Actions")

        # Edit button
        edit_button = tk.Button(self.action_window, text="Edit", command=lambda: self.update_todo(todo_id))
        edit_button.pack(pady=5)

        # Delete button
        delete_button = tk.Button(self.action_window, text="Delete", command=lambda: self.confirm_delete(todo_id))
        delete_button.pack(pady=5)

    def confirm_delete(self, todo_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this todo?"):
            self.delete_todo(todo_id)
