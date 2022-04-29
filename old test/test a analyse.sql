\folder test a;
\sqlite3 test a.db;

select * from sqlite_master where type = "table";

select code, round(avg(value), 2) as value_mean, count(*) as count from b group by code order by 2 desc;

select * from b where id is NULL;

select * from b;

select code, round(avg(value), 2) as value_mean, count(*) as count from b group by code
union all
select "Total", round(avg(value), 2) as value_mean, count(*) as count from b
;
