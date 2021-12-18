\folder Bla nks;
\mssql "bla nks";

SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE';

DROP TABLE if exists a;
SELECT * INTO a FROM b;

drop table if exists "moje a";
create table "moje a" ("i d" int, "t ext" text);
select id as "i d", code as "t ext" from a;
\insert moje a;
select * from "moje a";

drop table if exists "moje a";
SELECT id as "i d", code as "t ext" into"moje a" from a;
select * from "moje a";
