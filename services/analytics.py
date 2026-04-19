def analyze(transactions):
    result = {}
    for t in transactions:
        if t.type == "expense":
            result[t.category] = result.get(t.category, 0) + t.amount
    return str(result)

def monthly_report(transactions, selected_month):
    income = 0
    expense = 0

    for t in transactions:
        month = t.date.strftime("%Y-%m")

        if month != selected_month:
            continue

        if t.type == "income":
            income += t.amount
        else:
            expense += t.amount

    balance = income - expense

    return f"""
Month: {selected_month}
Income: {income}
Expense: {expense}
Balance: {balance}
"""