import tkinter as tk
from tkinter import messagebox

class NotificationManager:
    def __init__(self, parent_frame):
        self.notifications = []
        
        # Load the notification icon
        #self.icon = tk.PhotoImage(file="notification_icon.png")
        
        # Create a button for notifications
        self.notification_button = tk.Button(parent_frame, command=self.show_notifications)
        self.notification_button.pack(side=tk.RIGHT, padx=10)
        
        # Label to show the number of notifications
        self.notification_count_label = tk.Label(parent_frame, text="0", bg="red", fg="white", font=("Arial", 12, "bold"))
        self.notification_count_label.pack(side=tk.RIGHT, padx=5)
        self.notification_count_label.place_forget()  # Hide the label initially

    def add_notification(self, message):
        self.notifications.append(message)
        self.notification_count_label.config(text=f"{len(self.notifications)}")
        self.notification_count_label.place(relx=0.95, rely=0.1)  # Adjust position as needed

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
        self.notification_count_label.config(text="0")
        self.notification_count_label.place_forget()
        self.notification_window.destroy()
