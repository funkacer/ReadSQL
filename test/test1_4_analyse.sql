---folder:test;
---mysql:moje;

show tables;

select k, round(avg(b), 2) as bonita_mean, count(*) as count from test1 group by k order by 2 desc;

select * from test1 where V is NULL;
