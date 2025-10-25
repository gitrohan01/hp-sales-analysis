-- 1. Top selling product
SELECT Product, SUM(Sales) AS total_sales
FROM hp_sales
GROUP BY Product
ORDER BY total_sales DESC
LIMIT 10;

-- 2. Monthly sales trend
SELECT DATE_TRUNC('month', "Order Date") AS month, SUM(Sales) AS total_sales
FROM hp_sales
GROUP BY month
ORDER BY month;

-- 3. Region-wise sales
SELECT Region, SUM(Sales) AS total_sales
FROM hp_sales
GROUP BY Region
ORDER BY total_sales DESC;

-- 4. Profit vs Sales correlation
SELECT CORR(Sales, Profit) AS profit_sales_correlation
FROM hp_sales;

-- 5. Top products by region
SELECT Region, Product, SUM(Sales) AS total_sales
FROM hp_sales
GROUP BY Region, Product
ORDER BY Region, total_sales DESC;
