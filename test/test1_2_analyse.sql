\folder test;
\sqlite3 test.dbx;

select * from sqlite_master where type = "table";

select k, round(avg(b), 2) as bonita_mean, count(*) as count from test1 group by k order by 2 desc;

select * from test1 where V is NULL;

select d, count(*), round(avg(SP)), round(avg(SE)) from test1 group by d
union all
select "Total", count(*), round(avg(SP)), round(avg(SE)) from test1
;

select D, U, avg(SP) as SP, avg(SE) as SE, count(*) from test1 group by D, U
union all
select "Sum" as D, "Sum" as U, avg(SP) as SP, avg(SE) as SE, count(*) from test1
