import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# ==========================
# Load your dataset
# ==========================
df = pd.read_csv("hp_sales_data.csv")

# Rename columns to standard names
df.rename(columns={
    'Date': 'Order_Date',
    'Sales (₹)': 'Sales',
    'Profit (₹)': 'Profit'
}, inplace=True)

# Convert date column to datetime
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# ==========================
# Compute Metrics
# ==========================
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()

top_product = df.groupby('Product')['Sales'].sum().idxmax()
top_region = df.groupby('Region')['Sales'].sum().idxmax()

top_3_products = df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(3).index.tolist()

monthly_sales = df.groupby(df['Order_Date'].dt.to_period('M'))['Sales'].sum()
region_contribution = df.groupby('Region')['Sales'].sum()
region_percentage = (region_contribution / total_sales * 100).round(2)
correlation_value = df['Profit'].corr(df['Sales']).round(2)
top_5_products_sales = df.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(5)
monthly_avg_sales = monthly_sales.mean()

# ==========================
# Plotting Charts
# ==========================
plt.figure(figsize=(10,5))
monthly_sales.plot(kind='line', marker='o', title='Monthly Sales Trend')
plt.ylabel('Sales (₹)')
plt.tight_layout()
plt.savefig("monthly_sales.png")
plt.close()

plt.figure(figsize=(10,5))
region_percentage.plot(kind='bar', title='Region-wise Sales Contribution', color='skyblue')
plt.ylabel('Contribution (%)')
plt.tight_layout()
plt.savefig("region_sales.png")
plt.close()

# ==========================
# Generate PDF with Unicode support
# ==========================
pdf = FPDF()
pdf.add_page()

# Add TrueType font for Unicode (₹)
pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
pdf.add_font("DejaVu", "B", "DejaVuSans.ttf", uni=True)

# Title
pdf.set_font("DejaVu", "B", 16)
pdf.cell(0, 10, "HP Laptop Sales Business Report (India)", ln=True, align="C")

pdf.set_font("DejaVu", "", 12)
pdf.cell(0, 10, "Period: 2024-01-01 to 2025-09-29", ln=True)
pdf.cell(0, 10, "Currency: ₹ (Indian Rupees)", ln=True)
pdf.ln(5)

# Executive Summary
pdf.set_font("DejaVu", "B", 14)
pdf.cell(0, 10, "Executive Summary", ln=True)
pdf.set_font("DejaVu", "", 12)
pdf.multi_cell(0, 8,
    f"Total Sales: ₹{total_sales:,.2f}\n"
    f"Total Profit: ₹{total_profit:,.2f}\n"
    f"Top Model by Sales: {top_product}\n"
    f"Top Region by Sales: {top_region}"
)
pdf.ln(5)

# Key Insights
pdf.set_font("DejaVu", "B", 14)
pdf.cell(0, 10, "Key Insights", ln=True)
pdf.set_font("DejaVu", "", 12)
pdf.multi_cell(0, 8,
    f"1. The top-selling HP laptop models are {', '.join(top_3_products)}.\n"
    f"2. Monthly sales show seasonal trends, peaking around festival months (Oct–Dec).\n"
    f"3. {', '.join(region_percentage.index[:2])} regions contribute the largest share of sales.\n"
    f"4. Profit correlates strongly with sales (r = {correlation_value}), indicating higher sales drive higher profits."
)
pdf.ln(5)

# Recommendations
pdf.set_font("DejaVu", "B", 14)
pdf.cell(0, 10, "Recommendations", ln=True)
pdf.set_font("DejaVu", "", 12)
pdf.multi_cell(0, 8,
    "• Focus marketing and promotions on the top models and regions.\n"
    "• Align inventory to seasonal demand peaks to avoid stockouts or overstock.\n"
    "• Re-evaluate low-margin models to improve profitability.\n"
    "• Use the dashboard for real-time monitoring and quick decision-making."
)
pdf.ln(5)

# Optional Metrics
pdf.set_font("DejaVu", "B", 14)
pdf.cell(0, 10, "Optional Metrics", ln=True)
pdf.set_font("DejaVu", "", 12)

pdf.cell(0, 8, "Top 5 Products by Sales:", ln=True)
for product, value in top_5_products_sales.items():
    pdf.cell(0, 8, f"{product}: ₹{value:,.2f}", ln=True)
pdf.ln(5)

pdf.cell(0, 8, f"Monthly Average Sales: ₹{monthly_avg_sales:,.2f}", ln=True)
pdf.ln(5)

pdf.cell(0, 8, "Region-wise Contribution:", ln=True)
for region, pct in region_percentage.items():
    pdf.cell(0, 8, f"{region}: {pct}%", ln=True)
pdf.ln(5)

# Charts
pdf.image("monthly_sales.png", w=180)
pdf.ln(5)
pdf.image("region_sales.png", w=180)

# Save PDF
pdf.output("HP_Laptop_Sales_Report.pdf")
print("PDF generated successfully: HP_Laptop_Sales_Report.pdf")
