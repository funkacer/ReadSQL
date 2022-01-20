\f "2 Udacity BA";
\s "Udacity_4_albb_salaries_2003.db";

drop table if exists t1;
create table t1 (id integer primary key autoincrement, Team text, "Last Name" text, "First Name" text, Salary int, Position text);

\r "Udacity_4_albb-salaries-2003.txt", "	";
\dp;
\i t1;

select * from t1;
\dp;
