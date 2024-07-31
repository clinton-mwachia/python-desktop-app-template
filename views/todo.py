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

        self.todos_per_page = 10
        self.current_page = 1

        self.todos_frame = tk.Frame(root)
        self.todos_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_todos_frame()

    def setup_todos_frame(self):
        self.add_button = tk.Button(self.todos_frame, text="Add Todo", command=self.add_todo)
        self.add_button.pack(pady=10)

        self.tree_frame = tk.Frame(self.todos_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview for displaying todos
        self.tree = ttk.Treeview(self.tree_frame, columns=("title", "description", "status", "actions"), show="headings")
        self.tree.heading("title", text="Title")
        self.tree.heading("description", text="Description")
        self.tree.heading("status", text="Status")
        self.tree.heading("actions", text="Actions")
        self.tree.column("actions", width=150, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

        # Pagination controls
        self.pagination_frame = tk.Frame(self.todos_frame)
        self.pagination_frame.pack(pady=10)
        self.prev_button = tk.Button(self.pagination_frame, text="Previous", command=self.prev_page)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.next_button = tk.Button(self.pagination_frame, text="Next", command=self.next_page)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.page_label = tk.Label(self.pagination_frame, text=f"Page {self.current_page}")
        self.page_label.pack(side=tk.LEFT, padx=5)

        self.load_todos()

    def load_todos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        start = (self.current_page - 1) * self.todos_per_page
        end = start + self.todos_per_page
        current_todos = self.todos[start:end]
        
        for todo in current_todos:
            self.tree.insert("", tk.END, iid=str(todo['_id']),
                             values=(todo['title'], todo['description'], todo.get('status', 'NA'), 'Edit/Delete'))

        self.update_pagination_controls()

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

        # Status label and combobox
        tk.Label(self.add_todo_window, text="Status").pack(pady=5)
        self.status_combobox = ttk.Combobox(self.add_todo_window, values=["completed", "active", "dormant"])
        self.status_combobox.current(1)  # Set default status to 'active'
        self.status_combobox.pack(pady=5)

        # Add button
        add_button = tk.Button(self.add_todo_window, text="Add", command=self.save_todo)
        add_button.pack(pady=10)

    def save_todo(self):
        user = self.todo_model.collection.find_one({"username": self.username})
        if user:
            title = self.title_entry.get()
            description = self.description_entry.get()
            status = self.status_combobox.get()
            if title and description and status:
                self.todo_model.add_todo(user["_id"], title, description, status)
                self.todos = list(self.todo_model.get_todos(self.user['_id']))
                self.load_todos()
            else:
                messagebox.showwarning("Input Error", "Please enter all fields.")
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

        # Status label and combobox
        tk.Label(self.update_todo_window, text="Status").pack(pady=5)
        self.status_combobox = ttk.Combobox(self.update_todo_window, values=["completed", "active", "dormant"])
        self.status_combobox.set(todo.get('status', 'No status'))
        self.status_combobox.pack(pady=5)

        # Save button
        save_button = tk.Button(self.update_todo_window, text="Save", command=lambda: self.save_updated_todo(todo_id))
        save_button.pack(pady=10)

    def save_updated_todo(self, todo_id):
        new_title = self.title_entry.get()
        new_description = self.description_entry.get()
        new_status = self.status_combobox.get()
        if new_title and new_description and new_status:
            self.todo_model.update_todo(todo_id, new_title, new_description, new_status)
            self.todos = list(self.todo_model.get_todos(self.user['_id']))
            self.load_todos()
        else:
            messagebox.showwarning("Input Error", "Please enter both title and description.")
        self.update_todo_window.destroy()  # Close the update todo window

    def delete_todo(self, todo_id):
        self.todo_model.delete_todo(todo_id)
        self.todos = list(self.todo_model.get_todos(self.user['_id']))
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

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_todos()

    def next_page(self):
        if self.current_page * self.todos_per_page < len(self.todos):
            self.current_page += 1
            self.load_todos()

    def update_pagination_controls(self):
        self.page_label.config(text=f"Page {self.current_page}")
        self.prev_button.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.current_page * self.todos_per_page < len(self.todos) else tk.DISABLED)
