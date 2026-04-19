from datetime import datetime

class Transaction:
    def __init__(self, amount, category, t_type, date=None):
        self.amount = amount
        self.category = category
        self.type = t_type
        self.date = date if date else datetime.now()