SELECT account_id, a.name as Aname,
       SUM(total_amt_usd) AS sum_total_amt_usd
FROM orders o
JOIN accounts a
on o.account_id = a.id
GROUP BY 1, 2
HAVING SUM(total_amt_usd) >= 250000
order by SUM(total_amt_usd) DESC
limit 1;
