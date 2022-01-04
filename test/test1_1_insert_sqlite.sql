\folder test;
\sqlite3 test.dbx;

select * from sqlite_master where type = "table";

drop table if exists test1;

create table test1 (id INTEGER PRIMARY KEY AUTOINCREMENT, V integer, B integer, D text, U text, SP REAL, SE REAL, ZE text, ZT text, K text);

\read test1.csvx;

\insert test1;

\print columns;
