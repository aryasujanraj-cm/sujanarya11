import json
import os
from datetime import datetime

FILE = "expenses.json"

def load_expenses():
    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_expense(amount, category, merchant="Unknown"):
    data = load_expenses()

    expense = {
        "amount": float(amount),
        "category": category,
        "merchant": merchant,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    data.append(expense)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)