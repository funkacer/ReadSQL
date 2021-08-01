---use:Weather.db;
-- tyto tri zaznamy s _id =1 smazat!!!
select * from condition where pubdate = '2020-01-18 19:00:00' and creatat = '2020-01-18 20:23:40';
select count(*) from condition;
delete from condition where pubdate = '2020-01-18 19:00:00' and creatat = '2020-01-18 20:23:40';
select count(*) from condition;
-- smazat zaznam!!!
select * from condition where pubdate = '2020-10-25 08:00:00' and creatat = '2020-10-25 08:45:10';
select count(*) from condition;
delete from condition where pubdate = '2020-10-25 08:00:00' and creatat = '2020-10-25 08:45:10';
select count(*) from condition;
--odhali duplicity
select distinct strftime('%Y-%m-%d %H', pubdate), count(*) from condition group by 1 order by 2 desc;
