import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from models.todo import TodoModel
from auth.auth import AuthController
from bson.objectid import ObjectId
from views.notification import NotificationManager
import csv

class TodoView:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.todo_model = TodoModel()
        self.page_size = 30
        self.current_page = 1

        # Get user information from AuthController
        self.auth_controller = AuthController()
        self.user = self.auth_controller.user_model.find_user(username)

        # search query and filter
        self.search_query = ""
        self.search_timer = None

        # filter status
        self.filter_status = "All"

        # sort
        self.sort_by = "title"

        # notification manager
        # Create a frame for the toolbar
        self.toolbar_frame = tk.Frame(root)
        self.toolbar_frame.pack(fill=tk.X)

        self.notification_manager = NotificationManager(self.toolbar_frame)

        self.todos_frame = tk.Frame(root)
        self.todos_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_todos_frame()
        self.load_todos()  # Load todos after setting up the UI

    def setup_todos_frame(self):
        # creating buttons frame
        self.button_frame = tk.Frame(self.todos_frame)
        self.button_frame.pack()

        # add todo button
        self.add_button = tk.Button(self.button_frame, text="Add Todo", command=self.add_todo)
        self.add_button.pack(side=tk.LEFT, pady=5)

        # export to csv button
        self.export_csv_button = tk.Button(self.button_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_csv_button.pack(side=tk.LEFT, pady=5)

         # upload data button
        self.upload_button = tk.Button(self.button_frame, text="Upload CSV", command=self.upload_csv)
        self.upload_button.pack(side=tk.LEFT, pady=5)

        # Add the progress bar frame
        self.progress_frame = tk.Frame(self.todos_frame)
        self.progress_frame.pack()

        # Add the progress bar
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(side=tk.LEFT, pady=5)

        # search input
        self.search_frame = tk.Frame(self.todos_frame)
        self.search_frame.pack(pady=5)

        tk.Label(self.search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        self.search_entry.insert(0, "Search Todos")
        self.search_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, "Search Todos"))
        self.search_entry.bind("<FocusOut>", lambda event: self.set_placeholder(event, "Search Todos"))

        # filter input
        self.filter_frame = tk.Frame(self.todos_frame)
        self.filter_frame.pack(pady=5)

        tk.Label(self.filter_frame, text="Filter By Status:").pack(side=tk.LEFT, padx=5)
        self.status_combobox = ttk.Combobox(self.filter_frame, values=["All", "completed", "active", "domant"])
        self.status_combobox.set("All")
        self.status_combobox.pack(side=tk.LEFT)
        self.status_combobox.bind("<<ComboboxSelected>>", self.on_filter_change)

        # sorting frame
        tk.Label(self.filter_frame, text="Sort By:").pack(side=tk.LEFT, padx=5)
        self.sort_combobox = ttk.Combobox(self.filter_frame, values=["NONE", "title", "status"])
        self.sort_combobox.set("NONE")
        self.sort_combobox.pack(side=tk.LEFT)
        self.sort_combobox.bind("<<ComboboxSelected>>", self.on_sort_change)

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

    def upload_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        self.preview_csv(file_path)

    def preview_csv(self, file_path):
        # Create a preview window to show the CSV content
        self.preview_window = tk.Toplevel(self.root)
        self.preview_window.title("CSV Preview")
        
        # Add a text widget to show CSV preview
        self.preview_text = tk.Text(self.preview_window)
        self.preview_text.pack(pady=10)
        
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.preview_text.insert(tk.END, ', '.join(row) + '\n')

        # Add buttons to confirm or cancel
        tk.Button(self.preview_window, text="Confirm", command=lambda: self.bulk_add_from_csv(file_path)).pack(pady=5)
        tk.Button(self.preview_window, text="Cancel", command=self.preview_window.destroy).pack(pady=5)

    def bulk_add_from_csv(self, file_path):
        todos_to_add = []
        total_lines = sum(1 for line in open(file_path, 'r')) - 1  # Exclude header line
        
        self.progress_bar['maximum'] = total_lines
        self.progress_bar['value'] = 0
        
        try:
            with open(file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for index, row in enumerate(reader):
                    title = row.get('title', '').strip()
                    description = row.get('description', '').strip()
                    status = row.get('status', '').strip()
                    if title:
                        todos_to_add.append({
                            'user_id': self.user['_id'],
                            'title': title.lower(),
                            'description': description.lower(),
                            'status': status.lower()
                        })

                    if len(todos_to_add) >= 1000:  # Process in chunks
                        self.todo_model.add_many_todos(todos_to_add)
                        self.notification_manager.add_notification(f"Bulk Todos: {len(todos_to_add)} todos added")
                        todos_to_add = []
                        self.progress_bar['value'] = index + 1
                        self.root.update_idletasks()

            if todos_to_add:
                self.todo_model.add_many_todos(todos_to_add)
                self.notification_manager.add_notification(f"Bulk Todos: {len(todos_to_add)} todos added")

            self.progress_bar['value'] = total_lines
            self.root.update_idletasks()

            self.load_todos()
            messagebox.showinfo("Success", "Todos have been bulk added from CSV.")
            self.preview_window.destroy()
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            print(f"An error occurred while processing the CSV file: {e}")


    def on_search(self, event):
        if self.search_timer:
            self.root.after_cancel(self.search_timer)
        self.search_timer = self.root.after(300, self.update_search_query)

    def update_search_query(self):
        self.search_query = self.search_entry.get()
        self.load_todos()

    def clear_placeholder(self, event, placeholder_text):
        if event.widget.get() == placeholder_text:
            event.widget.delete(0, tk.END)
            event.widget.config(fg="black")

    def set_placeholder(self, event, placeholder_text):
        if event.widget.get() == "":
            event.widget.insert(0, placeholder_text)
            event.widget.config(fg="grey")

    def on_filter_change(self, event):
        self.filter_status = self.status_combobox.get()
        self.load_todos()

    def on_sort_change(self, event):
        self.sort_by = self.sort_combobox.get()
        self.load_todos()

    def export_to_csv(self):
        todos = self.todo_model.collection.find({"user_id": self.user['_id']})
        filtered_todos = [todo for todo in todos if self.search_query.lower() in todo['title'].lower()]

        if self.filter_status != "All":
            filtered_todos = [todo for todo in filtered_todos if todo.get('status', '') == self.filter_status]

        with open('todos.csv', 'w', newline='') as csvfile:
            fieldnames = ['Title', 'Description', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for todo in filtered_todos:
                writer.writerow({'Title': todo['title'], 'Description': todo['description'], 'Status': todo.get('status','')})

        messagebox.showinfo("Export to CSV", "Todos have been exported to todos.csv")

    def load_todos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        total_todos = self.todo_model.collection.count_documents({"user_id": self.user['_id']})
        start = (self.current_page - 1) * self.page_size
        todos = self.todo_model.collection.find({"user_id": self.user['_id']}).skip(start).limit(self.page_size)
        filtered_todos = [todo for todo in todos if self.search_query.lower() in todo['title'].lower()]

        # filter todo based on filter
        if self.filter_status != "All":
            filtered_todos = [todo for todo in filtered_todos if todo.get('status', '') == self.filter_status]

        # handle sorting
        if self.sort_by == "NONE":
            filtered_todos
        elif self.sort_by == "title":
                    filtered_todos.sort(key=lambda x: x['title'])
        elif self.sort_by == "status":
                    filtered_todos.sort(key=lambda x: x.get('status', ''))

        if not filtered_todos:
            self.tree.insert("", tk.END, iid="no_todo", values=("No todos found", "", "", ""))
            self.prev_button.config(state=tk.DISABLED)
            self.next_button.config(state=tk.DISABLED)
        else:
            for todo in filtered_todos:
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
        title = self.title_entry.get().lower()
        description = self.description_entry.get().lower()
        status = self.status_combobox.get().lower()
        if title and description and status:
            self.todo_model.add_todo(self.user['_id'], title, description, status)
            self.load_todos()
            self.notification_manager.add_notification(f"New todo added: {title}")
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
        new_title = self.title_entry.get().lower()
        new_description = self.description_entry.get().lower()
        new_status = self.status_combobox.get().lower()
        if new_title and new_description and new_status:
            self.todo_model.update_todo(todo_id, new_title, new_description, new_status)
            self.load_todos()
            self.notification_manager.add_notification(f"todo updated: {new_title}")
        else:
            messagebox.showwarning("Input Error", "Please enter all fields.")
        self.update_todo_window.destroy()

    def delete_todo(self, todo_id):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this todo?"):
            self.todo_model.delete_todo(todo_id)
            self.load_todos()
            self.notification_manager.add_notification(f"todo deleted: {todo_id}")

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
