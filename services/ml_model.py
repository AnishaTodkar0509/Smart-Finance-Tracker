def predict_expense_with_suggestion(transactions):
    import pandas as pd
    from sklearn.linear_model import LinearRegression

    data = []
    total_income = 0

    for t in transactions:
        if t.type == "expense":
            month = t.date.month
            data.append([month, t.amount])
        elif t.type == "income":
            total_income += t.amount

    if len(data) < 2:
        return "Not enough data for prediction"

    df = pd.DataFrame(data, columns=["month", "amount"])
    df = df.groupby("month").sum().reset_index()

    X = df[["month"]]
    y = df["amount"]

    model = LinearRegression()
    model.fit(X, y)

    next_month = [[df["month"].max() + 1]]
    prediction = model.predict(next_month)[0]

    # 🔥 Add suggestion logic
    message = f"Predicted expense: ₹{prediction:.2f}\n"

    if total_income > 0 and prediction > total_income:
        message += "⚠️ You may overspend next month!"

    elif total_income > 0 and prediction > 0.8 * total_income:
        message += "💡 Your expenses may be high. Try to control spending."

    else:
        message += "✅ Your predicted spending looks balanced."

    return message