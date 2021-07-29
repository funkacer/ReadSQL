---use:test.db;
select * from sqlite_master where type = 'table';
--drop table IF EXISTS moje1;
--create table moje1 (id integer primary key autoincrement, value real, code text);
--insert into moje1 values (Null, 122.5, 'Ahoj');
select * from sqlite_master;

-- select * from moje1
select * from moje1 --select * from moje1

;
---use:a.db;
select value, code from moje1;
---use:test.db;
---insert:moje1;
select * from moje1;

---save:test.txt;
