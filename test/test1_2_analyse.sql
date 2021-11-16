---folder:test;
---sqlite3:test.dbx;

select * from sqlite_master where type = "table";

select k, round(avg(b), 2) as bonita_mean, count(*) as count from test1 group by k order by 2 desc;

select * from test1 where V is NULL;
