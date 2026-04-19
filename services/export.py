import csv

def export_csv(transactions):
    with open("transactions.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Amount", "Category", "Type", "Date"])

        for t in transactions:
            if isinstance(t, tuple):
                writer.writerow([t[0], t[1], t[2], t[3]])
            else:
                writer.writerow([t.amount, t.category, t.type, t.date])