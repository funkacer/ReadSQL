\f "2 Udacity BA";
\s "Udacity_1_23.db";

drop table t1;
create table t1 (id integer primary key autoincrement, code text, value int);

insert into t1 values (Null, "x1", 5);
insert into t1 values (Null, "x2", 15);
insert into t1 values (Null, "x3", 3);
insert into t1 values (Null, "x4", 3);
insert into t1 values (Null, "x5", 8);
insert into t1 values (Null, "x6", 10);
insert into t1 values (Null, "x7", 12);

select * from t1;

select count(*) as "n" from t1;
select sum(value) as "sum(x1-xn)"from t1;
select (sum(value) + 6) as "sum(x2-x7)" from t1 where id >= 2;
select value as "x5" from t1 where id = 5;
select sum(value)/((select count(*) from t1)-1) as "sum(x3-x6)/(n-1)" from t1 where id >= 3 and id <= 6;
