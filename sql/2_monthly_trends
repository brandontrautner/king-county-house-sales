CREATE VIEW v_monthly_trends
AS
SELECT DATE_TRUNC('month', sale_date)::DATE AS month
	,COUNT(*) AS total_sales
	,ROUND(AVG(price)::NUMERIC, 2) AS avg_price
	,ROUND(MIN(price)::NUMERIC, 2) AS min_price
	,ROUND(MAX(price)::NUMERIC, 2) AS max_price
	,price_segment
	,waterfront_status
FROM v_house_sales_clean
GROUP BY DATE_TRUNC('month', sale_date)::DATE
	,price_segment
	,waterfront_status
ORDER BY month;
