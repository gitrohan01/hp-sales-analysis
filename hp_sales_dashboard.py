import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data(path="hp_sales_data.csv"):
    df = pd.read_csv(path)
    df.rename(columns={'Date':'Order Date', 'Sales (₹)':'Sales', 'Profit (₹)':'Profit'}, inplace=True)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['YearMonth'] = df['Order Date'].dt.to_period('M')
    return df

df = load_data()

st.title("HP Laptop Sales Dashboard (India)")

# Filters
product_filter = st.selectbox("Select Product", ["All"] + df['Product'].unique().tolist())
region_filter = st.selectbox("Select Region", ["All"] + df['Region'].unique().tolist())

data = df.copy()
if product_filter != "All":
    data = data[data['Product'] == product_filter]
if region_filter != "All":
    data = data[data['Region'] == region_filter]

# 1. Top Selling Products
st.subheader("Top 10 Selling Products")
top_products = data.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_products)

# 2. Monthly Sales Trend
st.subheader("Monthly Sales Trend")
monthly_sales = data.groupby('YearMonth')['Sales'].sum()
st.line_chart(monthly_sales)

# 3. Region-wise Sales
st.subheader("Sales by Region")
region_sales = data.groupby('Region')['Sales'].sum()
st.bar_chart(region_sales)

# 4. Profit vs Sales
st.subheader("Profit vs Sales Correlation")
fig, ax = plt.subplots(figsize=(8,6))
sns.scatterplot(data=data, x='Sales', y='Profit', hue='Region', alpha=0.7, ax=ax)
st.pyplot(fig)

# Display correlation
correlation = data['Sales'].corr(data['Profit'])
st.write(f"Correlation between Sales and Profit: {correlation:.2f}")
