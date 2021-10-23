---folder:6 SQL Queries;
---sqlite3:data.db;
drop table IF EXISTS bill;
create table bill (id INTEGER PRIMARY KEY AUTOINCREMENT, month DATE, type TEXT, Amount REAL);
insert into bill VALUES (null, "2021-01-01", "M", 1000);
insert into bill VALUES (null, "2021-01-01", "F", 1000);
insert into bill VALUES (null, "2021-02-01", "M", 3000);
insert into bill VALUES (null, "2021-02-01", "M", 4000);
insert into bill VALUES (null, "2021-03-01", "F", 5000);
insert into bill VALUES (null, "2021-03-01", "F", 6000);
insert into bill VALUES (null, "2021-03-01", "F", 7000);
insert into bill VALUES (null, "2021-03-01", "M", 8000);
insert into bill VALUES (null, "2021-04-01", "F", 9000);
insert into bill VALUES (null, "2021-04-01", "F", 9000);
insert into bill VALUES (null, "2021-04-01", "F", 11000);

select * from bill;
