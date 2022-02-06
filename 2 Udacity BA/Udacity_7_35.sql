\f "2 Udacity BA";
\cs Udacity_7_35.db;

drop table if exists t1;
create table t1 (id INTEGER PRIMARY KEY AUTOINCREMENT, Region TEXT, "Sale Leads" INT);

\r "Udacity_7_35.txt";

\dsa c=['Region', 'Sale Leads'];

\insert t1;

select * from t1;
