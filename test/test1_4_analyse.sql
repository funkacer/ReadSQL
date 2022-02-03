\folder test;
\c my test;

show tables;

select * from test1;

select k, round(avg(b), 2) as bonita_mean, count(*) as count from test1 group by k order by 2 desc;

select * from test1 where V is NULL;
