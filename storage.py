import json
import os

FILE = "expenses.json"

def save_expense(amount, category):
    expense = {
        "amount": float(amount),
        "category": category
    }

    data = load_expenses()
    data.append(expense)

    with open(FILE, "w") as f:
        json.dump(data, f)

def load_expenses():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []