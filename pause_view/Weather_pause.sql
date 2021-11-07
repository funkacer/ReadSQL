---folder:Weather\;
---sqlite3:Weather.db;
select *  from (condition) t1  left join (select *  from condition limit 5)  t2  ON t1.id != t2.id;
---pause:ask;
