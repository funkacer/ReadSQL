\folder Percentage;
\sqlite3 perc.db;
select code, count(*) as code_count,
       round(count(*) * 100.0/ sum(count(*)) over ()) as count_percent
       from moje1 group by code;
