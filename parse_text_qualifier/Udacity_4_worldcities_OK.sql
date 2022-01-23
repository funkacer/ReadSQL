\f parse_text_qualifier;
\s Udacity_4_worldcities.db;

drop table if exists t1;
create table t1 (id integer primary key autoincrement, City text, Country text);

\r "Udacity_4_worldcities.csv", ",", '"';
\pd l = [1565, 7233];
\dp;
\i t1;

select * from t1;
\pd l = [1565, 7233];
\dp;
