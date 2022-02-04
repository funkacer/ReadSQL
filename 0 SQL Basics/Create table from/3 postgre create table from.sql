\f '0 SQL Basics\Create table from';
\# case sensitive;
\cpostgre Test;

drop table if exists table1;
create table table1 (id SERIAL PRIMARY KEY, value REAL, code INTEGER, label TEXT);
select * from table1;

insert into table1 values (DEFAULT,0,0,'Zero');
insert into table1 values (DEFAULT,1.1,1,'One');
insert into table1 values (DEFAULT, 2.2,2,'Two');
insert into table1 values (DEFAULT, 3.3,3,'Three');
insert into table1 values (DEFAULT, 4.4,4,'Four');
insert into table1 values (DEFAULT, 5.5,5,'Five');
insert into table1 values (DEFAULT, 6.6,6,'Six');
insert into table1 values (DEFAULT, 7.7,7,'Seven');
insert into table1 values (DEFAULT, 8.8,8,'Eight');
insert into table1 values (DEFAULT, 9.9,9,'Nine');
insert into table1 values (DEFAULT, 10.10,10,'Ten');

create table aaa as select * from table1;
select * from aaa;
\pda tt = "Create table aaa as select * from table1;" tc = 51010;
drop table aaa;

SELECT current_database();
SELECT *
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND
    schemaname != 'information_schema';
