def budget_analysis(total, category_data):

    # 🔹 50-30-20 Rule Limits
    needs_limit = total * 0.5
    wants_limit = total * 0.3
    savings_limit = total * 0.2

    insights = []

    # 🔹 Category Classification
    needs_categories = ["Food", "Rent", "Transport", "Bills", "Groceries"]
    wants_categories = ["Shopping", "Entertainment", "Dining", "Travel"]
    savings_categories = ["Investment", "Savings"]

    needs_total = 0
    wants_total = 0
    savings_total = 0

    # 🔹 Calculate totals
    for category, amount in category_data.items():

        if category in needs_categories:
            needs_total += amount

        elif category in wants_categories:
            wants_total += amount

        elif category in savings_categories:
            savings_total += amount

    # 🔥 Rule Check
    if needs_total > needs_limit:
        insights.append(f"❌ Needs spending too high: ₹{needs_total:.0f} / ₹{needs_limit:.0f}")

    if wants_total > wants_limit:
        insights.append(f"⚠️ Wants spending too high: ₹{wants_total:.0f} / ₹{wants_limit:.0f}")

    if savings_total < savings_limit:
        insights.append(f"💡 Increase savings: ₹{savings_total:.0f} / ₹{savings_limit:.0f}")

    # 🔹 Category-wise analysis
    for category, amount in category_data.items():

        percent = (amount / total) * 100 if total > 0 else 0

        if percent > 40:
            insights.append(f"⚠️ High spending on {category} ({percent:.1f}%)")

        if percent < 5:
            insights.append(f"💡 Very low spending on {category} ({percent:.1f}%)")

    # 🔹 Overall health score
    if total > 0:
        savings_rate = (savings_total / total) * 100

        if savings_rate < 10:
            insights.append("❌ Poor savings habit (<10%)")
        elif savings_rate < 20:
            insights.append("⚠️ Average savings (10-20%)")
        else:
            insights.append("✅ Good savings habit")

    return insights