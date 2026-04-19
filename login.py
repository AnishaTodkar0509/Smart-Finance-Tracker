import tkinter as tk
from tkinter import messagebox
from database.db import login_user, register_user

def login_screen(start_app):

    def login():
        username = user_entry.get()
        password = pass_entry.get()

        user_id = login_user(username, password)

        if user_id:
            messagebox.showinfo("Success", "Login Successful")
            login_window.destroy()
            start_app(user_id, username)
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    def register():
        username = user_entry.get()
        password = pass_entry.get()

        if register_user(username, password):
            messagebox.showinfo("Success", "User Registered")
        else:
            messagebox.showerror("Error", "User already exists")

    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username").pack(pady=5)
    user_entry = tk.Entry(login_window)
    user_entry.pack()

    tk.Label(login_window, text="Password").pack(pady=5)
    pass_entry = tk.Entry(login_window, show="*")
    pass_entry.pack()

    tk.Button(login_window, text="Login", command=login).pack(pady=5)
    tk.Button(login_window, text="Register", command=register).pack(pady=5)

    login_window.mainloop()