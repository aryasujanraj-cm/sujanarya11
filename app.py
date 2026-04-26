# =========================
# app.py (FINAL VERSION)
# =========================

import streamlit as st
from PIL import Image
import pandas as pd
import PyPDF2

from categorize import categorize
from extract import extract_text_and_amount, extract_details
from storage import save_expense, load_expenses

from analysis import analyze, top_category, spending_insights, monthly_trend, budget_analysis
from prediction import predict_monthly_spending, category_prediction


# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Financial Advisor AI",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Financial Advisor & Expense Manager AI")


# ---------------- MENU ----------------
menu = st.sidebar.radio(
    "Select Feature",
    [
        "Home",
        "Upload Screenshot",
        "Manual Entry",
        "CSV Upload",
        "Analysis",
        "Budget Tracker",
        "Guru AI",
        "Splitwise"
    ]
)


# ---------------- HOME ----------------
if menu == "Home":
    st.subheader("Welcome")
    st.write("Use sidebar to navigate through features.")


# ---------------- OCR ----------------
elif menu == "Upload Screenshot":

    st.subheader("📤 Upload Screenshot / Receipt")

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:

        # Show image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Extract text using EasyOCR
        text, _ = extract_text_and_amount(uploaded_file)

        # Smart extraction
        merchant, amount, currency = extract_details(text)

        # Debug OCR output
        st.subheader("🔍 RAW OCR TEXT")
        st.text_area("OCR Output", text, height=200)

        # Display extracted values
        st.subheader("🏪 Merchant")
        st.write(merchant)

        st.subheader("💰 Amount")
        st.write(f"{currency} {amount}")

        # Category detection
        category = categorize(text)

        st.subheader("📂 Category")
        st.write(category)

        # Save
        if amount > 0:
            if st.button("Save Expense"):
                save_expense(amount, category, merchant)
                st.success("Expense Saved")
        else:
            st.warning("Amount not detected properly")


# ---------------- MANUAL ----------------
elif menu == "Manual Entry":

    st.subheader("✍️ Manual Expense")

    amount = st.number_input("Amount", min_value=0.0)
    category = st.text_input("Category")

    if st.button("Add Expense"):
        if amount > 0 and category:
            save_expense(amount, category)
            st.success("Expense Added")
        else:
            st.warning("Enter valid data")


# ---------------- CSV ----------------
elif menu == "CSV Upload":

    st.subheader("📂 Upload CSV")

    csv_file = st.file_uploader("Upload CSV File", type=["csv"])

    if csv_file is not None:

        df = pd.read_csv(csv_file)
        st.dataframe(df)

        if "amount" in df.columns and "category" in df.columns:

            for _, row in df.iterrows():
                save_expense(row["amount"], row["category"])

            st.success("CSV Imported")
        else:
            st.error("CSV must contain amount and category columns")


# ---------------- ANALYSIS ----------------
elif menu == "Analysis":

    st.subheader("📊 Advanced Analysis")

    expenses = load_expenses()

    if not expenses:
        st.warning("No expenses found")
    else:
        total, cat_data, monthly_data = analyze(expenses)

        st.metric("Total Spending", f"₹ {total:.2f}")

        st.subheader("Category Breakdown")
        st.bar_chart(cat_data)

        st.subheader("Top Category")
        st.write(top_category(cat_data))

        st.subheader("📈 Trend")
        st.write(monthly_trend(monthly_data))

        st.subheader("💡 Insights")
        for i in spending_insights(total, cat_data):
            st.info(i)

        st.subheader("💰 Budget Health")
        for i in budget_analysis(total, cat_data):
            st.warning(i)

        st.subheader("🤖 Prediction")
        pred = predict_monthly_spending()
        st.write(f"Next Month Estimate: ₹{pred}")

        st.write("Category Prediction:")
        st.write(category_prediction())


# ---------------- BUDGET ----------------
elif menu == "Budget Tracker":

    st.subheader("💵 Budget Tracker")

    expenses = load_expenses()

    if not expenses:
        st.warning("No expenses found")
    else:
        df = pd.DataFrame(expenses)

        budget = st.number_input("Enter Budget", value=10000.0)

        spent = df["amount"].sum()
        remaining = budget - spent

        st.write("Spent:", spent)
        st.write("Remaining:", remaining)

        progress = spent / budget if budget > 0 else 0
        st.progress(min(progress, 1.0))

        if spent > budget:
            st.error("Budget Exceeded")
        elif spent > budget * 0.8:
            st.warning("80% Budget Used")


# ---------------- GURU AI ----------------
elif menu == "Guru AI":

    st.subheader("📚 Guru AI")

    pdf = st.file_uploader("Upload Finance PDF", type=["pdf"])

    if pdf is not None:

        reader = PyPDF2.PdfReader(pdf)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        st.text_area("PDF Content", text[:5000], height=400)

        q = st.text_input("Ask Finance Question")

        if q:
            st.write("Suggested Insight:")
            st.write("Focus on saving, budgeting, debt control and investments.")


# ---------------- SPLITWISE ----------------
elif menu == "Splitwise":

    st.subheader("👥 Splitwise")

    total_bill = st.number_input("Total Bill", min_value=0.0)
    people = st.number_input("No of People", min_value=1, value=2)

    each = total_bill / people

    st.success(f"Each person pays ₹ {each:.2f}")