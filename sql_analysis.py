"""
Student Budget Analysis - SQL Layer
Loads the cleaned transaction data into SQLite and runs queries.
"""

import sqlite3
import pandas as pd

CLEAN_PATH = "data/cleaned_finance_transactions.csv"
DB_PATH = "student_budget.db"

df = pd.read_csv(CLEAN_PATH)
conn = sqlite3.connect(DB_PATH)
df.to_sql("transactions", conn, if_exists="replace", index=False)
print(f"Loaded {len(df)} rows into 'transactions' table in {DB_PATH}")

queries = {
    "1. Monthly Income, Expense, and Net Savings": """
        SELECT Month_Name AS Month,
               ROUND(SUM(CASE WHEN Type='Income' THEN Amount ELSE 0 END), 2) AS Income,
               ROUND(SUM(CASE WHEN Type='Expense' THEN Amount ELSE 0 END), 2) AS Expense,
               ROUND(SUM(CASE WHEN Type='Income' THEN Amount ELSE -Amount END), 2) AS Net_Savings
        FROM transactions
        GROUP BY Month
        ORDER BY Month;
    """,

    "2. Category-wise Annual Spending (Top 5)": """
        SELECT Category,
               ROUND(SUM(Amount), 2) AS Total_Spent,
               COUNT(*) AS Transaction_Count
        FROM transactions
        WHERE Type = 'Expense'
        GROUP BY Category
        ORDER BY Total_Spent DESC
        LIMIT 5;
    """,

    "3. Average Transaction Amount by Category": """
        SELECT Category,
               ROUND(AVG(Amount), 2) AS Avg_Amount,
               COUNT(*) AS Transaction_Count
        FROM transactions
        WHERE Type = 'Expense'
        GROUP BY Category
        ORDER BY Avg_Amount DESC;
    """,

    "4. Spending by Payment Mode": """
        SELECT Payment_Mode,
               ROUND(SUM(Amount), 2) AS Total_Amount,
               COUNT(*) AS Transaction_Count,
               ROUND(SUM(Amount) * 100.0 / (SELECT SUM(Amount) FROM transactions WHERE Type='Expense'), 2) AS Pct_of_Total
        FROM transactions
        WHERE Type = 'Expense'
        GROUP BY Payment_Mode
        ORDER BY Total_Amount DESC;
    """,

    "5. Months Where Expenses Exceeded Income": """
        SELECT Month_Name AS Month,
               ROUND(SUM(CASE WHEN Type='Income' THEN Amount ELSE 0 END), 2) AS Income,
               ROUND(SUM(CASE WHEN Type='Expense' THEN Amount ELSE 0 END), 2) AS Expense
        FROM transactions
        GROUP BY Month
        HAVING Expense > Income
        ORDER BY Month;
    """,

    "6. Top 10 Highest Single Expenses": """
        SELECT Date, Category, Description, Amount, Payment_Mode
        FROM transactions
        WHERE Type = 'Expense'
        ORDER BY Amount DESC
        LIMIT 10;
    """,

    "7. Total Income by Source": """
        SELECT Category AS Income_Source,
               ROUND(SUM(Amount), 2) AS Total_Amount,
               COUNT(*) AS Transaction_Count
        FROM transactions
        WHERE Type = 'Income'
        GROUP BY Category
        ORDER BY Total_Amount DESC;
    """,
}

print("\n" + "=" * 70)
for title, query in queries.items():
    print(f"\n{title}")
    print("-" * 70)
    result = pd.read_sql_query(query, conn)
    print(result.to_string(index=False))

conn.close()
print("\nDone.")
