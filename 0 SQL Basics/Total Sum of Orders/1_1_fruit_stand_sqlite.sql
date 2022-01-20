\f "0 SQL Basics\Total Sum of Orders";
\s "1_1_fruit_stand.db";

drop table if exists f_order;
create table f_order (id integer primary key autoincrement, "Order" int, Item text, Qty int);

drop table if exists f_price;
create table f_price (id integer primary key autoincrement, Item text, Price int);

\r 1_1_fruit_stand_orders.csv, ";";
\dp;
\i f_order;

\r 1_1_fruit_stand_prices.csv, ";";
\dp;
\i f_price;

select * from f_order;
\dp;

select * from f_price;
\dp;

SELECT fo.Item, fo."Order", fo.Qty, fp.Item, fp.Price, round(fo.Qty * fp.Price, 2) as Total_price
FROM f_order AS fo
LEFT JOIN f_price AS fp
ON fo.Item = fp.Item;
\pd 100;

SELECT DISTINCT "Order", round(sum(Total_price) over (PARTITION BY "Order" ORDER BY "Order"), 2) AS "Total $"
from (SELECT fo.Item, fo."Order", fo.Qty, fp.Item, fp.Price, fo.Qty * fp.Price as Total_price
FROM f_order AS fo
LEFT JOIN f_price AS fp
ON fo.Item = fp.Item);

select a from b;
\dp;
