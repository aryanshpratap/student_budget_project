"""
Generate a synthetic personal finance dataset for a student (12 months, 2025)
for the Student Budget Analysis project. Includes minor realistic data
quality issues (duplicates, inconsistent category casing, refunds).
"""

import numpy as np
import pandas as pd
from datetime import date, timedelta
import calendar

np.random.seed(7)

months = list(range(1, 13))
year = 2025

# Expense categories with (per-transaction min, max, transactions-per-month range)
expense_categories = {
    "Food & Snacks": (50, 250, (10, 15)),
    "Transportation": (20, 100, (8, 12)),
    "Mobile & Internet": (250, 320, (1, 1)),
    "Education": (50, 800, (1, 3)),
    "Entertainment": (100, 600, (2, 5)),
    "Subscriptions": (149, 399, (1, 1)),
    "Personal Care": (50, 300, (1, 3)),
    "Clothing": (300, 1500, (0, 2)),
    "Savings": (500, 2000, (1, 1)),
    "Miscellaneous": (50, 400, (0, 2)),
}

food_descriptions = ["Mess Bill", "Tiffin", "Canteen", "Tea/Snacks", "Restaurant", "Grocery"]
transport_descriptions = ["Bus Fare", "Auto/Rickshaw", "Metro Card Recharge", "Cab Ride", "Fuel"]
education_descriptions = ["Stationery", "Printouts/Xerox", "Reference Book", "Online Course Fee", "Lab Manual"]
entertainment_descriptions = ["Movie Ticket", "OTT Rental", "Outing with Friends", "Gaming", "Event Ticket"]
personal_care_descriptions = ["Haircut", "Toiletries", "Skincare"]
clothing_descriptions = ["T-Shirt/Shirt", "Footwear", "Festive Shopping", "Winter Wear"]
misc_descriptions = ["Gift", "Donation", "Repairs", "Stationery Shop", "Other"]

payment_modes = ["UPI", "Cash", "Card", "Net Banking"]
payment_weights = [0.55, 0.20, 0.15, 0.10]

rows = []

for month in months:
    days_in_month = calendar.monthrange(year, month)[1]

    # ---- Income ----
    rows.append([date(year, month, 1).isoformat(), "Income", "Pocket Money",
                  "Monthly Allowance from Parents", 8000, "Net Banking"])

    # Tutoring income in ~5 random months
    if month in [2, 4, 6, 8, 11]:
        amt = int(np.random.randint(1000, 3000))
        rows.append([date(year, month, np.random.randint(5, 25)).isoformat(),
                      "Income", "Tutoring Income", "Tuition for Junior Student", amt, "UPI"])

    # Festive bonus in October (Diwali)
    if month == 10:
        amt = int(np.random.randint(3000, 5000))
        rows.append([date(year, month, 15).isoformat(),
                      "Income", "Festival Bonus", "Diwali Gift from Family", amt, "Cash"])

    # ---- Expenses ----
    for category, (lo, hi, (n_min, n_max)) in expense_categories.items():
        n_tx = np.random.randint(n_min, n_max + 1)

        # Seasonal adjustments
        if category == "Education" and month in [1, 7]:
            n_tx += 1  # semester start
        if category in ["Clothing", "Entertainment"] and month in [10, 11]:
            n_tx += 1  # festive season

        for _ in range(n_tx):
            day = np.random.randint(1, days_in_month + 1)
            amount = round(np.random.uniform(lo, hi), 2)

            if category == "Food & Snacks":
                desc = np.random.choice(food_descriptions)
            elif category == "Transportation":
                desc = np.random.choice(transport_descriptions)
            elif category == "Mobile & Internet":
                desc = "Monthly Recharge"
            elif category == "Education":
                desc = np.random.choice(education_descriptions)
            elif category == "Entertainment":
                desc = np.random.choice(entertainment_descriptions)
            elif category == "Subscriptions":
                desc = np.random.choice(["Netflix/OTT Share", "Spotify Premium"])
            elif category == "Personal Care":
                desc = np.random.choice(personal_care_descriptions)
            elif category == "Clothing":
                desc = np.random.choice(clothing_descriptions)
            elif category == "Savings":
                desc = "Transfer to Savings Account"
            else:
                desc = np.random.choice(misc_descriptions)

            payment = np.random.choice(payment_modes, p=payment_weights)
            rows.append([date(year, month, day).isoformat(), "Expense", category, desc, amount, payment])

    # Occasional refund (income) - 2 months
    if month in [5, 9]:
        amt = round(np.random.uniform(100, 400), 2)
        rows.append([date(year, month, np.random.randint(1, days_in_month + 1)).isoformat(),
                      "Income", "Refund", "Refund for Returned Item", amt, "UPI"])

df = pd.DataFrame(rows, columns=["Date", "Type", "Category", "Description", "Amount", "Payment_Mode"])
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

# ---------------- Inject realistic data quality issues ----------------

# 1. Inconsistent category casing for ~3% of expense rows
mask = df["Type"] == "Expense"
inconsistent_idx = df[mask].sample(frac=0.03, random_state=1).index
df.loc[inconsistent_idx, "Category"] = df.loc[inconsistent_idx, "Category"].str.lower()

# 2. Duplicate rows (~8 duplicates)
dupes = df.sample(n=8, random_state=2)
df = pd.concat([df, dupes], ignore_index=True)

# 3. Trailing whitespace in a few Payment_Mode values
ws_idx = df.sample(n=10, random_state=3).index
df.loc[ws_idx, "Payment_Mode"] = df.loc[ws_idx, "Payment_Mode"] + "  "

df = df.sample(frac=1, random_state=4).reset_index(drop=True)
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

df.to_csv("data/personal_finance_transactions.csv", index=False)
print(f"Generated {len(df)} transactions (including {len(dupes)} intentional duplicates)")
print(df.head(10))
