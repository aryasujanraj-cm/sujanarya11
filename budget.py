def budget_analysis(total, category_data):
    
    # 50-30-20 rule
    needs_limit = total * 0.5
    wants_limit = total * 0.3
    savings_limit = total * 0.2

    insights = []

    for category, amount in category_data.items():
        percent = (amount / total) * 100 if total > 0 else 0

        if percent > 40:
            insights.append(f"⚠️ High spending on {category} ({percent:.1f}%)")

        if amount > needs_limit:
            insights.append(f"❌ {category} exceeds recommended budget")

    return insights