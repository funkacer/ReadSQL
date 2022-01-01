\f "0 SQL Basics\Create table from";
\s create table from.sql;
#\\this is error, should be red!!!;
\s create table from.db;
create table table1 (id integer auto_increment primary key, value real, code integer, label text);
select * from table1;
insert into table1 values (Null, 12.5,1,"One");
