\folder Bla nks;
\postgre "bla nks";

--show tables;

DROP TABLE if exists a;
CREATE TABLE IF NOT EXISTS a AS SELECT * FROM b;

drop table if exists "moje a";
create table "moje a" ("i d" int, "t ext" text);
select id as "i d", code as "t ext" from a;
\insert moje a;
select * from "moje a";

drop table if exists "moje a";
create table "moje a" as select id as "i d", code as "t ext" from a;
select * from "moje a";
