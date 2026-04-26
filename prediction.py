import json
from collections import defaultdict

def load_expenses():
    try:
        with open("expenses.json", "r") as f:
            return json.load(f)
    except:
        return []

def predict_monthly_spending():
    expenses = load_expenses()

    monthly_totals = defaultdict(float)

    for exp in expenses:
        date = exp.get("date")
        amount = float(exp.get("amount", 0))

        if not date or len(date) < 7:
            continue

        month = date[:7]
        monthly_totals[month] += amount

    if len(monthly_totals) < 2:
        return "Not enough data"

    months = sorted(monthly_totals.keys())[-3:]
    avg = sum(monthly_totals[m] for m in months) / len(months)

    return round(avg, 2)


def category_prediction():
    expenses = load_expenses()

    category_totals = defaultdict(float)

    for exp in expenses:
        cat = exp.get("category", "Other")
        amt = float(exp.get("amount", 0))
        category_totals[cat] += amt

    return dict(category_totals)