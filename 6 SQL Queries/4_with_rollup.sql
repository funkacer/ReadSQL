---folder:6 SQL Queries;
---sqlite3:data.db;

-- Only in MYSQL:
SELECT
	  month,
	  id,
	  SUM (Amount) AS total_amount
	FROM bill
	GROUP BY month,id WITH ROLLUP
;

-- In SQLite3:
select month,Amount,Total from (
select 1 id,type, '#' || COALESCE (type,'') as month ,'' Amount ,'' as Total from bill
group by type  --Title
union
select 2 id,type, month,Amount,'' from bill --Items
union
select 3 id,type, type || '- Subtotal :' as month ,'',Sum(Amount) as Total from bill
group by type --SubTotal
union
select 99 id,'_' type, 'Grand Total :' as month ,'', sum(Amount) as Total from bill
group by 1,2,3 --GrandTotal
)
;
