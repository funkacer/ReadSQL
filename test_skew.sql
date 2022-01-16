\s "test_skew.db";

drop table if exists t1;
create table t1 (id integer primary key autoincrement, code text, value int);

insert into t1 values (Null, "x1", 0);
insert into t1 values (Null, "x2", 2);
insert into t1 values (Null, "x3", 3);
insert into t1 values (Null, "x4", 4);
insert into t1 values (Null, "x5", 5);
insert into t1 values (Null, "x6", 6);
insert into t1 values (Null, "x7", 7);

select * from t1;

\dp;


drop table if exists t2;
create table t2 (id integer primary key autoincrement, code text, value int);

insert into t2 values (Null, "x1", 1);
insert into t2 values (Null, "x2", 5);
insert into t2 values (Null, "x3", 10);
insert into t2 values (Null, "x4", 3);
insert into t2 values (Null, "x5", 8);
insert into t2 values (Null, "x6", 12);
insert into t2 values (Null, "x7", 4);

select * from t2;

\dp;
