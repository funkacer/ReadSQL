\f "2 Udacity BA";
\s "Udacity_2_5_2.db";

drop table t1;
create table t1 (id integer primary key autoincrement, code text, value int);

insert into t1 values (Null, "x1", 5);
insert into t1 values (Null, "x2", 10);
insert into t1 values (Null, "x3", 3);
insert into t1 values (Null, "x4", 8);
insert into t1 values (Null, "x5", 12);
insert into t1 values (Null, "x6", 4);
insert into t1 values (Null, "x7", 1);
insert into t1 values (Null, "x8", 2);
insert into t1 values (Null, "x9", 8);

select * from t1;

\dp;
