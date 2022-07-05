\# !POSTGRE VERSION!, tc = 103001;

SELECT DATE_TRUNC('day',occurred_at) AS day_of_week,
       SUM(total) AS total_qty
FROM orders
GROUP BY 1
ORDER BY 2 DESC;

SELECT DATE_PART('dow',occurred_at) AS day_of_week,
       SUM(total) AS total_qty
FROM orders
GROUP BY 1
ORDER BY 2 DESC;

SELECT DATE_TRUNC('day',occurred_at) AS day_of_week,
       SUM(total) AS total_qty, MIN(DATE_PART('dow',occurred_at)) AS day_of_week
FROM orders
GROUP BY 1
ORDER BY 2 DESC;
