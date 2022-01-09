\f "2 Udacity BA";
\s "Udacity_2_9.db";

drop table t1;
create table t1 (id integer primary key autoincrement, code text, value int);

insert into t1 values (Null, "x1", 1);
insert into t1 values (Null, "x2", 5);
insert into t1 values (Null, "x3", 10);
insert into t1 values (Null, "x4", 3);
insert into t1 values (Null, "x5", 8);
insert into t1 values (Null, "x6", 12);
insert into t1 values (Null, "x7", 4);

select * from t1;

\dp;
