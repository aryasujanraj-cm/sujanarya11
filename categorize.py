def categorize(text):
    text = text.lower()

    if "zomato" in text or "swiggy" in text:
        return "Food"
    elif "uber" in text or "ola" in text:
        return "Transport"
    elif "amazon" in text or "flipkart" in text:
        return "Shopping"
    else:
        return "Other"