\folder test;
\s test.dbx;

select * from sqlite_master;

drop table if exists test2;

create table test2 (r INTEGER PRIMARY KEY AUTOINCREMENT, id INTEGER, id_p INTEGER,
    V integer, B integer, D text, DT text, UT text, SP REAL, SE REAL,
    E datetime, A datetime);

\read test2.csvx;

\insert test2;

\print columns;

select * from test2;
