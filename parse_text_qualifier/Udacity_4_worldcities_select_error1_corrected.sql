\f parse_text_qualifier;
\s Udacity_4_worldcities.db;

drop table if exists t1;
create table t1 (id integer primary key autoincrement, City text, Country text);

\r "Udacity_4_worldcities_select_error1.csv", ",", text_qualifier = '"';
\i t1;
select * from t1;
\pd 100;

\r "Udacity_4_worldcities_select_error1_test_blanks.csv", ",", text_qualifier = '"';

\r "Udacity_4_worldcities_select_error1_test_not_corrected.csv", ",", text_qualifier = '"';
