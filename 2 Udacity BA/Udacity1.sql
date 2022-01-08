\f "2 Udacity BA";
\s "2 Udacity BA.db";

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

select count(*) from t1;
select sum(value) from t1;
select (sum(value) + 6) as "sum2-7" from t1 where id >= 2;
select value from t1 where id = 5;
select sum(value)/((select count(*) from t1)-1) as "sum3-6/n-1" from t1 where id >= 3 and id <= 6;
