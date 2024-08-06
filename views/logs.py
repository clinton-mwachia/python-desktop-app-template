import tkinter as tk
from tkinter import ttk

class LogsView:
    def __init__(self, root):
        self.root = root
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.add_logs_tab()
        self.load_logs()

    def add_logs_tab(self):
        self.logs_tab = tk.Frame(self.notebook)
        self.notebook.add(self.logs_tab, text="User Logs")

        self.logs_text = tk.Text(self.logs_tab, wrap=tk.WORD)
        self.logs_text.pack(fill=tk.BOTH, expand=True)

    def load_logs(self):
        self.logs_text.delete(1.0, tk.END)

        try:
            with open("logs/activity.log", "r") as file:
                activity_logs = file.read()
            with open("logs/error.log", "r") as file:
                error_logs = file.read()

            self.logs_text.insert(tk.END, "Activity Logs:\n")
            self.logs_text.insert(tk.END, activity_logs + "\n\n")
            self.logs_text.insert(tk.END, "Error Logs:\n")
            self.logs_text.insert(tk.END, error_logs)

        except Exception as e:
            self.logs_text.insert(tk.END, f"Error loading logs: {e}")