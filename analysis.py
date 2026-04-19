def analyze(expenses):
    total = sum(e["amount"] for e in expenses)

    category_data = {}
    for e in expenses:
        cat = e["category"]
        category_data[cat] = category_data.get(cat, 0) + e["amount"]

    return total, category_data