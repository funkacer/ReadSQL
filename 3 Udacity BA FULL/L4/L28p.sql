\# !POSTGRE VERSION!, tc = 103001;

\# this should be answer;
select account_id, DATE_TRUNC('month', occurred_at) ord_date, sum(gloss_amt_usd) from orders where account_id = 1001 and DATE_TRUNC('month', occurred_at) = '2016-05-01' group by 1, 2;

SELECT DATE_TRUNC('month', o.occurred_at) ord_date, SUM(o.gloss_amt_usd) tot_spent
FROM orders o
JOIN accounts a
ON a.id = o.account_id
WHERE a.name = 'Walmart'
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;
