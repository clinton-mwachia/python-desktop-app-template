import tkinter as tk
from tkinter import messagebox
import json
import os

class NotificationManager:
    def __init__(self, parent_frame):
        self.notifications_file = "notifications.json"
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
