from collections import defaultdict

def analyze(expenses):
    total = 0
    category_data = defaultdict(float)
    monthly_data = defaultdict(float)

    for e in expenses:
        try:
            amount = float(e.get("amount", 0))
            category = e.get("category", "Other")
            date = e.get("date")

            total += amount
            category_data[category] += amount

            if date and len(date) >= 7:
                month = date[:7]
                monthly_data[month] += amount

        except Exception as err:
            print("Error:", err)

    return total, dict(category_data), dict(monthly_data)


def top_category(category_data):
    if not category_data:
        return None
    return max(category_data, key=category_data.get)


def spending_insights(total, category_data):
    insights = []

    if total == 0:
        return ["No expenses found"]

    for cat, amt in category_data.items():
        percent = (amt / total) * 100

        if percent > 40:
            insights.append(f"⚠️ {cat} dominates spending ({percent:.1f}%)")
        elif percent < 5:
            insights.append(f"💡 Low spending on {cat}")

    return insights


def monthly_trend(monthly_data):
    if len(monthly_data) < 2:
        return "Not enough data"

    months = sorted(monthly_data.keys())

    first = monthly_data[months[0]]
    last = monthly_data[months[-1]]

    if last > first:
        return "📈 Spending increased"
    elif last < first:
        return "📉 Spending decreased"
    else:
        return "➡️ Stable"


def budget_analysis(total, category_data):

    needs_categories = ["food", "rent", "transport", "bills", "groceries"]
    wants_categories = ["shopping", "entertainment", "travel"]

    needs_total = 0
    wants_total = 0

    for cat, amt in category_data.items():
        cat = cat.lower()

        if cat in needs_categories:
            needs_total += amt
        elif cat in wants_categories:
            wants_total += amt

    insights = []

    if total > 0:
        if needs_total > total * 0.5:
            insights.append("❌ Needs too high")

        if wants_total > total * 0.3:
            insights.append("⚠️ Wants too high")

    return insights