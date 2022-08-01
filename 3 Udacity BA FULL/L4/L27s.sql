\# !SQLITE VERSION!, tc = 103001;

\# this should be total;
select account_id, sum(standard_qty) from orders where account_id = 1001 group by 1;

SELECT strftime('%w', occurred_at) AS day_of_week, SUM(standard_qty) as standard_qty_sum
FROM orders o
join accounts a
on o.account_id = a.id
where name = 'Walmart'
GROUP BY 1
ORDER BY 2 DESC;

with a as (SELECT strftime('%w', occurred_at) AS day_of_week, SUM(standard_qty) as standard_qty_sum
FROM orders o
join accounts a
on o.account_id = a.id
where name = 'Walmart'
GROUP BY 1
ORDER BY 2 DESC)
select 'Total', sum(standard_qty_sum) as standard_qty_sum from a group by 1;

SELECT strftime('%w', occurred_at) AS day_of_week, SUM(standard_qty) as standard_qty_sum,
SUM(SUM(standard_qty)) OVER(ORDER BY SUM(standard_qty) DESC) as running_total
FROM orders o
join accounts a
on o.account_id = a.id
where name = 'Walmart'
GROUP BY 1
ORDER BY 2 DESC;

SELECT strftime('%w', occurred_at) AS day_of_week, SUM(standard_qty) as standard_qty_sum,
SUM(SUM(standard_qty)) OVER() as running_total
FROM orders o
join accounts a
on o.account_id = a.id
where name = 'Walmart'
GROUP BY 1
ORDER BY 2 DESC;
