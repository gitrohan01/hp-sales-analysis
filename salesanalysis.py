import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("hp_sales_data.csv")


df.rename(columns={
    'Date':'Order Date',
    'Sales (₹)':'Sales',
    'Profit (₹)':'Profit'
}, inplace=True)


# Display first few rows to verify structure
print("Dataset preview:\n", df.head(), "\n")
print("Columns:", df.columns.tolist(), "\n")

# --- 1️⃣ Top Selling Product ---
top_products = df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(10)
print("Top Selling Products:\n", top_products, "\n")

plt.figure(figsize=(10,6))
sns.barplot(x=top_products.values, y=top_products.index, palette="viridis")
plt.title("Top Selling Products")
plt.xlabel("Total Sales")
plt.ylabel("Product")
plt.tight_layout()
plt.show()

# --- 2️⃣ Monthly Sales Trend ---
# Ensure Date column is in datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

# Group by month
monthly_sales = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum()

plt.figure(figsize=(12,6))
monthly_sales.plot(marker='o', color='teal')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.grid(True)
plt.tight_layout()
plt.show()

# --- 3️⃣ Region-wise Sales ---
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
print("Region-wise Sales:\n", region_sales, "\n")

plt.figure(figsize=(8,6))
sns.barplot(x=region_sales.values, y=region_sales.index, palette="coolwarm")
plt.title("Sales by Region")
plt.xlabel("Total Sales")
plt.ylabel("Region")
plt.tight_layout()
plt.show()

# --- 4️⃣ Profit vs Sales Correlation ---
plt.figure(figsize=(8,6))
sns.scatterplot(x='Sales', y='Profit', data=df, hue='Region', alpha=0.7)
plt.title("Profit vs Sales Correlation")
plt.xlabel("Sales")
plt.ylabel("Profit")
plt.legend(title='Region')
plt.tight_layout()
plt.show()

correlation = df['Sales'].corr(df['Profit'])
print(f"Correlation between Sales and Profit: {correlation:.2f}")
