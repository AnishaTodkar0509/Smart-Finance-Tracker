import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from models.transaction import Transaction
from services.tracker import FinanceTracker
from database.db import create_table, insert_transaction, get_user_transactions
from services.analytics import monthly_report
from reports.graphs import show_graph
from services.export import export_csv
from services.ml_model import predict_expense_with_suggestion
from login import login_screen

tracker = FinanceTracker()
create_table()

# 🎨 COLORS
BG = "#f4f6f9"
SUCCESS = "#22c55e"
DANGER = "#ef4444"
INFO = "#3b82f6"
ACCENT = "#0ea5e9"
WARNING = "#f59e0b"
PRIMARY = "#4f46e5"
DARK = "#1e293b"


# 🔴 MAIN APP FUNCTION
def start_app(user_id, username):
    global current_user_id
    current_user_id = user_id

    # ✅ Clear previous data
    tracker.transactions = []

    # ✅ Load user data
    data = get_user_transactions(current_user_id)
    for d in data:
        t = Transaction(d[0], d[1], d[2])
        tracker.add_transaction(t)

    root = tk.Tk()
    root.title("Smart Finance Tracker")
    root.geometry("650x720")
    root.configure(bg=BG)

    tk.Label(root, text="Personal Finance Tracker",
             font=("Segoe UI", 18, "bold"),
             bg=BG, fg=DARK).pack(pady=10)

    # ✅ Welcome user
    tk.Label(root,
             text=f"Welcome, {username} 👋",
             font=("Segoe UI", 12),
             bg=BG, fg="#555").pack()

    frame = tk.Frame(root, bg=BG)
    frame.pack(pady=10)

    # Amount
    tk.Label(frame, text="Amount", bg=BG).grid(row=0, column=0, padx=10, pady=5)
    amount_entry = tk.Entry(frame, width=20)
    amount_entry.grid(row=0, column=1)

    # Category
    categories = [
        "Food", "Travel", "Rent", "Shopping", "Bills",
        "Salary", "Entertainment", "Health", "Education",
        "Groceries", "Fuel", "Business", "Freelancing",
        "Part-Time Job", "Investments", "Stock Profit",
        "Mutual Funds", "Bonus", "Rental Income",
        "Commission", "Pension", "Scholarship",
        "Gift", "Online Earnings", "Other Income", "Other Expense"
    ]

    tk.Label(frame, text="Category", bg=BG).grid(row=1, column=0, padx=10, pady=5)
    category_combo = ttk.Combobox(frame, values=categories, state="readonly", width=18)
    category_combo.grid(row=1, column=1)
    category_combo.set("Select Category")

    # Month
    tk.Label(frame, text="Month", bg=BG).grid(row=2, column=0, padx=10, pady=5)
    months = [f"2026-{str(i).zfill(2)}" for i in range(1, 13)]
    month_combo = ttk.Combobox(frame, values=months, width=18)
    month_combo.grid(row=2, column=1)
    month_combo.set(datetime.now().strftime("%Y-%m"))

    # FUNCTIONS
    def add_transaction(t_type):
        try:
            amount = float(amount_entry.get().strip())
            category = category_combo.get().strip()

            if not category or category == "Select Category":
                raise ValueError

            t = Transaction(amount, category, t_type)
            tracker.add_transaction(t)

            insert_transaction(t, current_user_id)

            tree.insert("", "end", values=(t.amount, t.category, t.type))

            messagebox.showinfo("Success", "Transaction Added")

            amount_entry.delete(0, tk.END)
            category_combo.set("Select Category")

        except ValueError:
            messagebox.showerror("Error", "Enter valid amount and select category")

    def add_income():
        add_transaction("income")

    def add_expense():
        add_transaction("expense")

    def show_balance():
        messagebox.showinfo("Balance", f"Balance: ₹{tracker.get_balance()}")

    def show_chart():
        show_graph(tracker.transactions)

    # ✅ Export only current user data
    def export_data():
        data = get_user_transactions(current_user_id)
        export_csv(data)
        messagebox.showinfo("Export", "CSV Exported")

    def show_monthly_report():
        result = monthly_report(tracker.transactions, month_combo.get())
        messagebox.showinfo("Monthly Report", result)

    def show_prediction():
        result = predict_expense_with_suggestion(tracker.transactions)
        messagebox.showinfo("Prediction + Suggestions", result)

    # ✅ Logout
    def logout():
        root.destroy()
        login_screen(start_app)

    # BUTTON FRAME
    btn_frame = tk.Frame(root, bg=BG)
    btn_frame.pack(pady=25, fill="x")

    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)

    def create_button(text, command, row, col, color):
        btn = tk.Button(
            btn_frame,
            text=text,
            command=command,
            bg=color,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            height=2,
            relief="flat",
            cursor="hand2"
        )

        btn.grid(row=row, column=col, padx=20, pady=10, sticky="ew")

        def on_enter(e):
            btn.config(bg=DARK)

        def on_leave(e):
            btn.config(bg=color)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # BUTTONS
    create_button("Add Income", add_income, 0, 0, SUCCESS)
    create_button("Add Expense", add_expense, 0, 1, DANGER)

    create_button("Balance", show_balance, 1, 0, INFO)
    create_button("Graph", show_chart, 1, 1, ACCENT)

    create_button("Export", export_data, 2, 0, WARNING)
    create_button("Predict", show_prediction, 2, 1, PRIMARY)

    # Monthly Report
    create_button("Monthly Report", show_monthly_report, 3, 0, "#6366f1")
    btn_frame.grid_slaves(row=3, column=0)[0].grid(columnspan=2)

    # Logout button
    create_button("Logout", logout, 4, 0, "#6b7280")
    btn_frame.grid_slaves(row=4, column=0)[0].grid(columnspan=2)

    # TABLE
    columns = ("Amount", "Category", "Type")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=8)

    for col in columns:
        tree.heading(col, text=col)

    tree.pack(pady=20, fill="x")

    # ✅ Show old data in table
    for d in data:
        tree.insert("", "end", values=(d[0], d[1], d[2]))

    root.mainloop()


# 🔵 START WITH LOGIN
login_screen(start_app)