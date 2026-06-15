"""
Student Budget Analysis - Exploratory Data Analysis
Cleans the transaction data, computes monthly/category summaries,
and generates visualizations.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

RAW_PATH = "data/personal_finance_transactions.csv"
CLEAN_PATH = "data/cleaned_finance_transactions.csv"
CHART_DIR = "charts"

# ============================================================
# 1. LOAD & CLEAN
# ============================================================
df = pd.read_csv(RAW_PATH)
print(f"Raw shape: {df.shape}")
print(f"Duplicate rows: {df.duplicated().sum()}")

before = len(df)
df = df.drop_duplicates().reset_index(drop=True)
print(f"Removed {before - len(df)} duplicate rows")

df["Category"] = df["Category"].str.strip().str.title()
df["Payment_Mode"] = df["Payment_Mode"].str.strip()
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%b")

print(f"Cleaned shape: {df.shape}")
df.to_csv(CLEAN_PATH, index=False)

# ============================================================
# 2. MONTHLY INCOME / EXPENSE / SAVINGS
# ============================================================
monthly = df.groupby(["Month", "Month_Name", "Type"])["Amount"].sum().unstack(fill_value=0).reset_index()
monthly = monthly.sort_values("Month")
monthly["Net_Savings"] = monthly["Income"] - monthly["Expense"]
monthly["Savings_Rate_%"] = (monthly["Net_Savings"] / monthly["Income"] * 100).round(2)

print("\n" + "=" * 60)
print("MONTHLY INCOME, EXPENSE, SAVINGS")
print("=" * 60)
print(monthly[["Month_Name", "Income", "Expense", "Net_Savings", "Savings_Rate_%"]].to_string(index=False))

avg_income = monthly["Income"].mean()
avg_expense = monthly["Expense"].mean()
avg_savings_rate = monthly["Savings_Rate_%"].mean()

print(f"\nAverage Monthly Income:  Rs. {avg_income:,.2f}")
print(f"Average Monthly Expense: Rs. {avg_expense:,.2f}")
print(f"Average Savings Rate:    {avg_savings_rate:.2f}%")

# ============================================================
# 3. CATEGORY-WISE SPENDING
# ============================================================
expenses = df[df["Type"] == "Expense"]
category_totals = expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False).reset_index()
category_totals["Pct_of_Total"] = (category_totals["Amount"] / category_totals["Amount"].sum() * 100).round(2)

print("\n" + "=" * 60)
print("CATEGORY-WISE SPENDING (Annual)")
print("=" * 60)
print(category_totals.to_string(index=False))

# ============================================================
# 4. PAYMENT MODE BREAKDOWN
# ============================================================
payment_summary = expenses.groupby("Payment_Mode")["Amount"].agg(["sum", "count"]).reset_index()
payment_summary.columns = ["Payment_Mode", "Total_Amount", "Transaction_Count"]
payment_summary = payment_summary.sort_values("Total_Amount", ascending=False)

print("\n" + "=" * 60)
print("SPENDING BY PAYMENT MODE")
print("=" * 60)
print(payment_summary.to_string(index=False))

# ============================================================
# VISUALIZATIONS
# ============================================================

# 1. Monthly Income vs Expense vs Savings
plt.figure(figsize=(10, 5))
plt.plot(monthly["Month_Name"], monthly["Income"], marker="o", label="Income", color="#2a9d8f")
plt.plot(monthly["Month_Name"], monthly["Expense"], marker="o", label="Expense", color="#e76f51")
plt.plot(monthly["Month_Name"], monthly["Net_Savings"], marker="o", label="Net Savings", color="#264653")
plt.title("Monthly Income, Expense & Net Savings (2025)")
plt.ylabel("Amount (Rs.)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/01_monthly_income_expense_savings.png", dpi=120)
plt.close()

# 2. Category-wise spending breakdown (pie chart)
plt.figure(figsize=(7, 7))
plt.pie(category_totals["Amount"], labels=category_totals["Category"], autopct="%1.1f%%",
        colors=sns.color_palette("Set3", len(category_totals)))
plt.title("Annual Spending by Category")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/02_category_breakdown_pie.png", dpi=120)
plt.close()

# 3. Savings rate trend
plt.figure(figsize=(10, 5))
colors = ["#2a9d8f" if x >= 0 else "#e76f51" for x in monthly["Savings_Rate_%"]]
sns.barplot(data=monthly, x="Month_Name", y="Savings_Rate_%", hue="Month_Name", palette=colors, legend=False)
plt.axhline(avg_savings_rate, color="black", linestyle="--", linewidth=1, label=f"Avg: {avg_savings_rate:.1f}%")
plt.title("Monthly Savings Rate (%)")
plt.ylabel("Savings Rate (%)")
plt.legend()
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/03_savings_rate_trend.png", dpi=120)
plt.close()

# 4. Category spending over months (heatmap)
pivot = expenses.pivot_table(values="Amount", index="Category", columns="Month_Name", aggfunc="sum", fill_value=0)
month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
pivot = pivot[[m for m in month_order if m in pivot.columns]]
plt.figure(figsize=(11, 6))
sns.heatmap(pivot, cmap="YlOrRd", annot=False, cbar_kws={"label": "Amount (Rs.)"})
plt.title("Spending by Category Across Months")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/04_category_month_heatmap.png", dpi=120)
plt.close()

# 5. Payment mode breakdown
plt.figure(figsize=(7, 5))
sns.barplot(data=payment_summary, x="Payment_Mode", y="Total_Amount", hue="Payment_Mode", palette="crest", legend=False)
plt.title("Total Spending by Payment Mode")
plt.ylabel("Total Amount (Rs.)")
plt.xlabel("")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/05_payment_mode_breakdown.png", dpi=120)
plt.close()

print("\nAll charts saved to:", CHART_DIR)
print("Done.")
