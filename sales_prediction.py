import pandas as pd

# Load dataset
df = pd.read_csv("hp_sales_data.csv")

# Rename columns
df.rename(columns={
    'Date':'Order_Date',
    'Sales (₹)':'Sales',
    'Profit (₹)':'Profit'
}, inplace=True)

# Convert Order_Date to datetime
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# Aggregate monthly sales
df_monthly = df.groupby(df['Order_Date'].dt.to_period('M'))['Sales'].sum().reset_index()
df_monthly['Order_Date'] = df_monthly['Order_Date'].dt.to_timestamp()

# Features: we'll use time as a number
df_monthly['Month_Number'] = range(len(df_monthly))
X = df_monthly[['Month_Number']]
y = df_monthly['Sales']


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Train model
lr = LinearRegression()
lr.fit(X_train, y_train)

# Predict
y_pred = lr.predict(X_test)

# Evaluate
mse = mean_squared_error(y_test, y_pred)
print(f"Linear Regression MSE: {mse:.2f}")

# Plot
plt.figure(figsize=(10,5))
plt.plot(df_monthly['Order_Date'], y, label='Actual Sales', marker='o')
plt.plot(df_monthly['Order_Date'].iloc[-len(y_test):], y_pred, label='Predicted Sales', marker='x')
plt.title("Linear Regression: Actual vs Predicted Sales")
plt.xlabel("Month")
plt.ylabel("Sales (₹)")
plt.legend()
plt.show()


from sklearn.ensemble import RandomForestRegressor

# Train model
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Predict
y_pred_rf = rf.predict(X_test)

# Evaluate
mse_rf = mean_squared_error(y_test, y_pred_rf)
print(f"Random Forest MSE: {mse_rf:.2f}")

# Plot
plt.figure(figsize=(10,5))
plt.plot(df_monthly['Order_Date'], y, label='Actual Sales', marker='o')
plt.plot(df_monthly['Order_Date'].iloc[-len(y_test):], y_pred_rf, label='Predicted Sales (RF)', marker='x')
plt.title("Random Forest: Actual vs Predicted Sales")
plt.xlabel("Month")
plt.ylabel("Sales (₹)")
plt.legend()
plt.show()


# Predict next 6 months
future_months = np.array(range(len(df_monthly), len(df_monthly)+6)).reshape(-1,1)
future_pred_lr = lr.predict(future_months)
future_pred_rf = rf.predict(future_months)

print("Next 6 months predicted sales (Linear Regression):", future_pred_lr)
print("Next 6 months predicted sales (Random Forest):", future_pred_rf)

