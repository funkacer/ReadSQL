---folder:Weather;
---sqlite3:Weather.db;
select distinct strftime('%Y-%m-%d', pubdate), count(*) from condition group by 1 order by 2 desc;
--odhali duplicity (každou hodinu má být maximálně jeden publikovaný záznam)
select distinct strftime('%Y-%m-%d %H', pubdate), count(*) from condition group by 1 order by 2 desc;
select * from condition where strftime('%Y-%m-%d', pubdate) = '2020-01-18';
select * from condition where strftime('%Y-%m-%d', pubdate) = '2020-01-18' and  (creatat = '2020-01-18 20:23:40' or creatat = '2020-01-18 20:15:13');
select * from condition where strftime('%Y-%m-%d', pubdate) = '2020-10-25';
select * from condition where strftime('%Y-%m-%d', pubdate) = '2020-10-25' and  (creatat = '2020-10-25 08:45:10' or creatat = '2020-10-25 08:45:13');
-- tyto tri zaznamy s _id =1 smazat!!!
select * from condition where pubdate = '2020-01-18 19:00:00' and  (creatat = '2020-01-18 20:23:40');
-- toto je OK, spustil jsem to rucne 20:15 a pak automaticka aktualizace 20:45 pro ruzne pubdate!!!
select * from condition where strftime('%Y-%m-%d', pubdate) = '2020-01-18' and  (creatat = '2020-01-18 20:15:13');
select * from condition where _file='20200621.db' and (_id = 1 or _id = 2 or _id = 3);
-- toto je duplicita
select distinct * from condition where strftime('%Y-%m-%d %H', pubdate) = '2020-10-25 08' ;
-- smazat zaznam
select * from condition where pubdate = '2020-10-25 08:00:00' and  (creatat = '2020-10-25 08:45:10');
