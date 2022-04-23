\f archive;
\cs archive.dbx;

with t1 as (select date as d, count(*) as c from prices group by
 date order by 2 desc) select c, count(*) from t1 group by c order by 2 desc;

select strftime("%Y", date), count(*) from prices group by 1;
