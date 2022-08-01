\# !SQLITE VERSION!, tc = 103001;

SELECT strftime('%Y-%m-%d', occurred_at) AS date_of_order,
       SUM(total) AS total_qty
FROM orders
GROUP BY 1
ORDER BY 2 DESC;

SELECT strftime('%w', occurred_at) AS day_of_week,
       SUM(total) AS total_qty
FROM orders
GROUP BY 1
ORDER BY 2 DESC;

SELECT strftime('%Y-%m-%d', occurred_at) AS date_of_order,
       SUM(total) AS total_qty, MIN(strftime('%w', occurred_at)) AS day_of_week
FROM orders
GROUP BY 1
ORDER BY 2 DESC;
