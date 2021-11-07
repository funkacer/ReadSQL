---folder:Weather\;
---sqlite3:Weather.db;
--select *  from (condition) t1  left join (select *  from condition limit 5)  t2  ON t1.id != t2.id;

select * from sqlite_master where type = "table";
---pause:ask;

select * from condition_original;
---pause:ask;

select * from forecast_original;
---pause:ask;

with t1 as (select * from forecast_original order by date) select * from t1  group by date;
---pause:ask;

with t1 as (select * from (select * from forecast_original order by date) group by date) select text, count(*) from t1  group by text;
---pause:ask;
