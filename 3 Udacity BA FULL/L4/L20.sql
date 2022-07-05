SELECT DISTINCT a.id, a.name as Aname,
       sales_rep_id, s.name as Sname
FROM accounts a
join sales_reps s
on a.sales_rep_id = s.id
ORDER BY sales_rep_id;
