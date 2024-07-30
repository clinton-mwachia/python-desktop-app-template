import tkinter as tk
from views.login import LoginView
from views.dashboard import DashboardView

class App:
    def __init__(self, root):
        self.root = root
        self.sidebar_frame = None
        self.content_frame = None
        self.login_view = None

        self.show_login()

    def show_login(self):
        self.clear_frames()
        self.login_view = LoginView(self.root, self.show_dashboard)

    def show_dashboard(self, username):
        self.clear_frames()
        self.sidebar_frame = tk.Frame(self.root, width=200, bg='gray')
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.dashboard_view = DashboardView(self.sidebar_frame, self.content_frame, username)

    def clear_frames(self):
        if self.sidebar_frame:
            self.sidebar_frame.destroy()
        if self.content_frame:
            self.content_frame.destroy()
        if self.login_view:
            self.login_view.frame.destroy()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
