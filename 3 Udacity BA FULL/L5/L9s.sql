\# !POSTGRE VERSION!, tc = 103001;

\# Code from video:;
WITH average_price as
( SELECT account_id, AVG(total_amt_usd) as brand_avg_price
  FROM orders
  GROUP BY 1
)
SELECT a.id, a.name, b.brand_avg_price
FROM accounts a
JOIN average_price b
ON b.account_id = a.id
ORDER BY b.brand_avg_price desc;
