import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os

class NotificationManager:
    def __init__(self, parent_frame):
        # notifications and settings manager
        self.notifications_file = "notifications.json"
        self.settings_file = "settings.json"
        self.settings = self.load_settings()
        self.notifications = self.load_notifications()
        
        # Load the notification icon
        #self.icon = tk.PhotoImage(file="notification_icon.png") 
        
        # Create a button for notifications
        self.notification_button = tk.Button(parent_frame, text="Notification",command=self.show_notifications)
        self.notification_button.pack(side=tk.RIGHT, padx=10)
        
        # Label to show the number of notifications
        self.notification_count_label = tk.Label(parent_frame, text="0", bg="red", fg="white", font=("Arial", 12, "bold"))
        self.notification_count_label.pack(side=tk.RIGHT, padx=5)
        
        if self.notifications:
            self.update_notification_count()
        else:
            self.notification_count_label.place_forget()  # Hide the label initially

         # Add settings button
        self.settings_button = tk.Button(parent_frame, text="Settings", command=self.open_settings)
        self.settings_button.pack(side=tk.RIGHT, padx=10)

        # Apply settings
        self.apply_settings()

    # notifications functions
    def add_notification(self, message):
        self.notifications.append(message)
        self.save_notifications()
        self.update_notification_count()

    def show_notifications(self):
        if not self.notifications:
            messagebox.showinfo("Notifications", "No new notifications.")
            return

        self.notification_window = tk.Toplevel()
        self.notification_window.title("Notifications")
        self.notification_window.geometry("300x400")

        notification_listbox = tk.Listbox(self.notification_window)
        for notification in self.notifications:
            notification_listbox.insert(tk.END, notification)
        notification_listbox.pack(fill=tk.BOTH, expand=True)

        clear_button = tk.Button(self.notification_window, text="Clear Notifications", command=self.clear_notifications)
        clear_button.pack(pady=10)

    def clear_notifications(self):
        self.notifications.clear()
        self.save_notifications()
        self.update_notification_count()
        self.notification_window.destroy()

    def save_notifications(self):
        with open(self.notifications_file, "w") as file:
            json.dump(self.notifications, file)

    def load_notifications(self):
        if os.path.exists(self.notifications_file):
            with open(self.notifications_file, "r") as file:
                return json.load(file)
        return []

    def update_notification_count(self):
        self.notification_count_label.config(text=f"{len(self.notifications)}")
        self.notification_count_label.place(relx=0.98, rely=0.1) 

    # settings functions
    def open_settings(self):
        self.settings_window = tk.Toplevel()
        self.settings_window.title("Settings")
        self.settings_window.geometry("400x300")
        
        tk.Label(self.settings_window, text="Theme").pack(pady=5)
        self.theme_var = tk.StringVar(value=self.settings.get("theme", "Light"))
        theme_options = ["Light", "Dark"]
        self.theme_combobox = ttk.Combobox(self.settings_window, textvariable=self.theme_var, values=theme_options)
        self.theme_combobox.pack(pady=5)

        tk.Label(self.settings_window, text="Add settings").pack(pady=5)
        
        save_button = tk.Button(self.settings_window, text="Save", command=self.save_settings)
        save_button.pack(pady=10)

    def save_settings(self):
        self.settings["theme"] = self.theme_var.get()
        self.apply_settings()
        self.settings_window.destroy()
        self.save_settings_to_file()

    def apply_settings(self):
        theme = self.settings.get("theme", "Light")
        
        if theme == "Dark":
            self.notification_button.config(bg="black", fg="white")
            self.notification_count_label.config(bg="black", fg="white")
            self.settings_button.config(bg="black", fg="white")
        else:
            self.notification_button.config(bg="white", fg="black")
            self.notification_count_label.config(bg="white", fg="black")
            self.settings_button.config(bg="white", fg="black")

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as file:
                return json.load(file)
        return {}

    def save_settings_to_file(self):
        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file)

