\f parse_text_quantificator;
\s Udacity_4_worldcities.db;

drop table if exists t1;
create table t1 (id integer primary key autoincrement, City text, Country text);

\r "Udacity_4_worldcities_select_error1.csv", ",", text_qualifier = '"';
\i t1;
select * from t1;
\q;
