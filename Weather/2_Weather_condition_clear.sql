---folder:Weather;
---sqlite3:Weather.db;
-- copy to new tables:
DROP TABLE IF EXISTS condition;
CREATE TABLE condition AS SELECT * FROM condition_original;
-- smazat tri zaznamy s _id = 1 !!!
select * from condition where pubdate = '2020-01-18 19:00:00' and creatat = '2020-01-18 20:23:40';
select count(*) from condition;
delete from condition where pubdate = '2020-01-18 19:00:00' and creatat = '2020-01-18 20:23:40';
select count(*) from condition;
-- smazat ctvrty zaznam!!!
select * from condition where pubdate = '2020-10-25 08:00:00' and creatat = '2020-10-25 08:45:10';
select count(*) from condition;
delete from condition where pubdate = '2020-10-25 08:00:00' and creatat = '2020-10-25 08:45:10';
select count(*) from condition;
--odhali duplicity
select distinct strftime('%Y-%m-%d %H', pubdate), count(*) from condition group by 1 order by 2 desc;

select * from sqlite_master where type = 'table';
