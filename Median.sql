\s "Median.db";

drop table t1;
create table t1 (id integer primary key autoincrement, code text, value int);

insert into t1 values (Null, "x1", 10);
insert into t1 values (Null, "x2", 9);
insert into t1 values (Null, "x3", 8);
insert into t1 values (Null, "x4", 7);
insert into t1 values (Null, "x5", 6);
insert into t1 values (Null, "x6", 5);
insert into t1 values (Null, "x7", 4);
insert into t1 values (Null, "x8", 3);
insert into t1 values (Null, "x9", 2);
insert into t1 values (Null, "x10", 1);

select * from t1;

\dp;
