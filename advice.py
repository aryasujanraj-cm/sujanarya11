def load_guru():
    try:
        with open("guru.txt") as f:
            return f.read().split("\n")
    except:
        return []


def give_advice(total, category_data):
    advice = []

    if total == 0:
        return ["No data available"]

    if category_data.get("Food", 0) > 0.4 * total:
        advice.append("⚠️ You are spending too much on food.")

    if category_data.get("Shopping", 0) > 0.3 * total:
        advice.append("⚠️ Reduce shopping expenses.")

    savings = total * 0.2
    advice.append(f"💰 Try to save ₹{savings:.0f}")

    # Add guru tip
    guru = load_guru()
    if guru:
        advice.append("📘 Tip: " + guru[0])

    return advice