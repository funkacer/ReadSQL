\f parse_text_qualifier;
\s Udacity_4_worldcities.db;

drop table if exists t1;
create table t1 (id integer primary key autoincrement, City text, Country text);

\r "Udacity_4_worldcities_select.txt", text_qualifier = '"';
\i t1;
select * from t1;

\r "Udacity_4_worldcities_select1.txt", text_qualifier = '"';
\i t1;
select * from t1;

\r "Udacity_4_worldcities_select.csv", ",", text_qualifier = '"';
\i t1;
select * from t1;

\r f = "Udacity_4_worldcities_select.csv", d = ",", t = '"';
\i t1;
select * from t1;

\r "Udacity_4_worldcities_select.csv", ",", tq = '"';
\i t1;
select * from t1;

\r "Udacity_4_worldcities.csv", ",", '"';
\pd l = [1565, 7233];
\dp;
\i t1;

select * from t1;
\pd l = [1565, 7233];
\dp;

\r "Udacity_4_worldcities1.csv", ",";
\pd l = [1565, 7233];
\dp;
\i t1;

\r "Udacity_4_worldcities_nodata.csv", ",";
\pd l = [1565, 7233];
\dp;
\i t1;

\r "Udacity_4_worldcities_columns_only.csv", ",";
\pd l = [1565, 7233];
\dp;
\i t1;

\r "Udacity_4_worldcities_select_error1.csv", ",";
\pd l = [1565, 7233];
\dp;
\i t1;
