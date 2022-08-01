\# !POSTGRE VERSION!, tc = 103001;

SELECT DATE_PART('dow', occurred_at) AS day_of_week, SUM(standard_qty)
FROM orders o
join accounts a
on o.account_id = a.id
where name = 'Walmart'
GROUP BY 1
ORDER BY 2 DESC;
