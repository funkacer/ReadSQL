\folder Bla nks;
\sqlite3 bla nks.db;

select * from sqlite_master;

--DROP TABLE a;
CREATE TABLE IF NOT EXISTS a AS SELECT * FROM b;

drop table if exists "moje a";
create table "moje a" ("i d" int, "t ext" text);
select id as "i d", code as "t ext" from a;
\insert moje a;
