\folder test;
\mysql test;

show tables;

drop table if exists test3_1;

create table test3_1 (r INTEGER PRIMARY KEY AUTO_INCREMENT, id INTEGER, id_p INTEGER,
    V integer, B integer, D text, DT text, UT text, SP REAL, SE REAL,
    E datetime, A datetime);

\read test3_1.csvx;

\insert test3_1;

\print columns;
