\f "0 SQL Basics\Total Sum of Orders";
\cs "1_1_fruit_stand.db";

select * from f_order;
\dp;

select * from f_price;
\dp;

SELECT fo.Item, fo."Order", fo.Qty, fp.Item, fp.Price, round(fo.Qty * fp.Price, 2) as Total_price
FROM f_order AS fo
LEFT JOIN f_price AS fp
ON fo.Item = fp.Item;
\pda tt = "Showing prices per order items:", tc = 51010, nc = 13,
nt = "SELECT fo.Item, fo."Order", fo.Qty, fp.Item, fp.Price, round(fo.Qty * fp.Price, 2) as Total_price
FROM f_order AS fo
LEFT JOIN f_price AS fp
ON fo.Item = fp.Item;";

SELECT DISTINCT "Order", round(sum(Total_price) over (PARTITION BY "Order" ORDER BY "Order"), 2) AS "Total $"
from (SELECT fo.Item, fo."Order", fo.Qty, fp.Item, fp.Price, fo.Qty * fp.Price as Total_price
FROM f_order AS fo
LEFT JOIN f_price AS fp
ON fo.Item = fp.Item);
\pda tt = "Showing prices per order:", tc = 51010, nc = 13,
nt = 'SELECT DISTINCT "Order", round(sum(Total_price) over (PARTITION BY "Order" ORDER BY "Order"), 2) AS "Total $"
from (SELECT fo.Item, fo."Order", fo.Qty, fp.Item, fp.Price, fo.Qty * fp.Price as Total_price
FROM f_order AS fo
LEFT JOIN f_price AS fp
ON fo.Item = fp.Item);';
