from datetime import datetime


class Purchase:
    def __init__(self, name, category, amount, date = None):
        self.name = name
        self.category = category
        self.amount = amount
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f'Expense = {self.name}, category = {self.category}, amount = {self.amount:.2f} | {self.date}'
