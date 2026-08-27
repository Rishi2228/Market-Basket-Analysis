# Market-Basket-Analysis
Project Overview

This project performs data cleaning and basic sales analysis on an
Online Retail dataset using Python. It removes invalid and cancelled
transactions, handles missing values, fixes data types, and creates
useful sales visualizations.

Objectives

Clean and prepare the retail dataset for analysis

Handle missing and duplicate data

Remove invalid quantities and prices

Identify and remove cancelled transactions

Calculate total sales

Analyze monthly sales, products, and countries

Visualize sales insights using Matplotlib

Technologies Used

Python

Pandas

Matplotlib

VS Code

Data Cleaning Steps

Load and inspect the dataset

Handle missing values

Remove duplicate rows

Remove zero/negative quantities

Remove zero/negative unit prices

Convert InvoiceDate to datetime

Remove cancelled transactions

Strip extra spaces from text columns

Clean column names

Fix data types

Remove empty rows

Perform final validation

A totalprice column is created using:

totalprice = quantity × unitprice

Visualizations

The project generates four charts:

Monthly Sales Trend -- shows sales performance over time.

Top 10 Products by Sales -- identifies the products generating
the highest sales.

Top 10 Countries by Sales -- compares sales across countries.

Quantity vs Unit Price -- shows the relationship between
quantity and unit price.

Project Structure

Online-Retail-Analysis/
│
├── retail_cleaning_analysis.py
├── OnlineRetail.csv
├── requirements.txt
├── README.md
│
└── output/
    ├── OnlineRetail_Cleaned.csv
    ├── 1_monthly_sales_trend.png
    ├── 2_top10_products.png
    ├── 3_sales_by_country.png
    └── 4_quantity_vs_unitprice.png

How to Run in VS Code

1. Add the Dataset

Place OnlineRetail.csv in the same folder as the Python script.

If your CSV has a different name, update the INPUT_FILE variable in
the Python file.

2. Install Required Libraries

Open the VS Code terminal and run:

pip install pandas matplotlib

Or, if a requirements.txt file is available:

pip install -r requirements.txt

3. Run the Project

Run:

python retail_cleaning_analysis.py

4. Check the Output

The cleaned dataset and four visualization PNG files will be created
inside the output folder.

Key Outcome

The project produces a clean retail dataset that can be used for further
business analysis and provides visual insights into sales trends,
top-performing products, country-wise sales, and pricing behavior.

Author

Rishi Shinde
