\f "2 Udacity BA";
\s "Udacity_2_15.db";

drop table if exists t1;
create table t1 (id integer primary key autoincrement, code text, value int);

insert into t1 values (Null, "x1", 15);
insert into t1 values (Null, "x2", 4);
insert into t1 values (Null, "x3", 3);
insert into t1 values (Null, "x4", 8);
insert into t1 values (Null, "x5", 15);
insert into t1 values (Null, "x6", 22);
insert into t1 values (Null, "x7", 7);
insert into t1 values (Null, "x8", 9);
insert into t1 values (Null, "x9", 2);
insert into t1 values (Null, "x10", 3);
insert into t1 values (Null, "x11", 3);
insert into t1 values (Null, "x12", 12);
insert into t1 values (Null, "x13", 6);

select * from t1;

\dp;
