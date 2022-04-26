\folder test;
\c mysql test;

show tables;

drop table if exists test1;

create table test1 (id INTEGER PRIMARY KEY AUTO_INCREMENT, V integer, B integer, D text, U text, SP REAL, SE REAL, ZE text, ZT text, K text);

\read test1.csvx, ";";

\insert test1;

\load test1_4_analyse.sql;

\print columns;
