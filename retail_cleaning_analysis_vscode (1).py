"""
Online Retail Dataset - Data Cleaning & Sales Analysis
========================================================
VS Code / local machine version.

Steps:
 1. Load & inspect dataset
 2. Handle missing values
 3. Remove duplicate rows
 4. Remove zero/negative Quantity
 5. Remove zero/negative UnitPrice
 6. Convert InvoiceDate to proper datetime
 7. Identify & remove cancelled transactions
 8. Strip extra spaces from text columns
 9. Clean column names
10. Fix data types
11. Remove empty rows
12. Final validation
13. Visualizations: Monthly Sales Trend, Top 10 Products, Sales by Country, Quantity vs UnitPrice

HOW TO RUN (VS Code):
1. Put your CSV file (e.g. OnlineRetail.csv) in the same folder as this script,
   OR update the INPUT_FILE path below to point to your file.
2. Open a terminal in VS Code (Terminal > New Terminal).
3. Install requirements:  pip install -r requirements.txt
4. Run:  python retail_cleaning_analysis.py
5. Cleaned CSV + 4 chart PNGs will be saved in the "output" folder.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------------------------
# CONFIG - change these paths as needed
# -----------------------------------------------------------------
INPUT_FILE = "OnlineRetail.csv"      # <-- put your CSV filename here
OUTPUT_DIR = "output"                 # folder where results are saved

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------------------------------
# 1. LOAD & INSPECT DATASET
# -----------------------------------------------------------------
df = pd.read_csv(INPUT_FILE, encoding="ISO-8859-1")

print("=" * 60)
print("STEP 1: INITIAL INSPECTION")
print("=" * 60)
print(f"Shape (rows, cols): {df.shape}")
print("\nColumn info:")
print(df.info())
print("\nFirst 5 rows:")
print(df.head())

# -----------------------------------------------------------------
# 9. CLEAN COLUMN NAMES (done early so all later steps use clean names)
# -----------------------------------------------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.replace(" ", "_")
    .str.lower()
)
print("\nCleaned column names:", list(df.columns))

# -----------------------------------------------------------------
# 11. REMOVE FULLY EMPTY ROWS
# -----------------------------------------------------------------
before = len(df)
df.dropna(how="all", inplace=True)
print(f"\nSTEP: Removed fully empty rows -> {before - len(df)} rows dropped")

# -----------------------------------------------------------------
# 8. STRIP EXTRA SPACES FROM TEXT COLUMNS
# -----------------------------------------------------------------
text_cols = ["invoiceno", "stockcode", "description", "country"]
for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# -----------------------------------------------------------------
# 2. HANDLE MISSING VALUES
# -----------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 2: MISSING VALUES")
print("=" * 60)
print(df.isnull().sum())

# Description missing -> drop those rows (can't analyze product without name)
before = len(df)
df.dropna(subset=["description"], inplace=True)
print(f"Dropped rows with missing description: {before - len(df)}")

# CustomerID missing -> keep row but mark as 'Unknown' (many retail rows lack CustomerID
# but still represent valid sales; dropping them would lose ~25% of sales data)
df["customerid"] = df["customerid"].fillna(-1).astype(int).astype(str)
df.loc[df["customerid"] == "-1", "customerid"] = "Unknown"

# -----------------------------------------------------------------
# 3. REMOVE DUPLICATE ROWS
# -----------------------------------------------------------------
before = len(df)
df.drop_duplicates(inplace=True)
print(f"\nSTEP 3: Removed duplicate rows -> {before - len(df)} rows dropped")

# -----------------------------------------------------------------
# 7. IDENTIFY & REMOVE CANCELLED TRANSACTIONS
#    (Cancelled invoices in this dataset start with 'C')
# -----------------------------------------------------------------
before = len(df)
cancelled_mask = df["invoiceno"].astype(str).str.startswith("C")
print(f"\nSTEP 7: Cancelled transactions found -> {cancelled_mask.sum()}")
df = df[~cancelled_mask]
print(f"Rows dropped (cancelled): {before - len(df)}")

# -----------------------------------------------------------------
# 4. REMOVE ZERO/NEGATIVE QUANTITY
# -----------------------------------------------------------------
before = len(df)
df = df[df["quantity"] > 0]
print(f"\nSTEP 4: Removed zero/negative Quantity -> {before - len(df)} rows dropped")

# -----------------------------------------------------------------
# 5. REMOVE ZERO/NEGATIVE UNITPRICE
# -----------------------------------------------------------------
before = len(df)
df = df[df["unitprice"] > 0]
print(f"STEP 5: Removed zero/negative UnitPrice -> {before - len(df)} rows dropped")

# -----------------------------------------------------------------
# 6. CONVERT INVOICEDATE TO PROPER DATETIME
# -----------------------------------------------------------------
df["invoicedate"] = pd.to_datetime(df["invoicedate"], format="%m/%d/%Y %H:%M", errors="coerce")
before = len(df)
df.dropna(subset=["invoicedate"], inplace=True)
print(f"STEP 6: Converted InvoiceDate to datetime -> {before - len(df)} unparseable rows dropped")

# -----------------------------------------------------------------
# 10. FIX DATA TYPES
# -----------------------------------------------------------------
df["invoiceno"] = df["invoiceno"].astype(str)
df["stockcode"] = df["stockcode"].astype(str)
df["description"] = df["description"].astype(str)
df["quantity"] = df["quantity"].astype(int)
df["unitprice"] = df["unitprice"].astype(float)
df["country"] = df["country"].astype(str)

# Add derived column: total sales per line item
df["totalprice"] = df["quantity"] * df["unitprice"]

# -----------------------------------------------------------------
# 12. FINAL VALIDATION
# -----------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 12: FINAL VALIDATION")
print("=" * 60)
print(f"Final shape: {df.shape}")
print("\nData types:")
print(df.dtypes)
print("\nRemaining missing values:")
print(df.isnull().sum())
print(f"\nDuplicate rows remaining: {df.duplicated().sum()}")
print(f"Min Quantity: {df['quantity'].min()}, Min UnitPrice: {df['unitprice'].min()}")
print(f"Any cancelled (invoiceno starts with C) remaining: {df['invoiceno'].str.startswith('C').sum()}")
print(f"Date range: {df['invoicedate'].min()} to {df['invoicedate'].max()}")

# Save cleaned dataset
cleaned_path = os.path.join(OUTPUT_DIR, "OnlineRetail_Cleaned.csv")
df.to_csv(cleaned_path, index=False)
print(f"\nCleaned data saved to: {cleaned_path}")

# ===================================================================
# VISUALIZATIONS
# ===================================================================
plt.style.use("seaborn-v0_8-darkgrid")

# -------------------------------------------------------------
# 1. Monthly Sales Trend -> Line Chart
# -------------------------------------------------------------
df["invoice_month"] = df["invoicedate"].dt.to_period("M").astype(str)
monthly_sales = df.groupby("invoice_month")["totalprice"].sum().sort_index()

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o", color="#2E86AB", linewidth=2)
plt.title("Monthly Sales Trend", fontsize=14, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Total Sales (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "1_monthly_sales_trend.png"), dpi=150)
plt.close()

# -------------------------------------------------------------
# 2. Top 10 Products by Sales -> Bar Chart
# -------------------------------------------------------------
top_products = (
    df.groupby("description")["totalprice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))
plt.barh(top_products.index[::-1], top_products.values[::-1], color="#F18F01")
plt.title("Top 10 Products by Sales", fontsize=14, fontweight="bold")
plt.xlabel("Total Sales (£)")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "2_top10_products.png"), dpi=150)
plt.close()

# -------------------------------------------------------------
# 3. Sales by Country -> Bar Chart
# -------------------------------------------------------------
country_sales = df.groupby("country")["totalprice"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 6))
plt.bar(country_sales.index, country_sales.values, color="#A23B72")
plt.title("Top 10 Countries by Sales", fontsize=14, fontweight="bold")
plt.xlabel("Country")
plt.ylabel("Total Sales (£)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "3_sales_by_country.png"), dpi=150)
plt.close()

# -------------------------------------------------------------
# 4. Quantity vs Unit Price -> Scatter Chart
# -------------------------------------------------------------
sample = df.sample(n=min(5000, len(df)), random_state=42)  # sample for readability

plt.figure(figsize=(10, 6))
plt.scatter(sample["quantity"], sample["unitprice"], alpha=0.4, color="#3B7A57", s=15)
plt.title("Quantity vs Unit Price", fontsize=14, fontweight="bold")
plt.xlabel("Quantity")
plt.ylabel("Unit Price (£)")
plt.xscale("log")
plt.yscale("log")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "4_quantity_vs_unitprice.png"), dpi=150)
plt.close()

print(f"\nAll charts saved to {OUTPUT_DIR}/")
print("Done!")
