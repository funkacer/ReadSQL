\f "0 SQL Basics\Create table from";
\s create table from.db;
drop table if exists table1;
create table table1 (id INTEGER PRIMARY KEY AUTOINCREMENT, value REAL, code INTEGER, label TEXT);
select * from table1;

insert into table1 values (Null,0,0,"Zero");
insert into table1 values (Null, 1.1,1,"One");
insert into table1 values (Null, 2.2,2,"Two");
insert into table1 values (Null, 3.3,3,"Three");
insert into table1 values (Null, 4.4,4,"Four");
insert into table1 values (Null, 5.5,5,"Five");
insert into table1 values (Null, 6.6,6,"Six");
insert into table1 values (Null, 7.7,7,"Seven");
insert into table1 values (Null, 8.8,8,"Eight");
insert into table1 values (Null, 9.9,9,"Nine");
insert into table1 values (Null, 10.10,10,"Ten");

create table aaa as select * from table1;
select * from aaa;
drop table aaa;
select * from sqlite_master where type = "table";
