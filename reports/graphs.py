import matplotlib.pyplot as plt

def show_graph(transactions):
    categories = {}

    for t in transactions:
        if t.type == "expense":
            categories[t.category] = categories.get(t.category, 0) + t.amount

    if not categories:
        return

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    # Bar Chart
    axs[0].bar(categories.keys(), categories.values())
    axs[0].set_title("Expenses by Category")
    axs[0].tick_params(axis='x', rotation=45)

    # Pie Chart
    axs[1].pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
    axs[1].set_title("Expense Distribution")

    plt.tight_layout()
    plt.show()