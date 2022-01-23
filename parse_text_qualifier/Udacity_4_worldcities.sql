\f parse_text_quantificator;
\s Udacity_4_worldcities.db;

drop table if exists t1;
create table t1 (id integer primary key autoincrement, City text, Country text);

\r "Udacity_4_worldcities_select.csv", ",", text_qualifier = '"';
\i t1;
select * from t1;

\r "Udacity_4_worldcities.csv", ",", text_qualifier = '"';
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
