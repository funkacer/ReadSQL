\f "2 Udacity BA";
\s "Udacity_3_19_fruit_stand.db";

drop table if exists f_order;
create table f_order (id integer primary key autoincrement, ordernr int, fruit text, qty int);

drop table if exists f_price;
create table f_price (id integer primary key autoincrement, fruit text, price int);

\r Udacity_3_19_fruit_stand3.csv, ";";
\dp;
\i f_order;

\r Udacity_3_19_fruit_stand2.csv, ";";
\dp;
\i f_price;

select * from f_order;
\dp;

select * from f_price;
\dp;

SELECT fo.fruit, fo.ordernr, fo.qty, fp.fruit, fp.price, round(fo.qty * fp.price, 2) as Total_price
FROM f_order AS fo
LEFT JOIN f_price AS fp
ON fo.fruit = fp.fruit;

SELECT DISTINCT ordernr, sum(round(Total_price)) over (PARTITION BY ordernr ORDER BY ordernr) from (
SELECT fo.fruit, fo.ordernr, fo.qty, fp.fruit, fp.price, round(fo.qty * fp.price) as Total_price
FROM f_order AS fo
LEFT JOIN f_price AS fp
ON fo.fruit = fp.fruit);

\pd 100;
