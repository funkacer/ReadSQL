\f '0 SQL Basics\Create table from';
\cmssql Test;

drop table if exists table1;
create table table1 (id INT NOT NULL IDENTITY(1,1) PRIMARY KEY, value REAL, code INTEGER, label TEXT);
select * from table1;

insert into table1 (value, code, label) values (0,0,'Zero');
insert into table1 (value, code, label) values (1.1,1,'One');
insert into table1 (value, code, label) values (2.2,2,'Two');
insert into table1 (value, code, label) values (3.3,3,'Three');
insert into table1 (value, code, label) values (4.4,4,'Four');
insert into table1 (value, code, label) values (5.5,5,'Five');
insert into table1 (value, code, label) values (6.6,6,'Six');
insert into table1 (value, code, label) values (7.7,7,'Seven');
insert into table1 (value, code, label) values (8.8,8,'Eight');
insert into table1 (value, code, label) values (9.9,9,'Nine');
insert into table1 (value, code, label) values (10.10,10,'Ten');

select * into aaa from table1;
select * from aaa;
\pda tt = "Create table aaa as select * from table1;" tc = 51010;
select id, FORMAT(value, '##.##') as value, code, label from aaa;
select id, Cast(CONVERT(DECIMAL(10,1),value) as nvarchar) AS value, code, label from aaa;
drop table aaa;

SELECT DB_NAME();
SELECT Distinct TABLE_NAME FROM information_schema.TABLES;
SELECT * FROM information_schema.TABLES;
