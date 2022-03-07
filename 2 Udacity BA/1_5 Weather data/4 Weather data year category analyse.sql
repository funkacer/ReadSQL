\f 2 Udacity BA\1_5 Weather data;
\cs Weather data.db;

select * from  a1 limit 10;

select round(avg(avg_temp),2), city, country, year_cat from city_data as t1
 join year_cat as t2
 on t1.year=t2.year group by city, country, year_cat
 having city = "Alexandria";
\pda;

with t1 as
(select round(avg(avg_temp),2) as avg_temp, city, country, year_cat, 1 as counter from city_data as t1
 join year_cat as t2
 on t1.year=t2.year group by city, country, year_cat
 having city = "Prague"
 order by 1 ASC)
select * from (select city, country, min(row) as minn, max(row) as maxx from (select city, country, year_cat, avg_temp, row_number() OVER(PARTITION BY city, country) as row from t1)
group by city, country) as t2
join (select city, country, year_cat, avg_temp, row_number() OVER(PARTITION BY city, country) as row from t1) as t3
on t2.minn = t3.row and t2.city = t3.city and t2.country = t3.country or t2.maxx = t3.row and t2.city = t3.city and t2.country = t3.country;

with t1 as
(select round(avg(avg_temp),2) as avg_temp, city, country, year_cat, 1 as counter from city_data as t1
 join year_cat as t2
 on t1.year=t2.year group by city, country, year_cat
 having city = "Alexandria"
)
select city, country, year_cat, avg_temp, sum(counter) OVER(PARTITION BY city, country ORDER BY avg_temp) as row from t1;

create table temp.a1 as
with t1 as
(select round(avg(avg_temp),2) as avg_temp, city, country, year_cat, 1 as counter from city_data as t1
 join year_cat as t2
 on t1.year=t2.year group by city, country, year_cat
 --having city = "Prague"
 having avg_temp is not Null
)
select t3.city, t3.country, t3.year_cat, t3.avg_temp, t3.row from (select city, country, min(row) as minn, max(row) as maxx from (select city, country, year_cat, avg_temp, sum(counter) OVER(PARTITION BY city, country ORDER BY avg_temp) as row from t1)
group by city, country) as t2
join (select city, country, year_cat, avg_temp, sum(counter) OVER(PARTITION BY city, country ORDER BY avg_temp, year_cat) as row from t1) as t3
on t2.minn = t3.row and t2.city = t3.city and t2.country = t3.country or t2.maxx = t3.row and t2.city = t3.city and t2.country = t3.country
--limit 100;

select * from  a1;
\pda;
