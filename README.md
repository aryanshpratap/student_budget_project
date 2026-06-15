# Student Personal Finance & Budget Analysis

## Overview
This project analyzes 12 months (2025) of a student's personal income and
expenses to understand spending habits, track savings, and compare actual
spending against a monthly budget. It demonstrates a complete data analyst
workflow built around Excel, Python, and SQL - covering data cleaning,
formula-driven spreadsheet modeling, exploratory analysis, and a Tableau
dashboard.

## Dataset
A transaction-level dataset (443 records) covering:
- **Date, Type** (Income/Expense), **Category**, **Description**,
  **Amount (Rs.)**, **Payment Mode** (UPI/Cash/Card/Net Banking)

Income sources: Pocket Money (monthly allowance), Tutoring Income, Festival
Bonus, and occasional Refunds.
Expense categories: Food & Snacks, Transportation, Mobile & Internet,
Education, Entertainment, Subscriptions, Personal Care, Clothing, Savings
(transfers), and Miscellaneous.

The raw data included realistic data quality issues - duplicate entries,
inconsistent category casing, and trailing whitespace in payment modes -
which were identified and cleaned during analysis.

## Tools Used
- **Microsoft Excel** - budget model with live formulas (SUMIFS), conditional
  formatting, and an embedded chart dashboard
- **Python (Pandas, Seaborn, Matplotlib)** - data cleaning and exploratory analysis
- **SQL (SQLite)** - business-style queries on transaction data
- **Tableau** - interactive dashboard (see guide below)

## Data Cleaning Steps
1. Removed 8 exact duplicate transaction rows
2. Standardized inconsistent `Category` text casing (e.g., "food & snacks" → "Food & Snacks")
3. Trimmed trailing whitespace from `Payment_Mode` values
4. Converted `Date` to datetime and derived `Month` / `Month Name`

Result: a clean dataset of 443 unique, analysis-ready transactions.

## Key Insights

1. **Overall, the budget is sustainable but tight.** Annual income was
   Rs. 1,11,650 against expenses of Rs. 92,715, giving an average monthly
   savings rate of 15.7% - but two months (January and September) saw
   expenses exceed income.

2. **Three categories are significantly over budget.** Education (245% of
   budget), Clothing (236%), and Entertainment (194%) all exceeded their
   annual budget allocations - together accounting for most of the Rs. 9,915
   total budget overrun.

3. **Food & Snacks is the single largest expense category** (Rs. 24,009,
   ~26% of annual spending) across 156 transactions, but it's actually
   slightly *under* its annual budget (80% used) - the high total is driven
   by frequency, not overspending.

4. **UPI dominates payments**, accounting for 59% of all expense transactions
   and value - reflecting typical digital payment habits.

5. **September was the worst month financially** - a Rs. 1,139 deficit driven
   by high Food & Snacks and Entertainment spending, with no offsetting bonus
   income (unlike October's festival bonus).

6. **Savings transfers themselves were the largest average transaction**
   (Rs. 1,175 average), showing a consistent habit of setting money aside -
   though Savings still came in under its annual target (78% used).

## Visualizations
All charts are in the `charts/` folder:

| File | Description |
|------|-------------|
| `01_monthly_income_expense_savings.png` | Monthly income, expense, and net savings trend |
| `02_category_breakdown_pie.png` | Annual spending by category |
| `03_savings_rate_trend.png` | Monthly savings rate, with two negative months highlighted |
| `04_category_month_heatmap.png` | Spending intensity by category across months |
| `05_payment_mode_breakdown.png` | Total spending by payment mode |

## Excel Workbook
`Student_Budget_Analysis.xlsx` contains:
- **Dashboard** - KPI summary (Total Income, Expense, Net Savings, Avg
  Savings Rate) with embedded line, pie, and bar charts
- **Transactions** - cleaned transaction log with formula-derived Month columns
- **Budget** - editable monthly/annual budget assumptions per category (blue inputs)
- **Monthly Summary** - SUMIFS-driven monthly income, expense, savings, and savings rate
- **Budget vs Actual** - variance analysis with conditional formatting
  (green = under budget, yellow = near limit, red = over budget)

All totals and ratios are live formulas - changing any transaction or budget
assumption automatically recalculates the dashboard.

## SQL Analysis
The cleaned dataset is loaded into `student_budget.db` (SQLite, table
`transactions`). See `sql_queries.sql` for all queries, including monthly
income/expense/savings, top spending categories, average transaction size by
category, payment mode breakdown, months where expenses exceeded income, and
top 10 highest single expenses.

## Building the Tableau Dashboard
Use `data/personal_finance_cleaned.csv` as the data source. Suggested layout:

**KPI Cards (top row):** Total Income, Total Expense, Net Savings, Avg Savings Rate

**Visuals:**
- Line chart: Monthly Income vs. Expense vs. Net Savings
- Pie/Treemap: Spending by Category
- Bar chart: Budget vs. Actual by Category (requires joining/adding budget values)
- Heatmap: Category spending by month
- Bar chart: Spending by Payment Mode

**Filters:** Month, Category, Type, Payment Mode

**Steps:**
1. Open Tableau Public/Desktop and connect to `personal_finance_cleaned.csv`
2. Verify `Date` is a Date field and `Amount` is a Number (decimal)
3. Build the visuals above on a single dashboard
4. Add filters for Month, Category, and Payment Mode
5. Add KPI text/number cards using calculated fields (SUM(Amount) filtered by Type)
6. Apply a consistent color theme and publish/export

## How to Reproduce
```bash
python generate_finance_data.py     # generates data/personal_finance_transactions.csv
python eda_analysis.py               # cleans data, prints insights, saves charts
python build_excel_workbook.py       # builds Student_Budget_Analysis.xlsx
python sql_analysis.py               # loads SQLite DB and runs SQL queries
```

## Project Structure
```
student_budget_project/
├── data/
│   ├── personal_finance_transactions.csv   # raw dataset
│   └── personal_finance_cleaned.csv        # cleaned dataset
├── charts/                                   # generated visualizations
├── Student_Budget_Analysis.xlsx              # Excel dashboard & budget model
├── student_budget.db                         # SQLite database
├── generate_finance_data.py
├── eda_analysis.py
├── build_excel_workbook.py
├── sql_analysis.py
├── sql_queries.sql
└── README.md
```

## Project Dashboards & Visualizations
```
<img width="1920" height="1080" alt="Screenshot (53)" src="https://github.com/user-attachments/assets/5b7354db-1af5-4e2a-9f44-3c00ef375c26" />
<img width="1920" height="1080" alt="Screenshot (58)" src="https://github.com/user-attachments/assets/384d6e59-8d37-41e0-b57e-9e3d0f0e45f4" />
[👉 Click Here to View the Live Interactive Tableau Dashboard](https://public.tableau.com/views/StudentPersonalFinanceDashboard/StudentBudgetDashboard?:language=en-US&publish=yes&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
```
