import tkinter as tk
from views.login import LoginView

def main():
    root = tk.Tk()
    LoginView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
