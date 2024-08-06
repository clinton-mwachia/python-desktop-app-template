import tkinter as tk
from tkinter import ttk
from views.todo import TodoView
from views.user import UserView
from views.profile import ProfileView
from views.logs import LogsView
from models.user import UserModel
from models.todo import TodoModel
import logging

# Initialize the logger
logger = logging.getLogger("application_logger")

class DashboardView:
    def __init__(self, sidebar_frame, content_frame, username, logout_callback):
        self.sidebar_frame = sidebar_frame
        self.content_frame = content_frame
        self.username = username
        self.logout_callback = logout_callback
        self.user_model = UserModel()
        self.todo_model = TodoModel()

        self.user_role = self.user_model.find_user(self.username)

        self.setup_sidebar()

        # Initially show the dashboard view
        self.show_dashboard()

    def setup_sidebar(self):
        tk.Button(self.sidebar_frame, text="Dashboard", command=self.show_dashboard, width=15).pack(fill=tk.X)
        tk.Button(self.sidebar_frame, text="Todos", command=self.show_todos).pack(fill=tk.X)
        if self.user_role['role'] == 'admin':
             tk.Button(self.sidebar_frame, text="Users", command=self.show_users).pack(fill=tk.X)
             tk.Button(self.sidebar_frame, text="Logs", command=self.show_logs).pack(fill=tk.X)
        tk.Button(self.sidebar_frame, text="Profile", command=self.show_profile).pack(fill=tk.X)
        tk.Button(self.sidebar_frame, text="Logout", command=self.logout).pack(fill=tk.X)

    def show_dashboard(self):
        self.clear_content()
        self.create_summary_boxes()
        self.todos_by_status_table()
        self.create_latest_todos_table()

    def show_todos(self):
        self.clear_content()
        TodoView(self.content_frame, self.username)

    def show_logs(self):
        self.clear_content()
        LogsView(self.content_frame)

    def show_users(self):
        self.clear_content()
        UserView(self.content_frame)

    def show_profile(self):
        self.clear_content()
        ProfileView(self.content_frame, self.username)

    def logout(self):
        self.clear_content()
        logger.info(f"{self.username} logged out")
        self.logout_callback()  

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def create_summary_boxes(self):
         # Get the user object to retrieve user ID
        user = self.user_model.find_user(self.username)
        user_id = user["_id"]

        # Top Frame for Summary Boxes
        top_frame = tk.Frame(self.content_frame,bg="gray")
        top_frame.pack(fill=tk.BOTH,pady=(45,0), padx=5)

        # Configure grid layout to expand with window size
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=1)

        # Summary Box for Total Todos
        total_todos = self.todo_model.get_total_todos(user_id)  
        # Summary Box for Total Users
        total_users = self.user_model.get_total_users()
        # Summary Box for Total Completed Todos
        completed_todos = self.todo_model.get_completed_todos()

        # Create beautiful boxes for summary stats
        self.create_summary_box(top_frame, "Total Users", total_users, 0, 0)
        self.create_summary_box(top_frame, "Total Todos", total_todos, 0, 1)
        self.create_summary_box(top_frame, "Completed Todos", completed_todos, 0, 2)


    # create summary box
    def create_summary_box(self, parent, title, value, row, column):
        frame = ttk.LabelFrame(parent, text=title, padding=(5,2))
        frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        value_label = ttk.Label(frame, text=str(value), font=("Helvetica", 24, "bold"))
        value_label.grid(row=0, column=0, pady=5, padx=5)

    def todos_by_status_table(self):
        table_frame = tk.Frame(self.content_frame, padx=5, pady=5)
        table_frame.pack(fill=tk.BOTH, padx=5, pady=5)

         # Title label
        title_label = tk.Label(table_frame, text="Todos by Status", font=("Helvetica", 16))
        title_label.pack(pady=10)

        statuses = [
            ("Completed", self.todo_model.count_todos_by_status("completed")),
            ("Active", self.todo_model.count_todos_by_status("active")),
            ("Domant", self.todo_model.count_todos_by_status("domant"))
        ]

        # Determine the number of rows
        num_rows = len(statuses)

        # Create the Treeview widget
        columns = ("status", "count")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=num_rows)
        tree.heading("status", text="Status")
        tree.heading("count", text="Count")
        tree.column("status", anchor=tk.CENTER, width=150)
        tree.column("count", anchor=tk.CENTER, width=100)

        # Insert data into the table
        for status, count in statuses:
            tree.insert("", tk.END, values=(status, count))

        # Pack the Treeview widget with adjusted padding
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5)) 

    def create_latest_todos_table(self):
        latest_todos = self.todo_model.get_latest_todos()
        rows_to_display = len(latest_todos)

        latest_table_frame = tk.Frame(self.content_frame, padx=5, pady=5)
        latest_table_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        # Title label
        title_label = tk.Label(latest_table_frame, text="Latest Added Todos", font=("Helvetica", 16))
        title_label.pack(pady=10)
        
        # Set a minimum height to avoid an empty table
        min_height = 5
        table_height = max(min_height, rows_to_display)
        self.latest_todos_table = ttk.Treeview(latest_table_frame, columns=('Title', 'Description', 'Status', 'Created At'), show='headings', height=table_height)
        self.latest_todos_table.heading('Title', text='Title')
        self.latest_todos_table.heading('Description', text='Description')
        self.latest_todos_table.heading('Status', text='Status')
        self.latest_todos_table.heading('Created At', text='Created At')
        self.latest_todos_table.pack(expand=True, fill='both')

        self.load_latest_todos()

    def load_latest_todos(self):
        latest_todos = self.todo_model.get_latest_todos()
        for todo in latest_todos:
            self.latest_todos_table.insert('', 'end', values=(todo['title'], todo['description'],todo.get('status',''),todo.get('created_at','')))


