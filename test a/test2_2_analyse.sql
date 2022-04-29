\folder test;
\s test.dbx;

select id_p, Count(*) from test2 group by id_p order by 2 DESC;
